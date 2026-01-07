import { tool } from '@anthropic-ai/claude-agent-sdk';
import { z } from 'zod';
import { getDatabase } from '../database/schema.js';

const formatResponse = (data: any) => ({
  content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }],
});

export const createTaskTool = tool(
  'create_task',
  'Create a new task/card in a list. Tasks can be assigned to team members and have priorities and due dates.',
  {
    title: z.string().describe('Title of the task'),
    list_id: z.number().describe('ID of the list to add the task to'),
    description: z.string().optional().describe('Detailed description of the task'),
    creator_id: z.number().describe('ID of the user creating the task'),
    assignee_id: z.number().optional().describe('ID of the user to assign the task to'),
    priority: z.enum(['low', 'medium', 'high', 'urgent']).default('medium').describe('Priority level'),
    due_date: z.string().optional().describe('Due date in ISO format (YYYY-MM-DD)'),
  },
  async (input) => {
    const db = getDatabase();
    try {
      const maxPos = db.prepare(`SELECT MAX(position) as max_pos FROM tasks WHERE list_id = ?`).get(input.list_id) as { max_pos: number | null };
      const position = (maxPos.max_pos || 0) + 1;

      const result = db.prepare(`
        INSERT INTO tasks (title, description, list_id, position, priority, due_date, assignee_id, creator_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
      `).run(input.title, input.description || null, input.list_id, position, input.priority, input.due_date || null, input.assignee_id || null, input.creator_id);

      const task = db.prepare(`
        SELECT t.*, u.full_name as assignee_name, c.full_name as creator_name, l.name as list_name
        FROM tasks t
        LEFT JOIN users u ON t.assignee_id = u.id
        LEFT JOIN users c ON t.creator_id = c.id
        LEFT JOIN lists l ON t.list_id = l.id
        WHERE t.id = ?
      `).get(result.lastInsertRowid);

      return formatResponse({ success: true, message: `Task created: ${input.title}`, task });
    } catch (error: any) {
      return formatResponse({ success: false, message: `Failed to create task: ${error.message}` });
    }
  }
);

export const updateTaskTool = tool(
  'update_task',
  'Update task details such as title, description, priority, assignee, or due date.',
  {
    task_id: z.number().describe('ID of the task to update'),
    title: z.string().optional().describe('New title'),
    description: z.string().optional().describe('New description'),
    priority: z.enum(['low', 'medium', 'high', 'urgent']).optional().describe('New priority'),
    assignee_id: z.number().optional().describe('New assignee user ID'),
    due_date: z.string().optional().describe('New due date in ISO format'),
  },
  async (input) => {
    const db = getDatabase();
    try {
      const updates: string[] = [];
      const params: any[] = [];

      if (input.title !== undefined) {
        updates.push('title = ?');
        params.push(input.title);
      }
      if (input.description !== undefined) {
        updates.push('description = ?');
        params.push(input.description);
      }
      if (input.priority !== undefined) {
        updates.push('priority = ?');
        params.push(input.priority);
      }
      if (input.assignee_id !== undefined) {
        updates.push('assignee_id = ?');
        params.push(input.assignee_id);
      }
      if (input.due_date !== undefined) {
        updates.push('due_date = ?');
        params.push(input.due_date);
      }

      if (updates.length === 0) {
        return formatResponse({ success: false, message: 'No fields to update' });
      }

      updates.push('updated_at = CURRENT_TIMESTAMP');
      params.push(input.task_id);

      const result = db.prepare(`UPDATE tasks SET ${updates.join(', ')} WHERE id = ?`).run(...params);

      if (result.changes === 0) {
        return formatResponse({ success: false, message: 'Task not found' });
      }

      const task = db.prepare(`
        SELECT t.*, u.full_name as assignee_name, l.name as list_name
        FROM tasks t
        LEFT JOIN users u ON t.assignee_id = u.id
        LEFT JOIN lists l ON t.list_id = l.id
        WHERE t.id = ?
      `).get(input.task_id);

      return formatResponse({ success: true, message: 'Task updated successfully', task });
    } catch (error: any) {
      return formatResponse({ success: false, message: `Failed to update task: ${error.message}` });
    }
  }
);

export const moveTaskTool = tool(
  'move_task',
  'Move a task to a different list (e.g., from "To Do" to "In Progress"). This is how you track task status.',
  {
    task_id: z.number().describe('ID of the task to move'),
    target_list_id: z.number().describe('ID of the list to move the task to'),
    position: z.number().optional().describe('Position in the target list (default: end of list)'),
  },
  async (input) => {
    const db = getDatabase();
    try {
      const task = db.prepare('SELECT * FROM tasks WHERE id = ?').get(input.task_id);
      if (!task) return formatResponse({ success: false, message: 'Task not found' });

      let targetPosition = input.position;
      if (targetPosition === undefined) {
        const maxPos = db.prepare(`SELECT MAX(position) as max_pos FROM tasks WHERE list_id = ?`).get(input.target_list_id) as { max_pos: number | null };
        targetPosition = (maxPos.max_pos || 0) + 1;
      }

      db.prepare(`UPDATE tasks SET list_id = ?, position = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?`).run(input.target_list_id, targetPosition, input.task_id);

      const updatedTask = db.prepare(`
        SELECT t.*, l.name as list_name, u.full_name as assignee_name
        FROM tasks t
        LEFT JOIN lists l ON t.list_id = l.id
        LEFT JOIN users u ON t.assignee_id = u.id
        WHERE t.id = ?
      `).get(input.task_id);

      return formatResponse({ success: true, message: `Task moved to ${(updatedTask as any).list_name}`, task: updatedTask });
    } catch (error: any) {
      return formatResponse({ success: false, message: `Failed to move task: ${error.message}` });
    }
  }
);

export const assignTaskTool = tool(
  'assign_task',
  'Assign or reassign a task to a team member.',
  {
    task_id: z.number().describe('ID of the task'),
    assignee_id: z.number().describe('ID of the user to assign the task to'),
  },
  async (input) => {
    const db = getDatabase();
    try {
      const result = db.prepare(`UPDATE tasks SET assignee_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?`).run(input.assignee_id, input.task_id);

      if (result.changes === 0) {
        return formatResponse({ success: false, message: 'Task not found' });
      }

      const task = db.prepare(`
        SELECT t.*, u.full_name as assignee_name
        FROM tasks t
        LEFT JOIN users u ON t.assignee_id = u.id
        WHERE t.id = ?
      `).get(input.task_id);

      return formatResponse({ success: true, message: `Task assigned to ${(task as any).assignee_name}`, task });
    } catch (error: any) {
      return formatResponse({ success: false, message: `Failed to assign task: ${error.message}` });
    }
  }
);

export const listTasksTool = tool(
  'list_tasks',
  'List tasks with various filters. Useful for viewing tasks by assignee, priority, or board.',
  {
    board_id: z.number().optional().describe('Filter by board'),
    list_id: z.number().optional().describe('Filter by list'),
    assignee_id: z.number().optional().describe('Filter by assignee'),
    priority: z.enum(['low', 'medium', 'high', 'urgent']).optional().describe('Filter by priority'),
  },
  async (input) => {
    const db = getDatabase();
    try {
      let query = `
        SELECT t.*, u.full_name as assignee_name, c.full_name as creator_name, l.name as list_name, b.name as board_name
        FROM tasks t
        LEFT JOIN users u ON t.assignee_id = u.id
        LEFT JOIN users c ON t.creator_id = c.id
        LEFT JOIN lists l ON t.list_id = l.id
        LEFT JOIN boards b ON l.board_id = b.id
        WHERE 1=1
      `;
      const params: any[] = [];

      if (input.list_id) {
        query += ' AND t.list_id = ?';
        params.push(input.list_id);
      }
      if (input.board_id) {
        query += ' AND b.id = ?';
        params.push(input.board_id);
      }
      if (input.assignee_id) {
        query += ' AND t.assignee_id = ?';
        params.push(input.assignee_id);
      }
      if (input.priority) {
        query += ' AND t.priority = ?';
        params.push(input.priority);
      }

      query += ' ORDER BY t.priority DESC, t.position ASC';

      const tasks = db.prepare(query).all(...params);
      return formatResponse({ success: true, count: tasks.length, tasks });
    } catch (error: any) {
      return formatResponse({ success: false, message: `Failed to list tasks: ${error.message}` });
    }
  }
);

export const deleteTaskTool = tool(
  'delete_task',
  'Delete a task from the system.',
  {
    task_id: z.number().describe('ID of the task to delete'),
  },
  async (input) => {
    const db = getDatabase();
    try {
      const task = db.prepare('SELECT title FROM tasks WHERE id = ?').get(input.task_id) as { title: string } | undefined;

      if (!task) {
        return formatResponse({ success: false, message: 'Task not found' });
      }

      db.prepare('DELETE FROM tasks WHERE id = ?').run(input.task_id);
      return formatResponse({ success: true, message: `Task deleted: ${task.title}` });
    } catch (error: any) {
      return formatResponse({ success: false, message: `Failed to delete task: ${error.message}` });
    }
  }
);

export const addCommentTool = tool(
  'add_comment',
  'Add a comment to a task for discussion or updates.',
  {
    task_id: z.number().describe('ID of the task'),
    user_id: z.number().describe('ID of the user adding the comment'),
    content: z.string().describe('Comment content'),
  },
  async (input) => {
    const db = getDatabase();
    try {
      const result = db.prepare(`INSERT INTO comments (task_id, user_id, content) VALUES (?, ?, ?)`).run(input.task_id, input.user_id, input.content);

      const comment = db.prepare(`
        SELECT c.*, u.full_name as user_name
        FROM comments c
        LEFT JOIN users u ON c.user_id = u.id
        WHERE c.id = ?
      `).get(result.lastInsertRowid);

      return formatResponse({ success: true, message: 'Comment added', comment });
    } catch (error: any) {
      return formatResponse({ success: false, message: `Failed to add comment: ${error.message}` });
    }
  }
);

export const getTaskTool = tool(
  'get_task',
  'Get full details of a task including all comments.',
  {
    task_id: z.number().describe('ID of the task'),
  },
  async (input) => {
    const db = getDatabase();
    try {
      const task = db.prepare(`
        SELECT t.*, u.full_name as assignee_name, c.full_name as creator_name, l.name as list_name, b.name as board_name, p.name as project_name
        FROM tasks t
        LEFT JOIN users u ON t.assignee_id = u.id
        LEFT JOIN users c ON t.creator_id = c.id
        LEFT JOIN lists l ON t.list_id = l.id
        LEFT JOIN boards b ON l.board_id = b.id
        LEFT JOIN projects p ON b.project_id = p.id
        WHERE t.id = ?
      `).get(input.task_id);

      if (!task) {
        return formatResponse({ success: false, message: 'Task not found' });
      }

      const comments = db.prepare(`
        SELECT c.*, u.full_name as user_name
        FROM comments c
        LEFT JOIN users u ON c.user_id = u.id
        WHERE c.task_id = ?
        ORDER BY c.created_at ASC
      `).all(input.task_id);

      return formatResponse({ success: true, task: { ...(task as object), comments } });
    } catch (error: any) {
      return formatResponse({ success: false, message: `Failed to get task: ${error.message}` });
    }
  }
);

import { tool } from '@anthropic-ai/claude-agent-sdk';
import { z } from 'zod';
import { getDatabase } from '../database/schema.js';

const formatResponse = (data: any) => ({
  content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }],
});

export const createProjectTool = tool(
  'create_project',
  'Create a new project. A project is a container for boards and can have multiple team members.',
  {
    name: z.string().describe('Name of the project'),
    description: z.string().optional().describe('Description of the project'),
    owner_id: z.number().describe('User ID of the project owner'),
  },
  async (input) => {
    const db = getDatabase();
    try {
      const stmt = db.prepare(`INSERT INTO projects (name, description, owner_id) VALUES (?, ?, ?)`);
      const result = stmt.run(input.name, input.description || null, input.owner_id);
      const projectId = result.lastInsertRowid;

      db.prepare(`INSERT INTO project_members (project_id, user_id, role) VALUES (?, ?, 'owner')`).run(projectId, input.owner_id);

      const project = db.prepare('SELECT * FROM projects WHERE id = ?').get(projectId);
      return formatResponse({ success: true, message: `Project created: ${input.name}`, project });
    } catch (error: any) {
      return formatResponse({ success: false, message: `Failed to create project: ${error.message}` });
    }
  }
);

export const listProjectsTool = tool(
  'list_projects',
  'List all projects or filter by status. Shows project details and member count.',
  {
    status: z.enum(['active', 'archived', 'completed']).optional().describe('Filter by project status'),
    user_id: z.number().optional().describe('Filter projects by user membership'),
  },
  async (input) => {
    const db = getDatabase();
    try {
      let query = `
        SELECT p.*, u.full_name as owner_name, COUNT(DISTINCT pm.user_id) as member_count, COUNT(DISTINCT b.id) as board_count
        FROM projects p
        LEFT JOIN users u ON p.owner_id = u.id
        LEFT JOIN project_members pm ON p.id = pm.project_id
        LEFT JOIN boards b ON p.id = b.project_id
      `;
      const conditions: string[] = [];
      const params: any[] = [];

      if (input.status) {
        conditions.push('p.status = ?');
        params.push(input.status);
      }
      if (input.user_id) {
        conditions.push('pm.user_id = ?');
        params.push(input.user_id);
      }
      if (conditions.length > 0) query += ' WHERE ' + conditions.join(' AND ');
      query += ' GROUP BY p.id ORDER BY p.created_at DESC';

      const projects = db.prepare(query).all(...params);
      return formatResponse({ success: true, count: projects.length, projects });
    } catch (error: any) {
      return formatResponse({ success: false, message: `Failed to list projects: ${error.message}` });
    }
  }
);

export const addProjectMemberTool = tool(
  'add_project_member',
  'Add a user to a project as a member. This allows them to access and work on the project.',
  {
    project_id: z.number().describe('ID of the project'),
    user_id: z.number().describe('ID of the user to add'),
    role: z.enum(['admin', 'member']).default('member').describe('Role in the project'),
  },
  async (input) => {
    const db = getDatabase();
    try {
      db.prepare(`INSERT INTO project_members (project_id, user_id, role) VALUES (?, ?, ?)`).run(input.project_id, input.user_id, input.role);
      const user = db.prepare('SELECT full_name FROM users WHERE id = ?').get(input.user_id) as any;
      const project = db.prepare('SELECT name FROM projects WHERE id = ?').get(input.project_id) as any;
      return formatResponse({ success: true, message: `Added ${user.full_name} to project "${project.name}"` });
    } catch (error: any) {
      return formatResponse({ success: false, message: `Failed to add member: ${error.message}` });
    }
  }
);

export const createBoardTool = tool(
  'create_board',
  'Create a new board within a project. Boards contain lists and tasks (like Trello boards).',
  {
    name: z.string().describe('Name of the board'),
    project_id: z.number().describe('ID of the project this board belongs to'),
    description: z.string().optional().describe('Description of the board'),
    create_default_lists: z.boolean().default(true).describe('Create default lists (To Do, In Progress, Done)'),
  },
  async (input) => {
    const db = getDatabase();
    try {
      const result = db.prepare(`INSERT INTO boards (name, project_id, description) VALUES (?, ?, ?)`).run(input.name, input.project_id, input.description || null);
      const boardId = result.lastInsertRowid;

      if (input.create_default_lists !== false) {
        const defaultLists = ['To Do', 'In Progress', 'Done'];
        const listStmt = db.prepare(`INSERT INTO lists (name, board_id, position) VALUES (?, ?, ?)`);
        defaultLists.forEach((listName, index) => listStmt.run(listName, boardId, index));
      }

      const board = db.prepare('SELECT * FROM boards WHERE id = ?').get(boardId);
      return formatResponse({ success: true, message: `Board created: ${input.name}`, board });
    } catch (error: any) {
      return formatResponse({ success: false, message: `Failed to create board: ${error.message}` });
    }
  }
);

export const listBoardsTool = tool(
  'list_boards',
  'List all boards in a project with their lists.',
  {
    project_id: z.number().describe('ID of the project'),
  },
  async (input) => {
    const db = getDatabase();
    try {
      const boards = db.prepare(`
        SELECT b.*, COUNT(DISTINCT l.id) as list_count, COUNT(DISTINCT t.id) as task_count
        FROM boards b
        LEFT JOIN lists l ON b.id = l.board_id
        LEFT JOIN tasks t ON l.id = t.list_id
        WHERE b.project_id = ?
        GROUP BY b.id ORDER BY b.created_at DESC
      `).all(input.project_id);
      return formatResponse({ success: true, count: boards.length, boards });
    } catch (error: any) {
      return formatResponse({ success: false, message: `Failed to list boards: ${error.message}` });
    }
  }
);

export const getBoardTool = tool(
  'get_board',
  'Get detailed view of a board including all its lists and tasks.',
  {
    board_id: z.number().describe('ID of the board'),
  },
  async (input) => {
    const db = getDatabase();
    try {
      const board = db.prepare('SELECT * FROM boards WHERE id = ?').get(input.board_id);
      if (!board) return formatResponse({ success: false, message: 'Board not found' });

      const lists = db.prepare(`
        SELECT l.*, COUNT(t.id) as task_count FROM lists l LEFT JOIN tasks t ON l.id = t.list_id
        WHERE l.board_id = ? GROUP BY l.id ORDER BY l.position ASC
      `).all(input.board_id);

      for (const list of lists as any[]) {
        list.tasks = db.prepare(`
          SELECT t.*, u.full_name as assignee_name, c.full_name as creator_name
          FROM tasks t
          LEFT JOIN users u ON t.assignee_id = u.id
          LEFT JOIN users c ON t.creator_id = c.id
          WHERE t.list_id = ? ORDER BY t.position ASC
        `).all(list.id);
      }

      return formatResponse({ success: true, board: { ...board, lists } });
    } catch (error: any) {
      return formatResponse({ success: false, message: `Failed to get board: ${error.message}` });
    }
  }
);

export const createListTool = tool(
  'create_list',
  'Create a new list/column in a board (e.g., "Backlog", "Review", etc.).',
  {
    name: z.string().describe('Name of the list'),
    board_id: z.number().describe('ID of the board'),
  },
  async (input) => {
    const db = getDatabase();
    try {
      const maxPos = db.prepare(`SELECT MAX(position) as max_pos FROM lists WHERE board_id = ?`).get(input.board_id) as { max_pos: number | null };
      const position = (maxPos.max_pos || 0) + 1;
      const result = db.prepare(`INSERT INTO lists (name, board_id, position) VALUES (?, ?, ?)`).run(input.name, input.board_id, position);
      const list = db.prepare('SELECT * FROM lists WHERE id = ?').get(result.lastInsertRowid);
      return formatResponse({ success: true, message: `List created: ${input.name}`, list });
    } catch (error: any) {
      return formatResponse({ success: false, message: `Failed to create list: ${error.message}` });
    }
  }
);

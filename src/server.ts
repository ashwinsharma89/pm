#!/usr/bin/env node

import express from 'express';
import cors from 'cors';
import bodyParser from 'body-parser';
import session from 'express-session';
import path from 'path';
import { fileURLToPath } from 'url';
import { query } from '@anthropic-ai/claude-agent-sdk';
import { pmTools } from './agent.js';
import { closeDatabase, getDatabase } from './database/schema.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

const SYSTEM_PROMPT = `You are a helpful project management assistant for a team of up to 30 users.

Your primary responsibilities:
- Help users create and manage projects, boards, and tasks
- Assist with team member management and task assignments
- Provide insights on project status and team workload
- Make it easy to track work through different stages (To Do, In Progress, Done)

Key concepts:
- PROJECTS: Top-level containers that hold boards and have team members
- BOARDS: Like Trello boards, containing lists and tasks (e.g., "Sprint 1", "Marketing Campaign")
- LISTS: Columns in a board that represent stages (e.g., "To Do", "In Progress", "Done", "Review")
- TASKS: Individual work items that can be assigned, prioritized, and moved between lists
- USERS: Team members who can be assigned to projects and tasks

When users ask questions:
- Be proactive in suggesting best practices (e.g., creating boards for projects, organizing with lists)
- Provide clear summaries of project and task status
- Help users find information quickly

Always be helpful, concise, and focus on helping the team stay organized and productive.`;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(session({
  secret: process.env.SESSION_SECRET || 'pm-tool-secret-change-in-production',
  resave: false,
  saveUninitialized: true,
  cookie: { secure: false } // Set to true if using HTTPS
}));

// Serve static files from public directory
app.use(express.static(path.join(__dirname, '../public')));

// Tool names for allowed tools
const allToolNames = [
  'create_user', 'list_users', 'get_user', 'update_user', 'delete_user',
  'create_project', 'list_projects', 'add_project_member',
  'create_board', 'list_boards', 'get_board', 'create_list',
  'create_task', 'update_task', 'move_task', 'assign_task',
  'list_tasks', 'delete_task', 'add_comment', 'get_task'
];

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', message: 'PM Tool API is running' });
});

// Main chat/query endpoint - uses natural language
app.post('/api/chat', async (req, res) => {
  try {
    const { message } = req.body;

    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    // Run the query with Claude Agent SDK
    const q = query({
      prompt: `${SYSTEM_PROMPT}\n\nUser request: ${message}`,
      options: {
        model: 'claude-sonnet-4-5-20250929',
        cwd: process.cwd(),
        mcpServers: {
          'project-management-tools': pmTools,
        },
        allowedTools: allToolNames,
      },
    });

    let lastResponse = '';
    let toolCalls: any[] = [];

    for await (const msg of q) {
      if (msg.type === 'assistant' && msg.message.content) {
        for (const content of msg.message.content) {
          if (content.type === 'text') {
            lastResponse = content.text;
          } else if (content.type === 'tool_use') {
            toolCalls.push({
              name: content.name,
              input: content.input
            });
          }
        }
      } else if (msg.type === 'result') {
        return res.json({
          response: lastResponse,
          toolCalls: toolCalls,
          success: true
        });
      }
    }

    res.json({ response: lastResponse, toolCalls: toolCalls, success: true });
  } catch (error: any) {
    console.error('Chat error:', error);
    res.status(500).json({ error: error.message, success: false });
  }
});

// Direct database query endpoints (bypass agent for faster direct access)

// Users endpoints
app.get('/api/users', (req, res) => {
  try {
    const db = getDatabase();
    const users = db.prepare('SELECT id, username, full_name, email, role, created_at FROM users ORDER BY created_at DESC').all();
    res.json({ users, success: true });
  } catch (error: any) {
    res.status(500).json({ error: error.message, success: false });
  }
});

app.post('/api/users', (req, res) => {
  try {
    const { username, full_name, email, role = 'member' } = req.body;
    const db = getDatabase();
    const result = db.prepare('INSERT INTO users (username, full_name, email, role) VALUES (?, ?, ?, ?)').run(username, full_name, email, role);
    const user = db.prepare('SELECT * FROM users WHERE id = ?').get(result.lastInsertRowid);
    res.json({ user, success: true });
  } catch (error: any) {
    res.status(500).json({ error: error.message, success: false });
  }
});

// Projects endpoints
app.get('/api/projects', (req, res) => {
  try {
    const db = getDatabase();
    const projects = db.prepare(`
      SELECT p.*, u.full_name as owner_name, COUNT(DISTINCT pm.user_id) as member_count
      FROM projects p
      LEFT JOIN users u ON p.owner_id = u.id
      LEFT JOIN project_members pm ON p.id = pm.project_id
      GROUP BY p.id
      ORDER BY p.created_at DESC
    `).all();
    res.json({ projects, success: true });
  } catch (error: any) {
    res.status(500).json({ error: error.message, success: false });
  }
});

app.post('/api/projects', (req, res) => {
  try {
    const { name, description, owner_id } = req.body;
    const db = getDatabase();
    const result = db.prepare('INSERT INTO projects (name, description, owner_id) VALUES (?, ?, ?)').run(name, description || null, owner_id);
    const projectId = result.lastInsertRowid;
    db.prepare('INSERT INTO project_members (project_id, user_id, role) VALUES (?, ?, ?)').run(projectId, owner_id, 'owner');
    const project = db.prepare('SELECT * FROM projects WHERE id = ?').get(projectId);
    res.json({ project, success: true });
  } catch (error: any) {
    res.status(500).json({ error: error.message, success: false });
  }
});

// Boards endpoints
app.get('/api/boards', (req, res) => {
  try {
    const { project_id } = req.query;
    const db = getDatabase();
    let query = 'SELECT * FROM boards';
    const params: any[] = [];

    if (project_id) {
      query += ' WHERE project_id = ?';
      params.push(project_id);
    }

    query += ' ORDER BY created_at DESC';
    const boards = db.prepare(query).all(...params);
    res.json({ boards, success: true });
  } catch (error: any) {
    res.status(500).json({ error: error.message, success: false });
  }
});

app.get('/api/boards/:id', (req, res) => {
  try {
    const db = getDatabase();
    const board = db.prepare('SELECT * FROM boards WHERE id = ?').get(req.params.id);

    if (!board) {
      return res.status(404).json({ error: 'Board not found', success: false });
    }

    const lists = db.prepare(`
      SELECT l.*, COUNT(t.id) as task_count
      FROM lists l
      LEFT JOIN tasks t ON l.id = t.list_id
      WHERE l.board_id = ?
      GROUP BY l.id
      ORDER BY l.position ASC
    `).all(req.params.id);

    for (const list of lists as any[]) {
      list.tasks = db.prepare(`
        SELECT t.*, u.full_name as assignee_name, c.full_name as creator_name
        FROM tasks t
        LEFT JOIN users u ON t.assignee_id = u.id
        LEFT JOIN users c ON t.creator_id = c.id
        WHERE t.list_id = ?
        ORDER BY t.position ASC
      `).all(list.id);
    }

    res.json({ board: { ...board, lists }, success: true });
  } catch (error: any) {
    res.status(500).json({ error: error.message, success: false });
  }
});

app.post('/api/boards', (req, res) => {
  try {
    const { name, project_id, description } = req.body;
    const db = getDatabase();
    const result = db.prepare('INSERT INTO boards (name, project_id, description) VALUES (?, ?, ?)').run(name, project_id, description || null);
    const boardId = result.lastInsertRowid;

    // Create default lists
    const defaultLists = ['To Do', 'In Progress', 'Done'];
    const listStmt = db.prepare('INSERT INTO lists (name, board_id, position) VALUES (?, ?, ?)');
    defaultLists.forEach((listName, index) => listStmt.run(listName, boardId, index));

    const board = db.prepare('SELECT * FROM boards WHERE id = ?').get(boardId);
    res.json({ board, success: true });
  } catch (error: any) {
    res.status(500).json({ error: error.message, success: false });
  }
});

// Tasks endpoints
app.get('/api/tasks', (req, res) => {
  try {
    const { board_id, list_id, assignee_id } = req.query;
    const db = getDatabase();

    let query = `
      SELECT t.*, u.full_name as assignee_name, l.name as list_name, b.name as board_name
      FROM tasks t
      LEFT JOIN users u ON t.assignee_id = u.id
      LEFT JOIN lists l ON t.list_id = l.id
      LEFT JOIN boards b ON l.board_id = b.id
      WHERE 1=1
    `;
    const params: any[] = [];

    if (list_id) {
      query += ' AND t.list_id = ?';
      params.push(list_id);
    }
    if (board_id) {
      query += ' AND b.id = ?';
      params.push(board_id);
    }
    if (assignee_id) {
      query += ' AND t.assignee_id = ?';
      params.push(assignee_id);
    }

    query += ' ORDER BY t.position ASC';
    const tasks = db.prepare(query).all(...params);
    res.json({ tasks, success: true });
  } catch (error: any) {
    res.status(500).json({ error: error.message, success: false });
  }
});

app.post('/api/tasks', (req, res) => {
  try {
    const { title, list_id, description, creator_id, assignee_id, priority = 'medium', due_date } = req.body;
    const db = getDatabase();

    const maxPos = db.prepare('SELECT MAX(position) as max_pos FROM tasks WHERE list_id = ?').get(list_id) as { max_pos: number | null };
    const position = (maxPos.max_pos || 0) + 1;

    const result = db.prepare(`
      INSERT INTO tasks (title, description, list_id, position, priority, due_date, assignee_id, creator_id)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `).run(title, description || null, list_id, position, priority, due_date || null, assignee_id || null, creator_id);

    const task = db.prepare(`
      SELECT t.*, u.full_name as assignee_name, l.name as list_name
      FROM tasks t
      LEFT JOIN users u ON t.assignee_id = u.id
      LEFT JOIN lists l ON t.list_id = l.id
      WHERE t.id = ?
    `).get(result.lastInsertRowid);

    res.json({ task, success: true });
  } catch (error: any) {
    res.status(500).json({ error: error.message, success: false });
  }
});

app.put('/api/tasks/:id', (req, res) => {
  try {
    const { title, description, priority, assignee_id, due_date, list_id } = req.body;
    const db = getDatabase();

    const updates: string[] = [];
    const params: any[] = [];

    if (title !== undefined) { updates.push('title = ?'); params.push(title); }
    if (description !== undefined) { updates.push('description = ?'); params.push(description); }
    if (priority !== undefined) { updates.push('priority = ?'); params.push(priority); }
    if (assignee_id !== undefined) { updates.push('assignee_id = ?'); params.push(assignee_id); }
    if (due_date !== undefined) { updates.push('due_date = ?'); params.push(due_date); }
    if (list_id !== undefined) { updates.push('list_id = ?'); params.push(list_id); }

    if (updates.length > 0) {
      updates.push('updated_at = CURRENT_TIMESTAMP');
      params.push(req.params.id);
      db.prepare(`UPDATE tasks SET ${updates.join(', ')} WHERE id = ?`).run(...params);
    }

    const task = db.prepare(`
      SELECT t.*, u.full_name as assignee_name, l.name as list_name
      FROM tasks t
      LEFT JOIN users u ON t.assignee_id = u.id
      LEFT JOIN lists l ON t.list_id = l.id
      WHERE t.id = ?
    `).get(req.params.id);

    res.json({ task, success: true });
  } catch (error: any) {
    res.status(500).json({ error: error.message, success: false });
  }
});

app.delete('/api/tasks/:id', (req, res) => {
  try {
    const db = getDatabase();
    db.prepare('DELETE FROM tasks WHERE id = ?').run(req.params.id);
    res.json({ success: true, message: 'Task deleted' });
  } catch (error: any) {
    res.status(500).json({ error: error.message, success: false });
  }
});

// Serve the web UI
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../public/index.html'));
});

// Start server
const server = app.listen(PORT, () => {
  console.log(`🚀 PM Tool Web Server Running`);
  console.log(`==============================`);
  console.log(`Server: http://localhost:${PORT}`);
  console.log(`API:    http://localhost:${PORT}/api`);
  console.log(`\nPress Ctrl+C to stop\n`);
});

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\n\nShutting down...');
  server.close(() => {
    closeDatabase();
    process.exit(0);
  });
});

process.on('SIGTERM', () => {
  server.close(() => {
    closeDatabase();
    process.exit(0);
  });
});

export default app;

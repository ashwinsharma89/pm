import { tool } from '@anthropic-ai/claude-agent-sdk';
import { z } from 'zod';
import { getDatabase } from '../database/schema.js';
import type { User } from '../database/models.js';

// Create User Tool
export const createUserTool = tool(
  'create_user',
  'Create a new user in the project management system. This adds a team member who can be assigned to projects and tasks.',
  {
    username: z.string().describe('Unique username for the user'),
    full_name: z.string().describe('Full name of the user'),
    email: z.string().email().describe('Email address of the user'),
    role: z.enum(['admin', 'manager', 'member']).default('member').describe('Role of the user in the system'),
  },
  async (input) => {
    const db = getDatabase();

    try {
      const stmt = db.prepare(`
        INSERT INTO users (username, full_name, email, role)
        VALUES (?, ?, ?, ?)
      `);

      const result = stmt.run(input.username, input.full_name, input.email, input.role);

      const user = db.prepare('SELECT * FROM users WHERE id = ?').get(result.lastInsertRowid) as User;

      return {
        content: [{
          type: 'text' as const,
          text: JSON.stringify({
            success: true,
            message: `User created successfully: ${user.full_name} (${user.username})`,
            user: user,
          }, null, 2),
        }],
      };
    } catch (error: any) {
      return {
        content: [{
          type: 'text' as const,
          text: JSON.stringify({
            success: false,
            message: `Failed to create user: ${error.message}`,
          }, null, 2),
        }],
      };
    }
  }
);

// List Users Tool
export const listUsersTool = tool(
  'list_users',
  'List all users in the system. Optionally filter by role.',
  {
    role: z.enum(['admin', 'manager', 'member']).optional().describe('Filter users by role'),
  },
  async (input) => {
    const db = getDatabase();

    try {
      let query = 'SELECT * FROM users';
      const params: any[] = [];

      if (input.role) {
        query += ' WHERE role = ?';
        params.push(input.role);
      }

      query += ' ORDER BY created_at DESC';

      const users = db.prepare(query).all(...params) as User[];

      return {
        content: [{
          type: 'text' as const,
          text: JSON.stringify({
            success: true,
            count: users.length,
            users: users,
          }, null, 2),
        }],
      };
    } catch (error: any) {
      return {
        content: [{
          type: 'text' as const,
          text: JSON.stringify({
            success: false,
            message: `Failed to list users: ${error.message}`,
          }, null, 2),
        }],
      };
    }
  }
);

// Get User Tool
export const getUserTool = tool(
  'get_user',
  'Get details of a specific user by ID or username.',
  {
    user_id: z.number().optional().describe('User ID'),
    username: z.string().optional().describe('Username'),
  },
  async (input) => {
    const db = getDatabase();

    try {
      let user: User | undefined;

      if (input.user_id) {
        user = db.prepare('SELECT * FROM users WHERE id = ?').get(input.user_id) as User;
      } else if (input.username) {
        user = db.prepare('SELECT * FROM users WHERE username = ?').get(input.username) as User;
      } else {
        return {
          content: [{
            type: 'text' as const,
            text: JSON.stringify({
              success: false,
              message: 'Either user_id or username must be provided',
            }, null, 2),
          }],
        };
      }

      if (!user) {
        return {
          content: [{
            type: 'text' as const,
            text: JSON.stringify({
              success: false,
              message: 'User not found',
            }, null, 2),
          }],
        };
      }

      // Get user's projects
      const projects = db.prepare(`
        SELECT p.* FROM projects p
        JOIN project_members pm ON p.id = pm.project_id
        WHERE pm.user_id = ?
      `).all(user.id);

      return {
        content: [{
          type: 'text' as const,
          text: JSON.stringify({
            success: true,
            user: user,
            projects: projects,
          }, null, 2),
        }],
      };
    } catch (error: any) {
      return {
        content: [{
          type: 'text' as const,
          text: JSON.stringify({
            success: false,
            message: `Failed to get user: ${error.message}`,
          }, null, 2),
        }],
      };
    }
  }
);

// Update User Tool
export const updateUserTool = tool(
  'update_user',
  'Update user information such as name, email, or role.',
  {
    user_id: z.number().describe('ID of the user to update'),
    full_name: z.string().optional().describe('New full name'),
    email: z.string().email().optional().describe('New email address'),
    role: z.enum(['admin', 'manager', 'member']).optional().describe('New role'),
  },
  async (input) => {
    const db = getDatabase();

    try {
      const updates: string[] = [];
      const params: any[] = [];

      if (input.full_name) {
        updates.push('full_name = ?');
        params.push(input.full_name);
      }
      if (input.email) {
        updates.push('email = ?');
        params.push(input.email);
      }
      if (input.role) {
        updates.push('role = ?');
        params.push(input.role);
      }

      if (updates.length === 0) {
        return {
          content: [{
            type: 'text' as const,
            text: JSON.stringify({
              success: false,
              message: 'No fields to update',
            }, null, 2),
          }],
        };
      }

      updates.push('updated_at = CURRENT_TIMESTAMP');
      params.push(input.user_id);

      const stmt = db.prepare(`
        UPDATE users SET ${updates.join(', ')}
        WHERE id = ?
      `);

      const result = stmt.run(...params);

      if (result.changes === 0) {
        return {
          content: [{
            type: 'text' as const,
            text: JSON.stringify({
              success: false,
              message: 'User not found',
            }, null, 2),
          }],
        };
      }

      const user = db.prepare('SELECT * FROM users WHERE id = ?').get(input.user_id) as User;

      return {
        content: [{
          type: 'text' as const,
          text: JSON.stringify({
            success: true,
            message: 'User updated successfully',
            user: user,
          }, null, 2),
        }],
      };
    } catch (error: any) {
      return {
        content: [{
          type: 'text' as const,
          text: JSON.stringify({
            success: false,
            message: `Failed to update user: ${error.message}`,
          }, null, 2),
        }],
      };
    }
  }
);

// Delete User Tool
export const deleteUserTool = tool(
  'delete_user',
  'Delete a user from the system. Note: This will also remove them from all projects.',
  {
    user_id: z.number().describe('ID of the user to delete'),
  },
  async (input) => {
    const db = getDatabase();

    try {
      const user = db.prepare('SELECT * FROM users WHERE id = ?').get(input.user_id) as User;

      if (!user) {
        return {
          content: [{
            type: 'text' as const,
            text: JSON.stringify({
              success: false,
              message: 'User not found',
            }, null, 2),
          }],
        };
      }

      const stmt = db.prepare('DELETE FROM users WHERE id = ?');
      stmt.run(input.user_id);

      return {
        content: [{
          type: 'text' as const,
          text: JSON.stringify({
            success: true,
            message: `User deleted: ${user.full_name} (${user.username})`,
          }, null, 2),
        }],
      };
    } catch (error: any) {
      return {
        content: [{
          type: 'text' as const,
          text: JSON.stringify({
            success: false,
            message: `Failed to delete user: ${error.message}`,
          }, null, 2),
        }],
      };
    }
  }
);

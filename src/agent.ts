import { createSdkMcpServer } from '@anthropic-ai/claude-agent-sdk';
import { initializeDatabase } from './database/schema.js';

// Import all tools
import {
  createUserTool,
  listUsersTool,
  getUserTool,
  updateUserTool,
  deleteUserTool,
} from './tools/user-tools.js';

import {
  createProjectTool,
  listProjectsTool,
  addProjectMemberTool,
  createBoardTool,
  listBoardsTool,
  getBoardTool,
  createListTool,
} from './tools/project-tools.js';

import {
  createTaskTool,
  updateTaskTool,
  moveTaskTool,
  assignTaskTool,
  listTasksTool,
  deleteTaskTool,
  addCommentTool,
  getTaskTool,
} from './tools/task-tools.js';

// Initialize database
initializeDatabase();

// Create MCP server with all tools
export const pmTools = createSdkMcpServer({
  name: 'project-management-tools',
  version: '1.0.0',
  tools: [
    // User management tools
    createUserTool,
    listUsersTool,
    getUserTool,
    updateUserTool,
    deleteUserTool,

    // Project and board management tools
    createProjectTool,
    listProjectsTool,
    addProjectMemberTool,
    createBoardTool,
    listBoardsTool,
    getBoardTool,
    createListTool,

    // Task management tools
    createTaskTool,
    updateTaskTool,
    moveTaskTool,
    assignTaskTool,
    listTasksTool,
    deleteTaskTool,
    addCommentTool,
    getTaskTool,
  ],
});

export default pmTools;

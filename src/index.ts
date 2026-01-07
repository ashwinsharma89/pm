#!/usr/bin/env node

import { query } from '@anthropic-ai/claude-agent-sdk';
import { closeDatabase } from './database/schema.js';
import { pmTools } from './agent.js';
import * as readline from 'readline';

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

async function main() {
  console.log('🚀 Project Management Tool');
  console.log('==========================');
  console.log('Built with Claude Agent SDK\n');
  console.log('Type your requests in natural language, or type "exit" to quit.\n');

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    prompt: '> ',
  });

  rl.prompt();

  rl.on('line', async (line) => {
    const input = line.trim();

    if (!input) {
      rl.prompt();
      return;
    }

    if (input.toLowerCase() === 'exit' || input.toLowerCase() === 'quit') {
      console.log('\nGoodbye! 👋');
      closeDatabase();
      process.exit(0);
    }

    try {
      console.log('\nThinking...\n');

      // Get all tool names for allowed_tools
      const allToolNames = [
        'create_user', 'list_users', 'get_user', 'update_user', 'delete_user',
        'create_project', 'list_projects', 'add_project_member',
        'create_board', 'list_boards', 'get_board', 'create_list',
        'create_task', 'update_task', 'move_task', 'assign_task',
        'list_tasks', 'delete_task', 'add_comment', 'get_task'
      ];

      // Run the query with the user's input
      const q = query({
        prompt: `${SYSTEM_PROMPT}\n\nUser request: ${input}`,
        options: {
          model: 'claude-sonnet-4-5-20250929',
          cwd: process.cwd(),
          mcpServers: {
            'project-management-tools': pmTools,
          },
          allowedTools: allToolNames,
        },
      });

      // Stream and display messages
      let lastResponse = '';
      for await (const message of q) {
        if (message.type === 'assistant' && message.message.content) {
          for (const content of message.message.content) {
            if (content.type === 'text') {
              lastResponse = content.text;
            }
          }
        } else if (message.type === 'result') {
          // Display the final result
          if (lastResponse) {
            console.log('Agent:', lastResponse);
          }
        }
      }

      console.log();
    } catch (error: any) {
      console.error('Error:', error.message);
      console.log();
    }

    rl.prompt();
  });

  rl.on('close', () => {
    console.log('\nGoodbye! 👋');
    closeDatabase();
    process.exit(0);
  });

  // Handle process termination
  process.on('SIGINT', () => {
    console.log('\n\nShutting down...');
    closeDatabase();
    process.exit(0);
  });
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((error) => {
    console.error('Fatal error:', error);
    closeDatabase();
    process.exit(1);
  });
}

export { pmTools };

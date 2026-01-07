# Project Management Tool

A powerful, Trello-style project management tool built with the Claude Agent SDK. Designed for local teams of up to 30 users with natural language interface for managing projects, boards, tasks, and team collaboration.

**✨ NEW: Now available as a web application! Access via browser at http://localhost:3000**

## Features

- **🌐 Web Interface**: Modern, responsive web UI accessible via browser
- **💬 Natural Language Interface**: Interact with your PM tool using conversational language powered by Claude
- **🔌 REST API**: Full API for programmatic access and integrations
- **👥 User Management**: Create and manage team members with different roles (admin, manager, member)
- **📊 Project Organization**: Organize work into projects with multiple team members
- **📋 Trello-style Boards**: Create boards with customizable lists (To Do, In Progress, Done, etc.)
- **✅ Task Management**: Create, assign, prioritize, and track tasks through different stages
- **💬 Comments**: Add comments to tasks for discussion and updates
- **💾 Local SQLite Database**: All data stored locally for privacy and control
- **👨‍👩‍👧‍👦 Multi-user Support**: Designed for teams up to 30 users
- **⌨️ CLI Mode**: Optional command-line interface for terminal users

## Architecture

```
Projects
  └── Boards (e.g., "Sprint 1", "Marketing Campaign")
      └── Lists (e.g., "To Do", "In Progress", "Done")
          └── Tasks (with assignments, priorities, due dates)
              └── Comments
```

## Installation

### Prerequisites

- Node.js 18 or higher
- npm or yarn

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd pm
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your Anthropic API key
```

4. Build the project:
```bash
npm run build
```

5. Start the application:
```bash
npm start
```

## Usage

### Web Application (Recommended)

The easiest way to use the PM tool is via the web interface:

```bash
# Start the web server (production)
npm start

# Development mode (with hot reload)
npm run dev
```

Then open your browser to: **http://localhost:3000**

The web interface provides:
- Interactive dashboard with project statistics
- Chat interface for natural language commands
- Visual boards and task lists
- Real-time updates

### CLI Mode

For terminal users, a command-line interface is also available:

```bash
# Start CLI mode
npm run start:cli

# Development CLI mode
npm run dev:cli
```

### Example Conversations

You can interact with the PM tool using natural language (via web chat or CLI):

#### Setting Up

```
> Create a user named John Doe with username john and email john@example.com
> Create a project called "Website Redesign" owned by user ID 1
> Add user ID 2 to project ID 1
> Create a board called "Sprint 1" for project ID 1
```

#### Managing Tasks

```
> Create a task "Design homepage" in list ID 1, assign it to user 3, priority high
> Move task 5 to the "In Progress" list
> Show me all tasks assigned to user 3
> Update task 5 to have priority urgent and due date 2026-01-15
> Add a comment to task 5: "Updated the mockups in Figma"
```

#### Viewing Information

```
> List all projects
> Show me board 1 with all its tasks
> List all users with role manager
> Get details of task 5
> Show me all high priority tasks in board 1
```

## Available Tools

The agent has access to the following tools:

### User Management
- `create_user` - Create a new user
- `list_users` - List all users (with optional role filter)
- `get_user` - Get user details by ID or username
- `update_user` - Update user information
- `delete_user` - Delete a user

### Project & Board Management
- `create_project` - Create a new project
- `list_projects` - List projects (with filters)
- `add_project_member` - Add a user to a project
- `create_board` - Create a new board in a project
- `list_boards` - List all boards in a project
- `get_board` - Get detailed board view with lists and tasks
- `create_list` - Create a new list/column in a board

### Task Management
- `create_task` - Create a new task
- `update_task` - Update task details
- `move_task` - Move a task to a different list
- `assign_task` - Assign a task to a user
- `list_tasks` - List tasks with filters
- `delete_task` - Delete a task
- `get_task` - Get full task details with comments
- `add_comment` - Add a comment to a task

## REST API

The web server exposes a comprehensive REST API for programmatic access:

### Chat/Query Endpoint

**POST** `/api/chat`
```json
{
  "message": "Create a user named John Doe with email john@example.com"
}
```

Response:
```json
{
  "response": "User created successfully: John Doe (johndoe)",
  "toolCalls": [...],
  "success": true
}
```

### Direct Database Endpoints

#### Users
- **GET** `/api/users` - List all users
- **POST** `/api/users` - Create a user
  ```json
  {
    "username": "john",
    "full_name": "John Doe",
    "email": "john@example.com",
    "role": "member"
  }
  ```

#### Projects
- **GET** `/api/projects` - List all projects
- **POST** `/api/projects` - Create a project
  ```json
  {
    "name": "Website Redesign",
    "description": "Q1 2026 redesign project",
    "owner_id": 1
  }
  ```

#### Boards
- **GET** `/api/boards?project_id=1` - List boards (optionally filter by project)
- **GET** `/api/boards/:id` - Get board with lists and tasks
- **POST** `/api/boards` - Create a board
  ```json
  {
    "name": "Sprint 1",
    "project_id": 1,
    "description": "First sprint board"
  }
  ```

#### Tasks
- **GET** `/api/tasks?board_id=1&assignee_id=2` - List tasks with filters
- **POST** `/api/tasks` - Create a task
  ```json
  {
    "title": "Design homepage",
    "list_id": 1,
    "description": "Create mockups for new homepage",
    "creator_id": 1,
    "assignee_id": 2,
    "priority": "high",
    "due_date": "2026-02-01"
  }
  ```
- **PUT** `/api/tasks/:id` - Update a task
- **DELETE** `/api/tasks/:id` - Delete a task

## Database Schema

The tool uses SQLite with the following tables:

- **users** - Team members
- **projects** - Top-level project containers
- **project_members** - Many-to-many relationship for project access
- **boards** - Boards within projects
- **lists** - Columns/stages in boards
- **tasks** - Individual work items
- **comments** - Task discussions

## Development

### Project Structure

```
pm/
├── src/
│   ├── database/
│   │   ├── schema.ts       # Database initialization and schema
│   │   └── models.ts       # TypeScript type definitions
│   ├── tools/
│   │   ├── user-tools.ts   # User management tools
│   │   ├── project-tools.ts # Project and board tools
│   │   └── task-tools.ts   # Task management tools
│   ├── agent.ts            # MCP server configuration
│   ├── server.ts           # Web server (Express + REST API)
│   └── index.ts            # CLI interface
├── public/
│   └── index.html          # Web UI
├── package.json
├── tsconfig.json
├── .env.example
└── README.md
```

### Building

```bash
npm run build
```

### Cleaning

```bash
npm run clean  # Removes dist/ and database
```

## API Integration

This tool uses the Claude Agent SDK to provide natural language interaction. To use it:

1. Get an Anthropic API key from https://console.anthropic.com/
2. Add it to your `.env` file as `ANTHROPIC_API_KEY`
3. The agent will automatically use it to process your requests

## Use Cases

### For Managers
- Track team workload and task assignments
- Monitor project progress
- Organize sprints and releases
- Coordinate multi-project work

### For Team Members
- View assigned tasks
- Update task status
- Add comments and collaborate
- Track priorities and deadlines

### For Teams
- Collaborate on shared projects
- Transparent task tracking
- Flexible workflow (customize lists)
- Local data control

## Deployment & Scaling

### Local Network Deployment

The web server can be accessed by multiple users on your local network:

1. Start the server on a computer accessible to your team
2. Find the server's local IP address (e.g., `192.168.1.100`)
3. Team members access via `http://192.168.1.100:3000`

### Environment Variables for Production

```bash
# .env file
ANTHROPIC_API_KEY=your_actual_key_here
PORT=3000
SESSION_SECRET=your-secure-random-secret
DB_PATH=./pm.db
```

### Cloud Deployment

Deploy to platforms like:
- **Heroku**: `heroku create` → `git push heroku main`
- **Railway**: Connect your repo and deploy
- **DigitalOcean/AWS**: Run with PM2 or Docker
- **Vercel/Netlify**: For serverless deployment

### Scaling Beyond 30 Users

For larger teams or enterprise deployment:

- ✅ Migrate to PostgreSQL or MySQL for better concurrency
- ✅ Add authentication (OAuth, JWT, or session-based)
- ✅ Implement role-based access control (RBAC)
- ✅ Add WebSocket support for real-time updates
- ✅ Set up load balancing with multiple server instances
- ✅ Add caching layer (Redis) for better performance
- ✅ Implement rate limiting and security headers

## Troubleshooting

### Database locked error
If you get a "database is locked" error, ensure no other instances are running.

### API key errors
Make sure your `.env` file has a valid `ANTHROPIC_API_KEY`.

### Module errors
Ensure you're using Node.js 18+ and have run `npm install` and `npm run build`.

## License

ISC

## Contributing

This is a demonstration project built with the Claude Agent SDK. Feel free to fork and customize for your team's needs.

## Support

For issues with the Claude Agent SDK, visit: https://github.com/anthropics/claude-agent-sdk

// Type definitions for the database models

export interface User {
  id: number;
  username: string;
  full_name: string;
  email: string;
  role: 'admin' | 'manager' | 'member';
  created_at: string;
  updated_at: string;
}

export interface Project {
  id: number;
  name: string;
  description: string | null;
  owner_id: number;
  status: 'active' | 'archived' | 'completed';
  created_at: string;
  updated_at: string;
}

export interface Board {
  id: number;
  name: string;
  project_id: number;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export interface List {
  id: number;
  name: string;
  board_id: number;
  position: number;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: number;
  title: string;
  description: string | null;
  list_id: number;
  position: number;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  due_date: string | null;
  assignee_id: number | null;
  creator_id: number;
  created_at: string;
  updated_at: string;
}

export interface Comment {
  id: number;
  task_id: number;
  user_id: number;
  content: string;
  created_at: string;
}

export interface ProjectMember {
  project_id: number;
  user_id: number;
  role: 'owner' | 'admin' | 'member';
  joined_at: string;
}

// Extended types with joined data
export interface TaskWithDetails extends Task {
  assignee_name?: string;
  creator_name?: string;
  list_name?: string;
}

export interface BoardWithLists extends Board {
  lists: List[];
}

export interface ProjectWithMembers extends Project {
  members: User[];
}

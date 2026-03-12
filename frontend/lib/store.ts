import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: string;
  email: string;
  username: string;
  full_name?: string;
  role: string;
  is_active: boolean;
}

interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  setAuth: (user: User, accessToken: string, refreshToken: string) => void;
  logout: () => void;
  updateUser: (user: Partial<User>) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
      setAuth: (user, accessToken, refreshToken) =>
        set({ user, accessToken, refreshToken, isAuthenticated: true }),
      logout: () =>
        set({ user: null, accessToken: null, refreshToken: null, isAuthenticated: false }),
      updateUser: (userData) =>
        set((state) => ({
          user: state.user ? { ...state.user, ...userData } : null,
        })),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);

interface Task {
  id: string;
  name: string;
  description?: string;
  input_data?: object;
  output_data?: object;
  status: string;
  error_message?: string;
  created_at: string;
  updated_at: string;
  completed_at?: string;
}

interface Workflow {
  id: string;
  name: string;
  description?: string;
  definition?: object;
  status: string;
  schedule?: string;
  created_at: string;
  updated_at: string;
}

interface Execution {
  id: string;
  input_data?: object;
  output_data?: object;
  logs?: object;
  status: string;
  error_message?: string;
  duration_ms?: number;
  created_at: string;
  completed_at?: string;
}

interface DashboardState {
  tasks: Task[];
  workflows: Workflow[];
  executions: Execution[];
  recentExecutions: Execution[];
  setTasks: (tasks: Task[]) => void;
  setWorkflows: (workflows: Workflow[]) => void;
  setExecutions: (executions: Execution[]) => void;
  addTask: (task: Task) => void;
  addWorkflow: (workflow: Workflow) => void;
  addExecution: (execution: Execution) => void;
  updateTask: (id: string, task: Partial<Task>) => void;
  updateWorkflow: (id: string, workflow: Partial<Workflow>) => void;
  updateExecution: (id: string, execution: Partial<Execution>) => void;
  removeTask: (id: string) => void;
  removeWorkflow: (id: string) => void;
}

export const useDashboardStore = create<DashboardState>((set) => ({
  tasks: [],
  workflows: [],
  executions: [],
  recentExecutions: [],
  setTasks: (tasks) => set({ tasks }),
  setWorkflows: (workflows) => set({ workflows }),
  setExecutions: (executions) => set({ executions, recentExecutions: executions.slice(0, 10) }),
  addTask: (task) => set((state) => ({ tasks: [task, ...state.tasks] })),
  addWorkflow: (workflow) => set((state) => ({ workflows: [workflow, ...state.workflows] })),
  addExecution: (execution) =>
    set((state) => ({
      executions: [execution, ...state.executions],
      recentExecutions: [execution, ...state.recentExecutions].slice(0, 10),
    })),
  updateTask: (id, task) =>
    set((state) => ({
      tasks: state.tasks.map((t) => (t.id === id ? { ...t, ...task } : t)),
    })),
  updateWorkflow: (id, workflow) =>
    set((state) => ({
      workflows: state.workflows.map((w) => (w.id === id ? { ...w, ...workflow } : w)),
    })),
  updateExecution: (id, execution) =>
    set((state) => ({
      executions: state.executions.map((e) => (e.id === id ? { ...e, ...execution } : e)),
    })),
  removeTask: (id) =>
    set((state) => ({
      tasks: state.tasks.filter((t) => t.id !== id),
    })),
  removeWorkflow: (id) =>
    set((state) => ({
      workflows: state.workflows.filter((w) => w.id !== id),
    })),
}));

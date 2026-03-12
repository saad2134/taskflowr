const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '/api';

interface RequestOptions extends RequestInit {
  skipAuth?: boolean;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private getToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('access_token');
  }

  private async request<T>(
    endpoint: string,
    options: RequestOptions = {}
  ): Promise<T> {
    const { skipAuth = false, ...fetchOptions } = options;
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    };

    if (!skipAuth) {
      const token = this.getToken();
      if (token) {
        (headers as Record<string, string>)['Authorization'] = `Bearer ${token}`;
      }
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...fetchOptions,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
      throw new Error(error.detail || 'Request failed');
    }

    if (response.status === 204) {
      return {} as T;
    }

    return response.json();
  }

  async get<T>(endpoint: string, options?: RequestOptions): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'GET' });
  }

  async post<T>(endpoint: string, data?: unknown, options?: RequestOptions): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async put<T>(endpoint: string, data?: unknown, options?: RequestOptions): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async delete<T>(endpoint: string, options?: RequestOptions): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'DELETE' });
  }
}

export const api = new ApiClient(API_BASE_URL);

export const authApi = {
  register: (data: { email: string; username: string; password: string; full_name?: string }) =>
    api.post('/auth/register', data, { skipAuth: true }),
  
  login: (data: { username: string; password: string }) =>
    api.post('/auth/login', data, { skipAuth: true }),
  
  refresh: (refreshToken: string) =>
    api.post('/auth/refresh', refreshToken, { skipAuth: true }),
  
  me: () => api.get('/auth/me'),
  
  update: (data: { full_name?: string; email?: string }) =>
    api.put('/auth/me', data),
};

export const tasksApi = {
  list: (params?: { skip?: number; limit?: number; status_filter?: string }) => {
    const searchParams = new URLSearchParams();
    if (params?.skip) searchParams.set('skip', String(params.skip));
    if (params?.limit) searchParams.set('limit', String(params.limit));
    if (params?.status_filter) searchParams.set('status_filter', params.status_filter);
    const query = searchParams.toString();
    return api.get(`/tasks${query ? `?${query}` : ''}`);
  },
  
  get: (id: string) => api.get(`/tasks/${id}`),
  
  create: (data: { name: string; description?: string; input_data?: object }) =>
    api.post('/tasks', data),
  
  update: (id: string, data: { name?: string; description?: string; input_data?: object }) =>
    api.put(`/tasks/${id}`, data),
  
  delete: (id: string) => api.delete(`/tasks/${id}`),
  
  execute: (id: string, data: { input_data: object }) =>
    api.post(`/tasks/${id}/execute`, data),
  
  executeDirect: (data: { input_data: object }) =>
    api.post('/tasks/execute', data),
};

export const workflowsApi = {
  list: (params?: { skip?: number; limit?: number; status_filter?: string }) => {
    const searchParams = new URLSearchParams();
    if (params?.skip) searchParams.set('skip', String(params.skip));
    if (params?.limit) searchParams.set('limit', String(params.limit));
    if (params?.status_filter) searchParams.set('status_filter', params.status_filter);
    const query = searchParams.toString();
    return api.get(`/workflows${query ? `?${query}` : ''}`);
  },
  
  get: (id: string) => api.get(`/workflows/${id}`),
  
  create: (data: { name: string; description?: string; definition?: object; schedule?: string }) =>
    api.post('/workflows', data),
  
  update: (id: string, data: object) => api.put(`/workflows/${id}`, data),
  
  delete: (id: string) => api.delete(`/workflows/${id}`),
  
  execute: (id: string, data: { input_data: object }) =>
    api.post(`/workflows/${id}/execute`, data),
  
  activate: (id: string) => api.post(`/workflows/${id}/activate`),
  
  pause: (id: string) => api.post(`/workflows/${id}/pause`),
};

export const executionsApi = {
  list: (params?: { skip?: number; limit?: number; status_filter?: string; task_id?: string; workflow_id?: string }) => {
    const searchParams = new URLSearchParams();
    if (params?.skip) searchParams.set('skip', String(params.skip));
    if (params?.limit) searchParams.set('limit', String(params.limit));
    if (params?.status_filter) searchParams.set('status_filter', params.status_filter);
    if (params?.task_id) searchParams.set('task_id', params.task_id);
    if (params?.workflow_id) searchParams.set('workflow_id', params.workflow_id);
    const query = searchParams.toString();
    return api.get(`/executions${query ? `?${query}` : ''}`);
  },
  
  get: (id: string) => api.get(`/executions/${id}`),
  
  cancel: (id: string) => api.post(`/executions/${id}/cancel`),
  
  logs: (id: string) => api.get(`/executions/${id}/logs`),
};

export const connectorsApi = {
  list: () => api.get('/connectors'),
  
  get: (id: string) => api.get(`/connectors/${id}`),
  
  create: (data: { name: string; connector_type: string; config?: object; credentials: object }) =>
    api.post('/connectors', data),
  
  update: (id: string, data: object) => api.put(`/connectors/${id}`, data),
  
  delete: (id: string) => api.delete(`/connectors/${id}`),
  
  test: (data: { connector_type: string; credentials: object }) =>
    api.post('/connectors/test', data),
};

export const webhooksApi = {
  list: () => api.get('/webhooks'),
  
  create: (data: { url: string; events: string[]; secret?: string }) =>
    api.post('/webhooks', data),
  
  delete: (id: string) => api.delete(`/webhooks/${id}`),
};

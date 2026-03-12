'use client';

import { useEffect, useState } from 'react';
import { tasksApi } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Plus, Play, Trash2, Clock, CheckCircle, XCircle, Loader } from 'lucide-react';

interface Task {
  id: string;
  name: string;
  description?: string;
  status: string;
  created_at: string;
  completed_at?: string;
}

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [newTask, setNewTask] = useState({ name: '', description: '', instruction: '' });
  const [executing, setExecuting] = useState<string | null>(null);

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      const data = await tasksApi.list({ limit: 50 });
      setTasks(data as Task[]);
    } catch (error) {
      console.error('Failed to load tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    try {
      await tasksApi.create({
        name: newTask.name,
        description: newTask.description,
        input_data: { instruction: newTask.instruction },
      });
      setNewTask({ name: '', description: '', instruction: '' });
      setShowCreate(false);
      loadTasks();
    } catch (error) {
      console.error('Failed to create task:', error);
    }
  };

  const handleExecute = async (taskId: string) => {
    setExecuting(taskId);
    try {
      await tasksApi.execute(taskId, { input_data: {} });
      loadTasks();
    } catch (error) {
      console.error('Failed to execute task:', error);
    } finally {
      setExecuting(null);
    }
  };

  const handleDelete = async (taskId: string) => {
    try {
      await tasksApi.delete(taskId);
      loadTasks();
    } catch (error) {
      console.error('Failed to delete task:', error);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'failed':
        return <XCircle className="h-4 w-4 text-red-500" />;
      case 'running':
        return <Loader className="h-4 w-4 text-blue-500 animate-spin" />;
      default:
        return <Clock className="h-4 w-4 text-gray-400" />;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Tasks</h1>
          <p className="text-gray-500 mt-1">Manage and execute your tasks</p>
        </div>
        <Button onClick={() => setShowCreate(!showCreate)}>
          <Plus className="h-4 w-4 mr-2" />
          New Task
        </Button>
      </div>

      {showCreate && (
        <Card>
          <CardHeader>
            <CardTitle>Create New Task</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Input
              placeholder="Task name"
              value={newTask.name}
              onChange={(e) => setNewTask({ ...newTask, name: e.target.value })}
            />
            <Input
              placeholder="Description"
              value={newTask.description}
              onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
            />
            <Input
              placeholder="Instruction (e.g., 'Generate a sales report')"
              value={newTask.instruction}
              onChange={(e) => setNewTask({ ...newTask, instruction: e.target.value })}
            />
            <div className="flex gap-2">
              <Button onClick={handleCreate}>Create Task</Button>
              <Button variant="outline" onClick={() => setShowCreate(false)}>Cancel</Button>
            </div>
          </CardContent>
        </Card>
      )}

      {loading ? (
        <div className="text-center py-8">Loading...</div>
      ) : tasks.length === 0 ? (
        <div className="text-center py-8 text-gray-500">No tasks yet. Create one to get started.</div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {tasks.map((task) => (
            <Card key={task.id}>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-base font-medium">{task.name}</CardTitle>
                {getStatusIcon(task.status)}
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-500 mb-4">{task.description || 'No description'}</p>
                <div className="flex gap-2">
                  <Button
                    size="sm"
                    onClick={() => handleExecute(task.id)}
                    disabled={executing === task.id || task.status === 'running'}
                  >
                    <Play className="h-4 w-4 mr-1" />
                    {executing === task.id ? 'Running...' : 'Run'}
                  </Button>
                  <Button size="sm" variant="destructive" onClick={() => handleDelete(task.id)}>
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}

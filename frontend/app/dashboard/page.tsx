'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { tasksApi, workflowsApi, executionsApi } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ListTodo, GitBranch, PlayCircle, Plus, ArrowRight } from 'lucide-react';

interface Stats {
  tasks: { total: number; pending: number; completed: number; failed: number };
  workflows: { total: number; active: number; draft: number };
  executions: { total: number; running: number; completed: number; failed: number };
}

export default function DashboardPage() {
  const [stats, setStats] = useState<Stats>({
    tasks: { total: 0, pending: 0, completed: 0, failed: 0 },
    workflows: { total: 0, active: 0, draft: 0 },
    executions: { total: 0, running: 0, completed: 0, failed: 0 },
  });
  const [loading, setLoading] = useState(true);
  const [instruction, setInstruction] = useState('');
  const [executing, setExecuting] = useState(false);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const [tasks, workflows, executions] = await Promise.all([
        tasksApi.list({ limit: 100 }),
        workflowsApi.list({ limit: 100 }),
        executionsApi.list({ limit: 100 }),
      ]);

      const taskList = tasks as any[];
      const workflowList = workflows as any[];
      const executionList = executions as any[];

      setStats({
        tasks: {
          total: taskList.length,
          pending: taskList.filter((t: any) => t.status === 'pending').length,
          completed: taskList.filter((t: any) => t.status === 'completed').length,
          failed: taskList.filter((t: any) => t.status === 'failed').length,
        },
        workflows: {
          total: workflowList.length,
          active: workflowList.filter((w: any) => w.status === 'active').length,
          draft: workflowList.filter((w: any) => w.status === 'draft').length,
        },
        executions: {
          total: executionList.length,
          running: executionList.filter((e: any) => e.status === 'running').length,
          completed: executionList.filter((e: any) => e.status === 'completed').length,
          failed: executionList.filter((e: any) => e.status === 'failed').length,
        },
      });
    } catch (error) {
      console.error('Failed to load stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExecute = async () => {
    if (!instruction.trim()) return;
    setExecuting(true);
    try {
      await tasksApi.executeDirect({ input_data: { instruction } });
      setInstruction('');
      loadStats();
    } catch (error) {
      console.error('Failed to execute:', error);
    } finally {
      setExecuting(false);
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-gray-500 mt-1">Manage your AI-powered workflows</p>
      </div>

      <Card className="border-blue-200 bg-gradient-to-r from-blue-50 to-indigo-50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <PlayCircle className="h-5 w-5 text-blue-600" />
            Quick Execute
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-3">
            <input
              type="text"
              value={instruction}
              onChange={(e) => setInstruction(e.target.value)}
              placeholder="Enter your instruction (e.g., 'Generate a sales report for Q4')"
              className="flex-1 h-12 px-4 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
              onKeyDown={(e) => e.key === 'Enter' && handleExecute()}
            />
            <Button
              onClick={handleExecute}
              disabled={executing || !instruction.trim()}
              className="h-12 px-6"
            >
              {executing ? 'Executing...' : 'Execute'}
            </Button>
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-6 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-gray-500">Total Tasks</CardTitle>
            <ListTodo className="h-4 w-4 text-gray-500" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{stats.tasks.total}</div>
            <p className="text-xs text-gray-500 mt-1">
              {stats.tasks.completed} completed, {stats.tasks.pending} pending
            </p>
            <Link href="/dashboard/tasks">
              <Button variant="ghost" size="sm" className="mt-3 h-8 px-0">
                View tasks <ArrowRight className="h-4 w-4 ml-1" />
              </Button>
            </Link>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-gray-500">Workflows</CardTitle>
            <GitBranch className="h-4 w-4 text-gray-500" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{stats.workflows.total}</div>
            <p className="text-xs text-gray-500 mt-1">
              {stats.workflows.active} active, {stats.workflows.draft} drafts
            </p>
            <Link href="/dashboard/workflows">
              <Button variant="ghost" size="sm" className="mt-3 h-8 px-0">
                View workflows <ArrowRight className="h-4 w-4 ml-1" />
              </Button>
            </Link>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-gray-500">Total Executions</CardTitle>
            <PlayCircle className="h-4 w-4 text-gray-500" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{stats.executions.total}</div>
            <p className="text-xs text-gray-500 mt-1">
              {stats.executions.completed} completed, {stats.executions.running} running
            </p>
            <Link href="/dashboard/executions">
              <Button variant="ghost" size="sm" className="mt-3 h-8 px-0">
                View executions <ArrowRight className="h-4 w-4 ml-1" />
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

'use client';

import { useEffect, useState } from 'react';
import { workflowsApi } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Plus, Play, Trash2, Pause, CheckCircle, XCircle, Clock, Loader } from 'lucide-react';

interface Workflow {
  id: string;
  name: string;
  description?: string;
  status: string;
  created_at: string;
}

export default function WorkflowsPage() {
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [newWorkflow, setNewWorkflow] = useState({ name: '', description: '', schedule: '' });
  const [executing, setExecuting] = useState<string | null>(null);

  useEffect(() => {
    loadWorkflows();
  }, []);

  const loadWorkflows = async () => {
    try {
      const data = await workflowsApi.list({ limit: 50 });
      setWorkflows(data as Workflow[]);
    } catch (error) {
      console.error('Failed to load workflows:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    try {
      await workflowsApi.create({
        name: newWorkflow.name,
        description: newWorkflow.description,
        schedule: newWorkflow.schedule || undefined,
      });
      setNewWorkflow({ name: '', description: '', schedule: '' });
      setShowCreate(false);
      loadWorkflows();
    } catch (error) {
      console.error('Failed to create workflow:', error);
    }
  };

  const handleExecute = async (workflowId: string) => {
    setExecuting(workflowId);
    try {
      await workflowsApi.execute(workflowId, { input_data: {} });
      loadWorkflows();
    } catch (error) {
      console.error('Failed to execute workflow:', error);
    } finally {
      setExecuting(null);
    }
  };

  const handleActivate = async (workflowId: string) => {
    try {
      await workflowsApi.activate(workflowId);
      loadWorkflows();
    } catch (error) {
      console.error('Failed to activate workflow:', error);
    }
  };

  const handlePause = async (workflowId: string) => {
    try {
      await workflowsApi.pause(workflowId);
      loadWorkflows();
    } catch (error) {
      console.error('Failed to pause workflow:', error);
    }
  };

  const handleDelete = async (workflowId: string) => {
    try {
      await workflowsApi.delete(workflowId);
      loadWorkflows();
    } catch (error) {
      console.error('Failed to delete workflow:', error);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'paused':
        return <Pause className="h-4 w-4 text-yellow-500" />;
      case 'draft':
        return <Clock className="h-4 w-4 text-gray-400" />;
      default:
        return <Clock className="h-4 w-4 text-gray-400" />;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Workflows</h1>
          <p className="text-gray-500 mt-1">Manage automated workflows</p>
        </div>
        <Button onClick={() => setShowCreate(!showCreate)}>
          <Plus className="h-4 w-4 mr-2" />
          New Workflow
        </Button>
      </div>

      {showCreate && (
        <Card>
          <CardHeader>
            <CardTitle>Create New Workflow</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Input
              placeholder="Workflow name"
              value={newWorkflow.name}
              onChange={(e) => setNewWorkflow({ ...newWorkflow, name: e.target.value })}
            />
            <Input
              placeholder="Description"
              value={newWorkflow.description}
              onChange={(e) => setNewWorkflow({ ...newWorkflow, description: e.target.value })}
            />
            <Input
              placeholder="Schedule (cron expression, optional)"
              value={newWorkflow.schedule}
              onChange={(e) => setNewWorkflow({ ...newWorkflow, schedule: e.target.value })}
            />
            <div className="flex gap-2">
              <Button onClick={handleCreate}>Create Workflow</Button>
              <Button variant="outline" onClick={() => setShowCreate(false)}>Cancel</Button>
            </div>
          </CardContent>
        </Card>
      )}

      {loading ? (
        <div className="text-center py-8">Loading...</div>
      ) : workflows.length === 0 ? (
        <div className="text-center py-8 text-gray-500">No workflows yet. Create one to get started.</div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {workflows.map((workflow) => (
            <Card key={workflow.id}>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-base font-medium">{workflow.name}</CardTitle>
                {getStatusIcon(workflow.status)}
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-500 mb-4">{workflow.description || 'No description'}</p>
                <div className="flex gap-2 flex-wrap">
                  <Button
                    size="sm"
                    onClick={() => handleExecute(workflow.id)}
                    disabled={executing === workflow.id || workflow.status !== 'active'}
                  >
                    <Play className="h-4 w-4 mr-1" />
                    {executing === workflow.id ? 'Running...' : 'Run'}
                  </Button>
                  {workflow.status === 'draft' && (
                    <Button size="sm" variant="secondary" onClick={() => handleActivate(workflow.id)}>
                      Activate
                    </Button>
                  )}
                  {workflow.status === 'active' && (
                    <Button size="sm" variant="secondary" onClick={() => handlePause(workflow.id)}>
                      Pause
                    </Button>
                  )}
                  <Button size="sm" variant="destructive" onClick={() => handleDelete(workflow.id)}>
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

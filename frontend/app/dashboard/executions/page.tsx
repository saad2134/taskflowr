'use client';

import { useEffect, useState } from 'react';
import { executionsApi } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Plus, Play, Trash2, CheckCircle, XCircle, Clock, Loader } from 'lucide-react';

interface Execution {
  id: string;
  status: string;
  input_data?: object;
  output_data?: object;
  error_message?: string;
  duration_ms?: number;
  created_at: string;
  completed_at?: string;
}

export default function ExecutionsPage() {
  const [executions, setExecutions] = useState<Execution[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedExecution, setSelectedExecution] = useState<Execution | null>(null);

  useEffect(() => {
    loadExecutions();
  }, []);

  const loadExecutions = async () => {
    try {
      const data = await executionsApi.list({ limit: 50 });
      const response = data as { executions: Execution[] };
      setExecutions(response.executions || []);
    } catch (error) {
      console.error('Failed to load executions:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = async (executionId: string) => {
    try {
      await executionsApi.cancel(executionId);
      loadExecutions();
    } catch (error) {
      console.error('Failed to cancel execution:', error);
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
      case 'cancelled':
        return <XCircle className="h-4 w-4 text-yellow-500" />;
      default:
        return <Clock className="h-4 w-4 text-gray-400" />;
    }
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleString();
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Executions</h1>
          <p className="text-gray-500 mt-1">View execution history</p>
        </div>
        <Button onClick={loadExecutions}>Refresh</Button>
      </div>

      {loading ? (
        <div className="text-center py-8">Loading...</div>
      ) : executions.length === 0 ? (
        <div className="text-center py-8 text-gray-500">No executions yet.</div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {executions.map((execution) => (
            <Card 
              key={execution.id} 
              className="cursor-pointer hover:shadow-md transition-shadow"
              onClick={() => setSelectedExecution(execution)}
            >
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-base font-mono text-xs">ID: {execution.id.slice(0, 8)}</CardTitle>
                {getStatusIcon(execution.status)}
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Status:</span>
                    <span className="font-medium capitalize">{execution.status}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Duration:</span>
                    <span className="font-medium">{execution.duration_ms ? `${execution.duration_ms}ms` : '-'}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Started:</span>
                    <span className="font-medium">{formatDate(execution.created_at)}</span>
                  </div>
                  {execution.status === 'running' && (
                    <Button 
                      size="sm" 
                      variant="destructive" 
                      className="w-full mt-2"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleCancel(execution.id);
                      }}
                    >
                      Cancel
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {selectedExecution && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" onClick={() => setSelectedExecution(null)}>
          <Card className="w-full max-w-2max-h-[80vh] overflow-auto" onClick={(e) => e.stopPropagation()}>
            <CardHeader>
              <CardTitle>Execution Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h4 className="font-medium mb-2">Status</h4>
                <div className="flex items-center gap-2">
                  {getStatusIcon(selectedExecution.status)}
                  <span className="capitalize">{selectedExecution.status}</span>
                </div>
              </div>
              <div>
                <h4 className="font-medium mb-2">Input</h4>
                <pre className="bg-gray-100 p-3 rounded-lg text-sm overflow-auto max-h-40">
                  {JSON.stringify(selectedExecution.input_data, null, 2)}
                </pre>
              </div>
              {selectedExecution.output_data && (
                <div>
                  <h4 className="font-medium mb-2">Output</h4>
                  <pre className="bg-gray-100 p-3 rounded-lg text-sm overflow-auto max-h-40">
                    {JSON.stringify(selectedExecution.output_data, null, 2)}
                  </pre>
                </div>
              )}
              {selectedExecution.error_message && (
                <div>
                  <h4 className="font-medium mb-2 text-red-600">Error</h4>
                  <pre className="bg-red-50 p-3 rounded-lg text-sm text-red-800">
                    {selectedExecution.error_message}
                  </pre>
                </div>
              )}
              <Button variant="outline" onClick={() => setSelectedExecution(null)}>Close</Button>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}

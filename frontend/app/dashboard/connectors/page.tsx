'use client';

import { useEffect, useState } from 'react';
import { connectorsApi, webhooksApi } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Plus, Trash2, CheckCircle, XCircle, Plug } from 'lucide-react';

interface Connector {
  id: string;
  name: string;
  connector_type: string;
  is_active: boolean;
  created_at: string;
}

interface Webhook {
  id: string;
  url: string;
  events: string[];
  is_active: boolean;
  created_at: string;
}

export default function ConnectorsPage() {
  const [connectors, setConnectors] = useState<Connector[]>([]);
  const [webhooks, setWebhooks] = useState<Webhook[]>([]);
  const [loading, setLoading] = useState(true);
  const [showConnectorForm, setShowConnectorForm] = useState(false);
  const [showWebhookForm, setShowWebhookForm] = useState(false);
  const [newConnector, setNewConnector] = useState({ name: '', connector_type: 'slack', webhook_url: '' });
  const [newWebhook, setNewWebhook] = useState({ url: '', events: [] as string[] });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [connectorData, webhookData] = await Promise.all([
        connectorsApi.list(),
        webhooksApi.list(),
      ]);
      setConnectors(connectorData as Connector[]);
      setWebhooks(webhookData as Webhook[]);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateConnector = async () => {
    try {
      const credentials = newConnector.connector_type === 'webhook' 
        ? { webhook_url: newConnector.webhook_url }
        : {};
      await connectorsApi.create({
        name: newConnector.name,
        connector_type: newConnector.connector_type,
        credentials,
      });
      setNewConnector({ name: '', connector_type: 'slack', webhook_url: '' });
      setShowConnectorForm(false);
      loadData();
    } catch (error) {
      console.error('Failed to create connector:', error);
    }
  };

  const handleCreateWebhook = async () => {
    try {
      await webhooksApi.create({
        url: newWebhook.url,
        events: newWebhook.events,
      });
      setNewWebhook({ url: '', events: [] });
      setShowWebhookForm(false);
      loadData();
    } catch (error) {
      console.error('Failed to create webhook:', error);
    }
  };

  const handleDeleteConnector = async (id: string) => {
    try {
      await connectorsApi.delete(id);
      loadData();
    } catch (error) {
      console.error('Failed to delete connector:', error);
    }
  };

  const handleDeleteWebhook = async (id: string) => {
    try {
      await webhooksApi.delete(id);
      loadData();
    } catch (error) {
      console.error('Failed to delete webhook:', error);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Connectors</h1>
        <p className="text-gray-500 mt-1">Manage external integrations</p>
      </div>

      <Tabs defaultValue="connectors">
        <TabsList>
          <TabsTrigger value="connectors">Connectors</TabsTrigger>
          <TabsTrigger value="webhooks">Webhooks</TabsTrigger>
        </TabsList>

        <TabsContent value="connectors" className="space-y-4">
          <Button onClick={() => setShowConnectorForm(!showConnectorForm)}>
            <Plus className="h-4 w-4 mr-2" />
            Add Connector
          </Button>

          {showConnectorForm && (
            <Card>
              <CardHeader>
                <CardTitle>New Connector</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <Input
                  placeholder="Connector name"
                  value={newConnector.name}
                  onChange={(e) => setNewConnector({ ...newConnector, name: e.target.value })}
                />
                <select
                  className="w-full h-10 px-3 rounded-md border border-input bg-background"
                  value={newConnector.connector_type}
                  onChange={(e) => setNewConnector({ ...newConnector, connector_type: e.target.value })}
                >
                  <option value="slack">Slack</option>
                  <option value="gmail">Gmail</option>
                  <option value="teams">Microsoft Teams</option>
                  <option value="webhook">Custom Webhook</option>
                </select>
                {newConnector.connector_type === 'webhook' && (
                  <Input
                    placeholder="Webhook URL"
                    value={newConnector.webhook_url}
                    onChange={(e) => setNewConnector({ ...newConnector, webhook_url: e.target.value })}
                  />
                )}
                <div className="flex gap-2">
                  <Button onClick={handleCreateConnector}>Create</Button>
                  <Button variant="outline" onClick={() => setShowConnectorForm(false)}>Cancel</Button>
                </div>
              </CardContent>
            </Card>
          )}

          {loading ? (
            <div className="text-center py-8">Loading...</div>
          ) : connectors.length === 0 ? (
            <div className="text-center py-8 text-gray-500">No connectors yet.</div>
          ) : (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {connectors.map((connector) => (
                <Card key={connector.id}>
                  <CardHeader className="flex flex-row items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Plug className="h-5 w-5" />
                      <CardTitle className="text-base">{connector.name}</CardTitle>
                    </div>
                    {connector.is_active ? (
                      <CheckCircle className="h-4 w-4 text-green-500" />
                    ) : (
                      <XCircle className="h-4 w-4 text-gray-400" />
                    )}
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-gray-500 mb-4 capitalize">{connector.connector_type}</p>
                    <Button size="sm" variant="destructive" onClick={() => handleDeleteConnector(connector.id)}>
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </TabsContent>

        <TabsContent value="webhooks" className="space-y-4">
          <Button onClick={() => setShowWebhookForm(!showWebhookForm)}>
            <Plus className="h-4 w-4 mr-2" />
            Add Webhook
          </Button>

          {showWebhookForm && (
            <Card>
              <CardHeader>
                <CardTitle>New Webhook</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <Input
                  placeholder="Webhook URL"
                  value={newWebhook.url}
                  onChange={(e) => setNewWebhook({ ...newWebhook, url: e.target.value })}
                />
                <div className="flex gap-2">
                  <Button onClick={handleCreateWebhook}>Create</Button>
                  <Button variant="outline" onClick={() => setShowWebhookForm(false)}>Cancel</Button>
                </div>
              </CardContent>
            </Card>
          )}

          {loading ? (
            <div className="text-center py-8">Loading...</div>
          ) : webhooks.length === 0 ? (
            <div className="text-center py-8 text-gray-500">No webhooks yet.</div>
          ) : (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {webhooks.map((webhook) => (
                <Card key={webhook.id}>
                  <CardHeader className="flex flex-row items-center justify-between">
                    <CardTitle className="text-base">Webhook</CardTitle>
                    {webhook.is_active ? (
                      <CheckCircle className="h-4 w-4 text-green-500" />
                    ) : (
                      <XCircle className="h-4 w-4 text-gray-400" />
                    )}
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-gray-500 mb-2 break-all">{webhook.url}</p>
                    <Button size="sm" variant="destructive" onClick={() => handleDeleteWebhook(webhook.id)}>
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}

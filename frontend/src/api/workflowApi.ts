// src/api/workflowApi.ts
import http from './http';

export type NodeType =
    | 'data_source'
    | 'train'
    | 'register'
    | 'deploy';

export interface WorkflowNode {
    id: string;
    type: NodeType;
    name: string;
    params: Record<string, any>;
    upstream_ids: string[];
}

export interface WorkflowDefinition {
    name: string;
    description?: string;
    nodes: WorkflowNode[];
}

export const runWorkflow = (workflowId: string, wf: WorkflowDefinition) =>
    http.post(`/workflows/${workflowId}/run`, wf).then((res) => res.data);

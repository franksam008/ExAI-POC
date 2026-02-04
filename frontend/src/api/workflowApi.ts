// src/api/workflowApi.ts
import http from './http';

export const listWorkflows = () =>
    http.get('/workflows').then(r => r.data);

export const getWorkflow = (id: string) =>
    http.get(`/workflows/${id}`).then(r => r.data);

export const createWorkflow = (payload: any) =>
    http.post('/workflows', payload).then(r => r.data);

export const updateWorkflow = (id: string, payload: any) =>
    http.put(`/workflows/${id}`, payload).then(r => r.data);

export const deleteWorkflow = (id: string) =>
    http.delete(`/workflows/${id}`).then(r => r.data);

export const runWorkflow = (id: string) =>
    http.post(`/workflows/${id}/run`).then(r => r.data);

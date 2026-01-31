import http from './http';

export const listWorkflowTemplates = () =>
    http.get('/workflow-templates').then(res => res.data);

export const getWorkflowTemplate = (id: string) =>
    http.get(`/workflow-templates/${id}`).then(res => res.data);

export const createWorkflowTemplate = (payload: any) =>
    http.post('/workflow-templates', payload).then(res => res.data);

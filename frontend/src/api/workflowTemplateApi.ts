import http from './http';

export const listWorkflowTemplates = (category?: string) =>
    http.get(`/workflow-templates`, {
        params: category ? { category } : {}
    }).then(res => res.data);

export const getWorkflowTemplate = (id: string) =>
    http.get(`/workflow-templates/${id}`).then(res => res.data);

export const createWorkflowTemplate = (payload: any) =>
    http.post('/workflow-templates', payload).then(res => res.data);

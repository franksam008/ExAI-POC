// src/api/modelApi.ts
import http from './http';

export const trainModel = (payload: any) =>
    http.post('/models/train', payload).then((res) => res.data);

// POC：模型列表暂时从后端聚合 MLflow
export const listModels = () =>
    http.get('/models').then((res) => res.data);

export const getModelMetrics = (name: string, version: string) =>
    http.get(`/monitor/models/${name}/${version}`).then(res => res.data);
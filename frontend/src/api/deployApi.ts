// src/api/deployApi.ts
import http from './http';

export interface ServiceItem {
    id: string;
    name: string;
    model_name: string;
    model_version: number;
    endpoint: string;
    status: string;
}

export const listServices = () =>
    http.get<ServiceItem[]>('/services').then((res) => res.data);

export const predict = (serviceId: string, features: Record<string, any>) =>
    http.post(`/services/predict/${serviceId}`, { features }).then((res) => res.data);

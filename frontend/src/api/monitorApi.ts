// src/api/monitorApi.ts
import http from './http';

export interface MetricPoint {
    timestamp: string;
    qps: number;
    latency_ms: number;
    error_rate: number;
}

export const getServiceMetrics = (serviceId: string) =>
    http.get<MetricPoint[]>(`/monitor/services/${serviceId}/metrics`).then((res) => res.data);

// src/api/systemApi.ts
import http from './http';

export const listUsers = () =>
    http.get('/system/users').then((res) => res.data);

export const listAuditLogs = () =>
    http.get('/system/audit-logs').then((res) => res.data);

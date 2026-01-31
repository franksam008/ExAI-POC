// src/api/registryApi.ts
import http from './http';

export const registerModel = (payload: {
    name: string;
    artifact_uri: string;
    description?: string;
}) => http.post('/registry/register', payload).then((res) => res.data);

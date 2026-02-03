// src/api/dataApi.ts
import http from './http';

export interface DataSource {
    id: string;
    name: string;
    type: string;
    config: string;
}

export interface Dataset {
    id: string;
    name: string;
    source_id: string;
    table_name: string;
    description?: string;
}

export const listDataSources = (): Promise<DataSource[]> =>
    http.get('/data/sources').then((res) => res.data);

export const createDataSource = (payload: any) =>
    http.post('/data/sources', payload).then(r => r.data);

export const updateDataSource = (id: string, payload: any) =>
    http.put(`/data/sources/${id}`, payload).then(r => r.data);

export const deleteDataSource = (id: string) =>
    http.delete(`/data/sources/${id}`).then(r => r.data);

export const listAllDatasets = (): Promise<Dataset[]> =>
    http.get('/data/datasets').then(r => r.data);

export const listDatasetsBySource = (sourceId: string): Promise<Dataset[]> =>
    http.get(`/data/sources/${sourceId}/datasets`).then((res) => res.data);

export const createDataset = (payload: any) =>
    http.post('/data/datasets', payload).then(r => r.data);

export const updateDataset = (id: string, payload: any) =>
    http.put(`/data/datasets/${id}`, payload).then(r => r.data);

export const deleteDataset = (id: string) =>
    http.delete(`/data/datasets/${id}`).then(r => r.data);

export const previewDataset = (datasetId: string, page = 1, pageSize = 20) =>
    http
        .get(`/data/datasets/${datasetId}/preview`, {
            params: { page, page_size: pageSize },
        })
        .then((res) => res.data);

export const getDatasetProfile = (datasetId: string) =>
    http.get(`/data/datasets/${datasetId}/profile`).then((res) => res.data);

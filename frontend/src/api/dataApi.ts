// src/api/dataApi.ts
import http from './http';

export const listDataSources = () =>
    http.get('/data/sources').then((res) => res.data);

export const listDatasets = (sourceId: string) =>
    http.get(`/data/sources/${sourceId}/datasets`).then((res) => res.data);

export const getDatasetPreview = (datasetId: string, page = 1, pageSize = 20) =>
    http
        .get(`/data/datasets/${datasetId}/preview`, {
            params: { page, page_size: pageSize },
        })
        .then((res) => res.data);

export const getDatasetProfile = (datasetId: string) =>
    http.get(`/data/datasets/${datasetId}/profile`).then((res) => res.data);

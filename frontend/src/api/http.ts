// src/api/http.ts
import axios from 'axios';

/*
const http = axios.create({
    baseURL: 'http://localhost:8000/api/v1',
    timeout: 10000,
});

// 重要：POC 简化，只做基础错误处理
http.interceptors.response.use(
    (resp) => resp,
    (error) => {
        console.error('API Error', error);
        throw error;
    }
);
*/


const http = axios.create({
    baseURL: '/api/v1', // 由 devServer 代理到 FastAPI
    timeout: 15000,
});

// 请求拦截：带上 token（如果有）
http.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers = config.headers || {};
        config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
});

export default http;

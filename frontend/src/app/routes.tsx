// src/app/routes.tsx
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';

// Layout
import MainLayout from '../components/Layout/MainLayout';

// Data module
import DataSourceList from '../pages/Data/DataSourceList';
import DatasetList from '../pages/Data/DatasetList';
import DatasetPreview from '../pages/Data/DatasetPreview';

// Workflow module
import WorkflowCanvas from '../pages/Workflow/WorkflowCanvas';

// Deploy module
import ServiceList from '../pages/Deploy/ServiceList';
import ServiceDetail from '../pages/Deploy/ServiceDetail';

// Model
import ModelList from '../pages/Model/ModelList';
import ModelMonitor from '../pages/Monitor/ModelMonitor';

// Monitor module
import ServiceMonitor from '../pages/Monitor/ServiceMonitor';

// System module
import UserList from '../pages/System/UserList';
import AuditLog from '../pages/System/AuditLog';

const AppRoutes: React.FC = () => {
    return (
        <Routes>
            {/* Main layout wrapper */}
            <Route path="/" element={<MainLayout />}>
                {/* Default redirect */}
                <Route index element={<Navigate to="/data" replace />} />

                {/* Data module */}
                <Route path="data" element={<DataSourceList />} />
                <Route path="data/datasets" element={<DatasetList />} />
                <Route path="data/preview" element={<DatasetPreview />} />

                {/* Workflow module */}
                <Route path="workflow" element={<WorkflowCanvas />} />

                {/* Deploy module */}
                <Route path="deploy" element={<ServiceList />} />
                <Route path="deploy/:id" element={<ServiceDetail />} />

                <Route path="model" element={<ModelList />} />

                {/* Monitor module */}
                <Route path="monitor" element={<ServiceMonitor />} />
                <Route path="monitor/model" element={<ModelMonitor />} />

                {/* System module */}
                <Route path="system" element={<UserList />} />
                <Route path="system/audit" element={<AuditLog />} />
            </Route>

            {/* Fallback route */}
            <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
    );
};

export default AppRoutes;

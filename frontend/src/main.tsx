// src/main.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import AppRoutes from './app/routes';
import 'antd/dist/reset.css';
import { Provider } from 'react-redux';
import { store } from './app/store';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
    <React.StrictMode>
        <Provider store={store}>
            <AppRoutes />
        </Provider>
    </React.StrictMode>
);

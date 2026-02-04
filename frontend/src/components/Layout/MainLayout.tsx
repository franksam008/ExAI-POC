// src/components/Layout/MainLayout.tsx
import React from 'react';
import { Layout } from 'antd';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import HeaderBar from './Header';

const { Header, Sider, Content } = Layout;

const MainLayout: React.FC = () => {
    return (
        <Layout style={{ minHeight: '100vh' }}>
            <Sider>
                <div style={{ color: '#fff', padding: 16, fontWeight: 'bold' }}>ExAI全生命周期平台</div>
                <Sidebar />
            </Sider>
            <Layout>
                <Header style={{ background: '#fff', paddingLeft: 16 }}>
                    <HeaderBar />
                </Header>
                <Content style={{ margin: 8, background: '#fff', padding: 8 }}>
                    <Outlet />
                </Content>
            </Layout>
        </Layout>
    );
};

export default MainLayout;

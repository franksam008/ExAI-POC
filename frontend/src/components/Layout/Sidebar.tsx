// src/components/Layout/Sidebar.tsx
import React from 'react';
import { Menu } from 'antd';
import { Link, useLocation } from 'react-router-dom';

const Sidebar: React.FC = () => {
    const location = useLocation();

    // 取一级路径作为菜单高亮，例如 /deploy/123 → deploy
    const selectedKey = location.pathname.split('/')[1] || 'data';

    const menuItems = [
        { key: 'data', label: <Link to="/data">数据</Link> },
        { key: 'workflow', label: <Link to="/workflows">工作流</Link> },
        { key: 'model', label: <Link to="/model">模型</Link> },
        { key: 'deploy', label: <Link to="/deploy">部署</Link> },
        { key: 'monitor', label: <Link to="/monitor">监控</Link> },
        { key: 'system', label: <Link to="/system">系统</Link> },
    ];

    return (
        <Menu
            theme="dark"
            mode="inline"
            selectedKeys={[selectedKey]}
            items={menuItems}
        />
    );
};

export default Sidebar;

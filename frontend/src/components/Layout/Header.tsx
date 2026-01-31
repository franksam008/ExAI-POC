// src/components/Layout/Header.tsx
import React from 'react';

/**
 * 顶部 Header 组件：
 * - POC：展示标题，后续可加用户信息、租户切换等
 */
const HeaderBar: React.FC = () => {
    return (
        <div style={{ fontSize: 16, fontWeight: 'bold' }}>
            ExAI 模型全生命周期平台（POC）
        </div>
    );
};

export default HeaderBar;

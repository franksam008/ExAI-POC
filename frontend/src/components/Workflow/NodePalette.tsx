// src/components/Workflow/NodePalette.tsx
import React from 'react';
import { Button } from 'antd';

/**
 * 节点面板：
 * - POC：只提供 4 种节点按钮，点击后在画布中追加
 */
interface Props {
    onAddNode: (type: string) => void;
}

const NodePalette: React.FC<Props> = ({ onAddNode }) => {
    return (
        <div>
            <Button block onClick={() => onAddNode('data_source')}>
                数据源
            </Button>
            <Button block onClick={() => onAddNode('train')} style={{ marginTop: 8 }}>
                训练
            </Button>
            <Button block onClick={() => onAddNode('register')} style={{ marginTop: 8 }}>
                注册
            </Button>
            <Button block onClick={() => onAddNode('deploy')} style={{ marginTop: 8 }}>
                部署
            </Button>
        </div>
    );
};

export default NodePalette;

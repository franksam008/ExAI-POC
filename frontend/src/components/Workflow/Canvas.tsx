// src/components/Workflow/Canvas.tsx
import React from 'react';
import { Card } from 'antd';
import { WorkflowNode } from '../../api/workflowApi';

/**
 * 画布组件：
 * - POC：用简单列表代替真正的可视化连线
 */
interface Props {
    nodes: WorkflowNode[];
    onSelectNode: (id: string) => void;
}

const Canvas: React.FC<Props> = ({ nodes, onSelectNode }) => {
    return (
        <div>
            {nodes.map((n) => (
                <Card
                    key={n.id}
                    style={{ marginBottom: 8, cursor: 'pointer' }}
                    onClick={() => onSelectNode(n.id)}
                >
                    <div>{n.name}</div>
                    <div style={{ fontSize: 12, color: '#999' }}>{n.type}</div>
                </Card>
            ))}
        </div>
    );
};

export default Canvas;

// src/components/Workflow/NodePropertiesPanel.tsx
import React from 'react';
import { Form, Input } from 'antd';
import { WorkflowNode } from '../../api/workflowApi';

/**
 * 节点属性面板：
 * - POC：根据节点类型展示少量关键参数
 */
interface Props {
    node?: WorkflowNode;
    onChange: (node: WorkflowNode) => void;
}

const NodePropertiesPanel: React.FC<Props> = ({ node, onChange }) => {
    if (!node) return <div>请选择一个节点</div>;

    const updateParam = (key: string, value: any) => {
        onChange({
            ...node,
            params: {
                ...node.params,
                [key]: value,
            },
        });
    };

    return (
        <Form layout="vertical">
            <Form.Item label="节点名称">
                <Input
                    value={node.name}
                    onChange={(e) => onChange({ ...node, name: e.target.value })}
                />
            </Form.Item>

            {node.type === 'data_source' && (
                <Form.Item label="数据集引用（CSV 路径或表名）">
                    <Input
                        value={node.params.dataset_ref}
                        onChange={(e) => updateParam('dataset_ref', e.target.value)}
                    />
                </Form.Item>
            )}

            {node.type === 'train' && (
                <>
                    <Form.Item label="目标列">
                        <Input
                            value={node.params.target_column}
                            onChange={(e) => updateParam('target_column', e.target.value)}
                        />
                    </Form.Item>
                    <Form.Item label="实验名称">
                        <Input
                            value={node.params.experiment_name}
                            onChange={(e) => updateParam('experiment_name', e.target.value)}
                        />
                    </Form.Item>
                </>
            )}

            {node.type === 'register' && (
                <Form.Item label="模型名称">
                    <Input
                        value={node.params.model_name}
                        onChange={(e) => updateParam('model_name', e.target.value)}
                    />
                </Form.Item>
            )}
        </Form>
    );
};

export default NodePropertiesPanel;

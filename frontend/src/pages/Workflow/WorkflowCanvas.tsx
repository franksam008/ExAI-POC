import React, { useState } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { Button, message } from 'antd';
import NodePalette from '../../components/Workflow/NodePalette';
import Canvas from '../../components/Workflow/Canvas';
import NodePropertiesPanel from '../../components/Workflow/NodePropertiesPanel';
import RunStatusPanel from '../../components/Workflow/RunStatusPanel';   // ★ 新增
import { WorkflowNode, WorkflowDefinition, runWorkflow } from '../../api/workflowApi';

const WorkflowCanvas: React.FC = () => {
    const [nodes, setNodes] = useState<WorkflowNode[]>([]);
    const [selectedId, setSelectedId] = useState<string>();
    const [runResult, setRunResult] = useState<any>();   // ★ 新增

    const addNode = (type: string) => {
        const id = uuidv4();
        const node: WorkflowNode = {
            id,
            type: type as any,
            name: `${type}-${nodes.length + 1}`,
            params: {},
            upstream_ids: nodes.length ? [nodes[nodes.length - 1].id] : [],
        };
        setNodes([...nodes, node]);
    };

    const updateNode = (node: WorkflowNode) => {
        setNodes(nodes.map((n) => (n.id === node.id ? node : n)));
    };

    const selectedNode = nodes.find((n) => n.id === selectedId);

    const handleRun = async () => {
        const wf: WorkflowDefinition = {
            name: 'demo-workflow',
            description: 'POC 工作流',
            nodes,
        };

        try {
            const res = await runWorkflow('demo-id', wf);
            setRunResult(res);   // ★ 保存执行结果
            message.success(`执行完成，状态：${res.status}`);
        } catch (e) {
            message.error('执行失败');
        }
    };

    return (
        <div style={{ display: 'flex', gap: 16 }}>
            <div style={{ width: 200 }}>
                <NodePalette onAddNode={addNode} />
            </div>

            <div style={{ flex: 1 }}>
                <Canvas nodes={nodes} onSelectNode={setSelectedId} />
                <div style={{ marginTop: 16 }}>
                    <Button type="primary" onClick={handleRun} disabled={!nodes.length}>
                        执行工作流
                    </Button>
                </div>
            </div>

            <div style={{ width: 300 }}>
                <NodePropertiesPanel node={selectedNode} onChange={updateNode} />

                {/* ★ 新增：运行状态面板 */}
                <div style={{ marginTop: 16 }}>
                    <RunStatusPanel
                        status={runResult?.status}
                        context={runResult?.context}
                    />
                </div>
            </div>
        </div>
    );
};

export default WorkflowCanvas;

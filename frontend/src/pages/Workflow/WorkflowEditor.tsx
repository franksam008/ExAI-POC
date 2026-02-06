import React, { useEffect, useState, useCallback } from 'react';
import ReactFlow, {
    Background,
    Controls,
    MiniMap,
    addEdge,
    Connection,
    Edge,
    Node,
    applyNodeChanges,
    applyEdgeChanges,
} from 'reactflow';
import 'reactflow/dist/style.css';
import dagre from 'dagre'; //没有声明类型，但不影响使用

import { Button, Card, Select, Input, Form, Popconfirm, message } from 'antd';
import { useParams, useNavigate } from 'react-router-dom';

import {
    getWorkflow,
    createWorkflow,
    updateWorkflow,
    runWorkflow,
} from '../../api/workflowApi';

const nodeTypeOptions = [
    { label: 'H2O 导入数据', value: 'h2o_import' },
    { label: 'H2O 列出数据框', value: 'h2o_list_frames' },
    { label: 'H2O 解析设置', value: 'h2o_parse_setup' },
    { label: 'H2O 解析', value: 'h2o_parse' },
    { label: 'H2O 拆分数据框', value: 'h2o_split_frame' },
    { label: 'H2O 预处理', value: 'h2o_prep' },
    { label: 'H2O PCA', value: 'h2o_pca' },
    { label: 'H2O 训练', value: 'h2o_train' },
    { label: 'H2O 评估', value: 'h2o_eval' },
    { label: 'H2O 预测', value: 'h2o_predict' },
    { label: 'H2O 导出模型', value: 'h2o_export' },
    { label: 'MLflow 记录模型', value: 'mlflow_log' },
    { label: 'MLflow 注册模型', value: 'mlflow_register' },
    { label: 'MLflow 阶段切换', value: 'mlflow_transition' },
    { label: 'MLflow 获取 Run 信息', value: 'mlflow_get_run' },
    { label: 'MLflow 获取模型版本', value: 'mlflow_list_versions' },
];

const nodeWidth = 180;
const nodeHeight = 60;

const getLayoutedElements = (nodes: Node[], edges: Edge[]) => {
    const g = new dagre.graphlib.Graph();
    g.setDefaultEdgeLabel(() => ({}));
    g.setGraph({ rankdir: 'TB', nodesep: 40, ranksep: 80 });
    nodes.forEach((node) => {
        g.setNode(node.id, { width: nodeWidth, height: nodeHeight });
    });
    edges.forEach((edge) => {
        g.setEdge(edge.source, edge.target);
    });

    dagre.layout(g);
    return nodes.map((node) => {
        const pos = g.node(node.id);
        return {
            ...node,
            position: {
                x: pos.x - nodeWidth / 2,
                y: pos.y - nodeHeight / 2,
            },
        };
    });
};

const WorkflowEditor: React.FC = () => {
    const { workflowId } = useParams();
    const navigate = useNavigate();

    // 判断是否为创建模式
    const isCreate = (workflowId === undefined);

    const [nodes, setNodes] = useState<Node[]>([]);
    const [edges, setEdges] = useState<Edge[]>([]);
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [runResult, setRunResult] = useState<any | null>(null);

    const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
    const [form] = Form.useForm();

    // -----------------------------
    // 初始化：创建模式 / 编辑模式
    // -----------------------------
    useEffect(() => {
        if (isCreate) {
            setNodes([
                {
                    id: 'node-1',
                    data: { label: 'H2O 导入数据', type: 'h2o_import', params: {} },
                    position: { x: 100, y: 100 },
                },
            ]);
            setEdges([]);
            console.log("is creating")
            return;
        }


        getWorkflow(workflowId).then((wf) => {
            setName(wf.name);
            setDescription(wf.description || '');

            setNodes(
                wf.dag.nodes.map((n: any, idx: number) => ({
                    id: n.id,
                    data: { label: n.label, type: n.type, params: n.params },
                    position: n.position || { x: 100 + idx * 150, y: 100 },
                })),
            );

            setEdges(
                wf.dag.edges.map((e: any) => ({
                    id: e.id,
                    source: e.source,
                    target: e.target,
                })),
            );
        });
    }, [workflowId, isCreate]);

    // -----------------------------
    // DAG 连接
    // -----------------------------
    const onNodesChange = useCallback(
        (changes: any) => setNodes((nds) => applyNodeChanges(changes, nds)),
        [],
    );
    const onEdgesChange = useCallback(
        (changes: any) => setEdges((eds) => applyEdgeChanges(changes, eds)),
        [],
    );
    const onConnect = useCallback(
        (connection: Connection) => setEdges((eds) => addEdge(connection, eds)),
        [],
    );

    // -----------------------------
    // 添加节点
    // -----------------------------
    const addNode = (type: string) => {
        const id = `node-${nodes.length + 1}`;
        const label = nodeTypeOptions.find((t) => t.value === type)?.label || type;

        setNodes([
            ...nodes,
            {
                id,
                data: { label, type, params: {} },
                position: { x: 100 + nodes.length * 150, y: 200 },
            },
        ]);
    };

    // -----------------------------
    // 点击节点 → 打开右侧参数配置
    // -----------------------------
    const onNodeClick = (_: any, node: Node) => {
        setSelectedNodeId(node.id);
        const data: any = node.data;

        form.setFieldsValue({
            label: data.label,
            type: data.type,
            params: JSON.stringify(data.params || {}, null, 2),
        });
    };

    // -----------------------------
    // 删除节点
    // -----------------------------
    const deleteSelectedNode = () => {
        if (!selectedNodeId) {
            message.warning('请先选择一个节点');
            return;
        }
        setNodes((nds) => nds.filter((n) => n.id !== selectedNodeId));
        setEdges((eds) => eds.filter((e) => e.source !== selectedNodeId && e.target !== selectedNodeId)); setSelectedNodeId(null);
        message.success('节点已删除');
    };

    // -----------------------------
    // 自动布局
    // ----------------------------- 
    const autoLayout = () => {
        const layouted = getLayoutedElements(nodes, edges);
        setNodes(layouted);
    };

    // -----------------------------
    // 保存节点参数
    // -----------------------------
    const saveNodeParams = async () => {
        if (!selectedNodeId) return;

        const values = await form.validateFields();

        let parsedParams: any = {};
        try {
            parsedParams = values.params ? JSON.parse(values.params) : {};
        } catch {
            message.error('参数 JSON 格式错误');
            return;
        }

        setNodes((prev) =>
            prev.map((n) =>
                n.id === selectedNodeId
                    ? {
                        ...n,
                        data: {
                            ...n.data,
                            label: values.label,
                            type: values.type,
                            params: parsedParams,
                        },
                    }
                    : n,
            ),
        );

        message.success('节点参数已更新');
    };

    // -----------------------------
    // 保存工作流
    // -----------------------------
    const saveWorkflow = async () => {
        const dag = {
            nodes: nodes.map((n) => ({
                id: n.id,
                type: (n.data as any).type,
                label: (n.data as any).label,
                params: (n.data as any).params || {},
                position: n.position,
            })),
            edges: edges.map((e) => ({
                id: e.id,
                source: e.source,
                target: e.target,
            })),
        };

        const payload = { name, description, dag };

        if (isCreate) {
            const id = await createWorkflow(payload);
            message.success('工作流已创建');
            navigate(`/workflows/${id}`);
        } else {
            await updateWorkflow(workflowId!, payload);
            message.success('工作流已保存');
        }
    };

    // -----------------------------
    // 运行工作流
    // -----------------------------
    const run = async () => {
        if (isCreate) {
            message.warning('请先保存工作流');
            return;
        }
        setRunResult("工作流运行中...")
        const res = await runWorkflow(workflowId!);
        setRunResult(res);
    };

    // -----------------------------
    // 渲染
    // -----------------------------
    return (
        <div style={{ display: 'flex', height: '100%' }}>
            {/* 左侧：工作流配置 */}
            <Card style={{ width: 200, margin: 8 }} title="工作流配置">
                <div style={{ marginBottom: 8 }}>
                    <div>名称</div>
                    <Input value={name} onChange={(e) => setName(e.target.value)} />
                </div>

                <div style={{ marginBottom: 8 }}>
                    <div>描述</div>
                    <Input.TextArea
                        rows={3}
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                    />
                </div>

                <div style={{ marginBottom: 8 }}>
                    <div>添加节点</div>
                    <Select
                        style={{ width: '100%' }}
                        options={nodeTypeOptions}
                        placeholder="选择节点类型"
                        onSelect={(v) => addNode(v as string)}
                    />
                </div>

                <Button type="primary" block onClick={saveWorkflow} style={{ marginBottom: 8 }}>
                    保存工作流
                </Button>

                <Button block onClick={run} style={{ marginBottom: 8 }}>运行工作流</Button>

                <Button block onClick={autoLayout} style={{ marginBottom: 8 }}>
                    自动布局
                </Button>

                <Popconfirm title="确认删除当前选中节点？" onConfirm={deleteSelectedNode}>
                    <Button danger block>
                        删除选中节点
                    </Button>
                </Popconfirm>

                {runResult && (
                    <div style={{ marginTop: 16, maxHeight: 260, overflow: 'auto', fontSize: 12, backgroundColor: 'lightgray' }}>
                        <pre>{JSON.stringify(runResult, null, 2)}</pre>
                    </div>
                )}
            </Card>

            {/* 中间：DAG 画布 */}
            <div style={{ flex: 1, height: '100%', marginRight: 16 }}>
                <ReactFlow
                    nodes={nodes}
                    edges={edges}
                    onNodesChange={onNodesChange}
                    onEdgesChange={onEdgesChange}
                    onConnect={onConnect}
                    onNodeClick={onNodeClick}
                    fitView
                >
                    <Background />
                    <Controls />
                    <MiniMap />
                </ReactFlow>
            </div>

            {/* 右侧：节点参数配置 */}
            <Card style={{ width: 200 }} title="节点参数配置">
                {selectedNodeId ? (
                    <Form form={form} layout="vertical">
                        <Form.Item name="label" label="节点名称" rules={[{ required: true }]}>
                            <Input />
                        </Form.Item>

                        <Form.Item name="type" label="节点类型" rules={[{ required: true }]}>
                            <Select options={nodeTypeOptions} />
                        </Form.Item>

                        <Form.Item
                            name="params"
                            label="参数(JSON)"
                            tooltip="与后端 H2O/MLflow 适配器的 params 一一对应"
                        >
                            <Input.TextArea rows={10} />
                        </Form.Item>

                        <Button type="primary" block onClick={saveNodeParams}>
                            保存节点参数
                        </Button>
                    </Form>
                ) : (
                    <div>请选择一个节点进行配置</div>
                )}
            </Card>
        </div>
    );
};

export default WorkflowEditor;

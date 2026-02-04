// src/pages/Workflow/WorkflowList.tsx
import React, { useEffect, useState } from 'react';
import { Table, Button, Popconfirm, message } from 'antd';
import { listWorkflows, deleteWorkflow } from '../../api/workflowApi';
import { useNavigate } from 'react-router-dom';

const WorkflowList: React.FC = () => {
    const [data, setData] = useState<any[]>([]);
    const navigate = useNavigate();

    const fetchData = () => {
        listWorkflows().then(setData);
    }

    useEffect(() => {
        fetchData();
    }, []);

    return (
        <div>
            <h3>工作流列表</h3>
            <Button type="primary" onClick={() => navigate('/workflows/create')}>
                新建工作流
            </Button>

            <Table
                rowKey="id"
                dataSource={data}
                style={{ marginTop: 16 }}
                /*onRow={(record) => ({
                    onClick: () => navigate(`/workflows/${record.id}`),
                })}*/
                columns={[
                    { title: '名称', dataIndex: 'name' },
                    { title: '描述', dataIndex: 'description' },
                    {
                        title: '操作',
                        render: (_, r) => (
                            <>
                                <Button type="link" onClick={() => navigate(`/workflows/${r.id}`)}>编辑</Button>
                                <Popconfirm title="确认删除？" onConfirm={() => deleteWorkflow(r.id).then(fetchData)}>
                                    <Button danger type="link">删除</Button>
                                </Popconfirm>
                            </>
                        ),
                    }
                ]}
            />
        </div>
    );
};

export default WorkflowList;

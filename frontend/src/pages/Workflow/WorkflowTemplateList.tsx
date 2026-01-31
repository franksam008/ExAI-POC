import React, { useEffect, useState } from 'react';
import { Table, Button, Select } from 'antd';
import { listWorkflowTemplates } from '../../api/workflowTemplateApi';
import { useNavigate } from 'react-router-dom';

const WorkflowTemplateList: React.FC = () => {
    const [data, setData] = useState<any[]>([]);
    const [category, setCategory] = useState<string | undefined>();
    const nav = useNavigate();

    const fetchData = (cat?: string) => {
        listWorkflowTemplates(cat).then(setData);
    };

    useEffect(() => {
        fetchData(category);
    }, [category]);

    return (
        <div>
            <h2>工作流模板库</h2>

            <div style={{ marginBottom: 16 }}>
                <Select
                    placeholder="按分类筛选"
                    allowClear
                    style={{ width: 220, marginRight: 16 }}
                    value={category}
                    onChange={value => setCategory(value)}
                    options={[
                        { label: '全部', value: undefined as any },
                        { label: '分类模型', value: 'classification' },
                        { label: '回归模型', value: 'regression' },
                        { label: 'AutoML', value: 'automl' },
                    ]}
                />
            </div>

            <Table
                rowKey="id"
                dataSource={data}
                columns={[
                    { title: '名称', dataIndex: 'name' },
                    { title: '描述', dataIndex: 'description' },
                    { title: '分类', dataIndex: 'category' },
                    {
                        title: '操作',
                        render: (_, r) => (
                            <Button type="link" onClick={() => nav(`/workflow/templates/${r.id}`)}>
                                查看
                            </Button>
                        ),
                    },
                ]}
            />
        </div>
    );
};

export default WorkflowTemplateList;

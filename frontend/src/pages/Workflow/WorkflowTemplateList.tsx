import React, { useEffect, useState } from 'react';
import { Table, Button } from 'antd';
import { listWorkflowTemplates } from '../../api/workflowTemplateApi';
import { useNavigate } from 'react-router-dom';

const WorkflowTemplateList: React.FC = () => {
    const [data, setData] = useState<any[]>([]);
    const nav = useNavigate();

    useEffect(() => {
        listWorkflowTemplates().then(setData);
    }, []);

    return (
        <div>
            <h2>工作流模板库</h2>
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

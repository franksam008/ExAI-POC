import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getWorkflowTemplate } from '../../api/workflowTemplateApi';
import { Button } from 'antd';

const WorkflowTemplateDetail: React.FC = () => {
    const { id } = useParams();
    const [tpl, setTpl] = useState<any>();
    const nav = useNavigate();

    useEffect(() => {
        if (id) getWorkflowTemplate(id).then(setTpl);
    }, [id]);

    const loadToCanvas = () => {
        nav('/workflow', { state: { template: tpl.definition } });
    };

    if (!tpl) return null;

    return (
        <div>
            <h2>{tpl.name}</h2>
            <p>{tpl.description}</p>
            <pre>{JSON.stringify(tpl.definition, null, 2)}</pre>

            <Button type="primary" onClick={loadToCanvas}>
                使用此模板创建工作流
            </Button>
        </div>
    );
};

export default WorkflowTemplateDetail;

// src/pages/Model/ModelList.tsx
import React, { useEffect, useState } from 'react';
import { Table } from 'antd';
import { listModels } from '../../api/modelApi';

/**
 * 模型列表页面：
 * - POC：展示后端聚合的模型信息
 */
const ModelList: React.FC = () => {
    const [data, setData] = useState<any[]>([]);

    useEffect(() => {
        listModels().then(setData).catch(() => setData([]));
    }, []);

    return (
        <Table
            rowKey={(r) => `${r.name}-${r.version}`}
            dataSource={data}
            columns={[
                { title: '模型名称', dataIndex: 'name' },
                { title: '版本', dataIndex: 'version' },
                { title: '阶段', dataIndex: 'stage' },
                { title: "来源", dataIndex: "source" },
            ]}
        />
    );
};

export default ModelList;

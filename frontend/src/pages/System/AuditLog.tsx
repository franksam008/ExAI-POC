// src/pages/System/AuditLog.tsx
import React, { useEffect, useState } from 'react';
import { listAuditLogs } from '../../api/systemApi';
import { Table } from 'antd';

const AuditLog: React.FC = () => {
    const [data, setData] = useState<any[]>([]);

    useEffect(() => {
        listAuditLogs().then(setData);
    }, []);

    return (
        <Table
            rowKey="id"
            dataSource={data}
            columns={[
                { title: 'ID', dataIndex: 'id' },
                { title: '用户', dataIndex: 'user_id' },
                { title: '操作', dataIndex: 'action' },
                { title: '详情', dataIndex: 'detail' },
                { title: '时间', dataIndex: 'created_at' },
            ]}
        />
    );
};

export default AuditLog;

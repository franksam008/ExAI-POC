// src/pages/System/UserList.tsx
import React, { useEffect, useState } from 'react';
import { listUsers } from '../../api/systemApi';
import { Table } from 'antd';

const UserList: React.FC = () => {
    const [data, setData] = useState<any[]>([]);

    useEffect(() => {
        listUsers().then(setData);
    }, []);

    return (
        <Table
            rowKey="id"
            dataSource={data}
            columns={[
                { title: 'ID', dataIndex: 'id' },
                { title: '用户名', dataIndex: 'username' },
                { title: '创建时间', dataIndex: 'created_at' },
            ]}
        />
    );
};

export default UserList;

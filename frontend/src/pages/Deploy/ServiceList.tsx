// src/pages/Deploy/ServiceList.tsx
import React, { useEffect, useState } from 'react';
import { Table } from 'antd';
import { listServices, ServiceItem } from '../../api/deployApi';
import { useNavigate } from 'react-router-dom';

const ServiceList: React.FC = () => {
    const [data, setData] = useState<ServiceItem[]>([]);
    const nav = useNavigate();

    useEffect(() => {
        listServices().then(setData);
    }, []);

    return (
        <Table
            rowKey="id"
            dataSource={data}
            columns={[
                { title: '服务名称', dataIndex: 'name' },
                { title: '模型名称', dataIndex: 'model_name' },
                { title: '模型版本', dataIndex: 'model_version' },
                { title: '状态', dataIndex: 'status' },
                {
                    title: '操作',
                    render: (_, r) => (
                        <a onClick={() => nav(`/deploy/${r.id}`)}>详情</a>
                    ),
                },
            ]}
        />
    );
};

export default ServiceList;

// src/pages/Data/DatasetList.tsx
import React, { useEffect, useState } from 'react';
import { listDatasets } from '../../api/dataApi';
import { Table } from 'antd';

/**
 * 数据集列表页面：
 * - POC：展示本地数据库中的所有表
 */
const DatasetList: React.FC = () => {
    const [data, setData] = useState<any[]>([]);

    useEffect(() => {
        listDatasets('local_db').then(setData);
    }, []);

    return (
        <Table
            rowKey="id"
            dataSource={data}
            columns={[
                { title: 'ID', dataIndex: 'id' },
                { title: '名称', dataIndex: 'name' },
            ]}
            pagination={false}
        />
    );
};

export default DatasetList;

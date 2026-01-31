// src/pages/Data/DataSourceList.tsx
import React, { useEffect, useState } from 'react';
import { listDataSources } from '../../api/dataApi';
import { Table } from 'antd';

/**
 * 数据源列表页面：
 * - POC：只展示一个“本地数据库”数据源
 */
const DataSourceList: React.FC = () => {
    const [data, setData] = useState<any[]>([]);

    useEffect(() => {
        listDataSources().then(setData);
    }, []);

    return (
        <Table
            rowKey="id"
            dataSource={data}
            columns={[
                { title: 'ID', dataIndex: 'id' },
                { title: '名称', dataIndex: 'name' },
                { title: '类型', dataIndex: 'type' },
            ]}
            pagination={false}
        />
    );
};

export default DataSourceList;

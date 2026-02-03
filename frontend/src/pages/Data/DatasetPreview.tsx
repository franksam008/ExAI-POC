// src/pages/Data/DatasetPreview.tsx
import React, { useEffect, useState } from 'react';
import { previewDataset } from '../../api/dataApi';
import { Table, Select } from 'antd';

/**
 * 数据集预览页面：
 * - POC：通过下拉选择表名，展示前 N 行
 */
const DatasetPreview: React.FC = () => {
    const [datasetId, setDatasetId] = useState<string>('your_table');
    const [data, setData] = useState<any>({ columns: [], rows: [] });

    useEffect(() => {
        if (datasetId) {
            previewDataset(datasetId).then(setData);
        }
    }, [datasetId]);

    return (
        <div>
            <div style={{ marginBottom: 16 }}>
                <span>数据集 ID：</span>
                <Select
                    style={{ width: 200 }}
                    value={datasetId}
                    onChange={setDatasetId}
                    options={[
                        { label: 'your_table', value: 'your_table' },
                        // 实际可从 DatasetList 传参或全局状态获取
                    ]}
                />
            </div>
            <Table
                rowKey={(row) => JSON.stringify(row)}
                dataSource={data.rows}
                columns={data.columns.map((c: string) => ({
                    title: c,
                    dataIndex: c,
                }))}
                pagination={false}
            />
        </div>
    );
};

export default DatasetPreview;

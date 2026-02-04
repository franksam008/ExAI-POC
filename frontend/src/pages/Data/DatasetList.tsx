// src/pages/Data/DatasetList.tsx
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Table, Button, Modal, Form, Input, Select, Popconfirm, message } from 'antd';
import { listDataSources, listAllDatasets, listDatasetsBySource, createDataset, updateDataset, deleteDataset, previewDataset } from '../../api/dataApi';
import { DataSource, Dataset } from '../../api/dataApi';

const DatasetList: React.FC = () => {
    const { sourceId } = useParams();
    const navigate = useNavigate();
    const [data, setData] = useState<any[]>([]);
    const [sources, setSources] = useState<any[]>([]);
    const [datasourceMap, setDatasourceMap] = useState<Record<string, string>>({});
    const [visible, setVisible] = useState(false);
    const [editing, setEditing] = useState<any | null>(null);
    const [preview, setPreview] = useState<any | null>(null);
    const [previewVisible, setPreviewVisible] = useState(false);
    const [form] = Form.useForm();

    const fetchData = () => {
        if (sourceId) {
            listDatasetsBySource(sourceId).then(setData);
        } else {
            listAllDatasets().then(setData);
        }
    }

    useEffect(() => {
        //fetchData();
        listDataSources().then(list => {
            setSources(list);
            const map = Object.fromEntries(list.map((ds: DataSource) => [ds.id, ds.name]));
            setDatasourceMap(map);
        });
    }, []);

    useEffect(() => {
        fetchData();
    }, [sourceId])

    const ruturnToDatasource = () => {
        navigate(`/data/sources/`);
    };

    const openCreate = () => {
        setEditing(null);
        form.resetFields();
        setVisible(true);
    };

    const openEdit = (record: any) => {
        setEditing(record);
        form.setFieldsValue({
            name: record.name,
            source_id: record.source_id,
            table_name: record.table_name,
            description: record.description,
        });
        setVisible(true);
    };

    const onSubmit = async () => {
        const values = await form.validateFields();
        if (editing) {
            await updateDataset(editing.id, values);
            message.success('修改成功');
        } else {
            await createDataset(values);
            message.success('创建成功');
        }
        setVisible(false);
        setEditing(null);
        form.resetFields();
        fetchData();
    };

    const onPreview = async (id: string) => {
        const res = await previewDataset(id);
        setPreview(res);
        setPreviewVisible(true);
    };

    return (
        <div>
            <h3>数据集管理</h3>
            <Button type="primary" onClick={openCreate}>新建数据集</Button>&nbsp;
            <Button type="primary" onClick={ruturnToDatasource}>&lArr;返回数据源</Button>
            <Table
                rowKey="id"
                dataSource={data}
                style={{ marginTop: 8 }}
                columns={[
                    { title: '名称', dataIndex: 'name' },
                    {
                        title: '数据源名',
                        dataIndex: 'source_id',
                        render: (id) => datasourceMap[id] || `#${id}`
                    },
                    { title: '表名', dataIndex: 'table_name' },
                    { title: '描述', dataIndex: 'description' },
                    {
                        title: '操作',
                        render: (_, r) => (
                            <>
                                <Button type="link" onClick={() => onPreview(r.id)}>预览</Button>
                                <Button type="link" onClick={() => openEdit(r)}>编辑</Button>
                                <Popconfirm title="确认删除？" onConfirm={() => deleteDataset(r.id).then(fetchData)}>
                                    <Button danger type="link">删除</Button>
                                </Popconfirm>
                            </>
                        ),
                    },
                ]}
            />

            <Modal
                title={editing ? '编辑数据集' : '新建数据集'}
                open={visible}
                onOk={onSubmit}
                onCancel={() => setVisible(false)}
                destroyOnHidden
            >
                <Form form={form} layout="vertical">
                    <Form.Item name="name" label="名称" rules={[{ required: true }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item name="source_id" label="数据源" rules={[{ required: true }]}>
                        <Select
                            options={sources.map((s: any) => ({
                                label: s.name,
                                value: s.id,
                            }))}
                        />
                    </Form.Item>
                    <Form.Item name="table_name" label="表名" rules={[{ required: true }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item name="description" label="描述">
                        <Input.TextArea rows={3} />
                    </Form.Item>
                </Form>
            </Modal>

            <Modal
                title="数据集预览"
                open={previewVisible}
                onCancel={() => setPreviewVisible(false)}
                footer={null}
                width={800}
            >
                {preview && (
                    <Table
                        rowKey={(_, idx) => String(idx)}
                        dataSource={preview.rows}
                        columns={preview.columns.map((c: string) => ({
                            title: c,
                            dataIndex: c,
                        }))}
                        pagination={false}
                        size="small"
                        scroll={{ x: true }}
                    />
                )}
            </Modal>
        </div>
    );
};

export default DatasetList;

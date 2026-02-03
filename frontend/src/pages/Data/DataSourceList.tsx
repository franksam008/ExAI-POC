// src/pages/Data/DataSourceList.tsx
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { listDataSources, createDataSource, updateDataSource, deleteDataSource } from '../../api/dataApi';
import { Table, Button, Modal, Form, Input, Select, Popconfirm, message } from 'antd';

/**
 * 数据源列表页面：
 * - POC：只展示一个“本地数据库”数据源
 */
const DataSourceList: React.FC = () => {
    const navigate = useNavigate();
    const [data, setData] = useState<any[]>([]);
    const [visible, setVisible] = useState(false);
    const [editing, setEditing] = useState<any>(null);
    const [form] = Form.useForm();

    const fetchData = () => listDataSources().then(setData);

    const onRowClick = (record: any) => {
        console.log(`navigate to /data/sources/${record.id}/datasets`)
        navigate(`/data/sources/${record.id}/datasets`);
    };

    useEffect(() => {
        fetchData();
    }, []);

    const openCreate = () => {
        setEditing(null);
        form.resetFields();
        setVisible(true);
    };

    const openEdit = (record: any) => {
        setEditing(record);
        form.setFieldsValue({
            name: record.name,
            type: record.type,
            config: JSON.stringify(record.config, null, 2),
        });
        setVisible(true);
    };

    const onSubmit = async () => {
        const values = await form.validateFields();
        const payload = {
            name: values.name,
            type: values.type,
            config: JSON.parse(values.config || {}),
        };
        if (editing) {
            await updateDataSource(editing.id, payload);
            message.success('修改成功');
        } else {
            await createDataSource(payload);
            message.success('创建成功');
        }
        setVisible(false);
        setEditing(null);
        form.resetFields();
        fetchData();
    };

    return (
        <div>
            <h3>数据源管理</h3>
            <Button type="primary" onClick={openCreate}>新建数据源</Button>
            <Table
                rowKey="id"
                dataSource={data}
                onRow={(record) => ({
                    onClick: () => onRowClick(record),
                })}
                style={{ marginTop: 8 }}
                columns={[
                    //{ title: 'ID', dataIndex: 'id' },
                    { title: '名称', dataIndex: 'name' },
                    { title: '类型', dataIndex: 'type' },
                    {
                        title: '配置参数',
                        dataIndex: 'config',
                        render: (value) => {
                            if (!value) return '-'
                            try {
                                return JSON.stringify(value, null, 2)
                            } catch (e) {
                                return String(value)
                            }
                        }
                    },
                    {
                        title: '操作',
                        render: (_, r) => (
                            <>
                                <Button type="link" onClick={() => openEdit(r)}>编辑</Button>
                                <Popconfirm title="确认删除？" onConfirm={() => deleteDataSource(r.id).then(fetchData)}>
                                    <Button danger type="link">删除</Button>
                                </Popconfirm>
                            </>
                        ),
                    },
                ]}
            />

            <Modal
                title={editing ? '编辑数据源' : '新建数据源'}
                open={visible}
                onOk={onSubmit}
                onCancel={() => setVisible(false)}
                destroyOnHidden
            >
                <Form form={form} layout="vertical">
                    <Form.Item name="name" label="名称" rules={[{ required: true }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item name="type" label="类型" rules={[{ required: true }]}>
                        <Select
                            options={[
                                { label: '本地数据库', value: 'db' },
                                { label: 'MySQL', value: 'mysql' },
                                { label: 'PostgreSQL', value: 'postgres' },
                            ]}
                        />
                    </Form.Item>
                    <Form.Item
                        name="config"
                        label="配置(JSON)"
                        rules={[{ required: true, message: '请输入 JSON 配置' }]}
                    >
                        <Input.TextArea rows={4} placeholder='例如：{"url": "sqlite:///./data.db"}' />
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    );
};

export default DataSourceList;


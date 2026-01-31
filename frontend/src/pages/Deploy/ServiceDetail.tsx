// src/pages/Deploy/ServiceDetail.tsx
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Card, Form, Input, Button, message } from 'antd';
import { predict } from '../../api/deployApi';

/**
 * 服务详情 + 简单在线推理：
 * - POC：手动输入 JSON 特征，调用后端 /predict
 */
const ServiceDetail: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const [features, setFeatures] = useState<string>('{}');
    const [result, setResult] = useState<any>();

    const handlePredict = async () => {
        try {
            const obj = JSON.parse(features);
            const res = await predict(id!, obj);
            setResult(res);
        } catch (e) {
            message.error('JSON 格式错误或预测失败');
        }
    };

    return (
        <Card title={`服务详情：${id}`}>
            <Form layout="vertical">
                <Form.Item label="特征 JSON">
                    <Input.TextArea
                        rows={6}
                        value={features}
                        onChange={(e) => setFeatures(e.target.value)}
                    />
                </Form.Item>
                <Button type="primary" onClick={handlePredict}>
                    调用预测
                </Button>
            </Form>
            {result && (
                <div style={{ marginTop: 16 }}>
                    <div>预测结果：</div>
                    <pre>{JSON.stringify(result, null, 2)}</pre>
                </div>
            )}
        </Card>
    );
};

export default ServiceDetail;

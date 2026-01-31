import React, { useState } from 'react';
import { Input, Button } from 'antd';
import { getModelMetrics } from '../../api/modelApi';

const ModelMonitor: React.FC = () => {
    const [name, setName] = useState('');
    const [version, setVersion] = useState('');
    const [data, setData] = useState<any>();

    const load = async () => {
        if (!name || !version) return;
        const res = await getModelMetrics(name, version);
        setData(res);
    };

    return (
        <div>
            <div style={{ marginBottom: 16 }}>
                <Input
                    style={{ width: 200, marginRight: 8 }}
                    placeholder="模型名称"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
                <Input
                    style={{ width: 120, marginRight: 8 }}
                    placeholder="版本"
                    value={version}
                    onChange={(e) => setVersion(e.target.value)}
                />
                <Button type="primary" onClick={load}>
                    加载指标
                </Button>
            </div>
            {data && (
                <pre style={{ maxHeight: 400, overflow: 'auto' }}>
                    {JSON.stringify(data, null, 2)}
                </pre>
            )}
        </div>
    );
};

export default ModelMonitor;

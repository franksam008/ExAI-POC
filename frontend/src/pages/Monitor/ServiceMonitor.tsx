// src/pages/Monitor/ServiceMonitor.tsx
import React, { useEffect, useState } from 'react';
import { getServiceMetrics, MetricPoint } from '../../api/monitorApi';
import ReactECharts from 'echarts-for-react';
import { Input, Button } from 'antd';

/**
 * 服务监控页面：
 * - POC：输入 service_id，展示 QPS 曲线
 */
const ServiceMonitor: React.FC = () => {
    const [serviceId, setServiceId] = useState<string>('');
    const [data, setData] = useState<MetricPoint[]>([]);

    const load = async () => {
        if (!serviceId) return;
        const res = await getServiceMetrics(serviceId);
        setData(res);
    };

    const option = {
        tooltip: { trigger: 'axis' },
        legend: { data: ['QPS', '延迟(ms)', '错误率'] },
        xAxis: {
            type: 'category',
            data: data.map((d) => d.timestamp),
        },
        yAxis: [
            { type: 'value', name: 'QPS' },
            { type: 'value', name: '延迟(ms)' },
            { type: 'value', name: '错误率' },
        ],
        series: [
            { name: 'QPS', type: 'line', data: data.map((d) => d.qps) },
            { name: '延迟(ms)', type: 'line', yAxisIndex: 1, data: data.map((d) => d.latency_ms) },
            { name: '错误率', type: 'line', yAxisIndex: 2, data: data.map((d) => d.error_rate) },
        ],
    };

    return (
        <div>
            <div style={{ marginBottom: 16 }}>
                <Input
                    style={{ width: 300, marginRight: 8 }}
                    placeholder="输入 service_id"
                    value={serviceId}
                    onChange={(e) => setServiceId(e.target.value)}
                />
                <Button type="primary" onClick={load}>
                    加载监控数据
                </Button>
            </div>
            {data.length > 0 && <ReactECharts option={option} style={{ height: 400 }} />}
        </div>
    );
};

export default ServiceMonitor;

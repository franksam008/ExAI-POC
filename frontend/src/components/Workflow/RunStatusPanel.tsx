// src/components/Workflow/RunStatusPanel.tsx
import React from 'react';

interface Props {
    status?: string;
    context?: any;
}

/**
 * 工作流运行状态面板：
 * - POC：展示状态 + context JSON
 */
const RunStatusPanel: React.FC<Props> = ({ status, context }) => {
    if (!status) return <div>尚未执行</div>;
    return (
        <div>
            <div>状态：{status}</div>
            <div style={{ marginTop: 8 }}>
                <div>上下文：</div>
                <pre style={{ maxHeight: 200, overflow: 'auto' }}>
                    {JSON.stringify(context, null, 2)}
                </pre>
            </div>
        </div>
    );
};

export default RunStatusPanel;

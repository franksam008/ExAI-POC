import React from 'react';
import { Result, Button } from 'antd';

/**
 * 应用错误边界组件
 * 用于捕获和处理子组件中发生的 JavaScript 错误
 * 防止错误传播到根组件，避免整个应用崩溃
 */
export class AppErrorBoundary extends React.Component<React.PropsWithChildren> {
    /**
     * 组件状态
     * hasError: 是否发生错误的标志位
     */
    state = { hasError: false };

    /**
     * 静态方法：从错误状态更新组件状态
     * 当子组件抛出错误时，React 会调用此方法
     * @returns 更新后的状态对象，设置 hasError 为 true
     */
    static getDerivedStateFromError() {
        return { hasError: true };
    }

    /**
     * 错误捕获生命周期方法
     * 记录错误信息到控制台，便于调试和监控
     * @param error 捕获到的错误对象
     */
    componentDidCatch(error: any) {
        console.error('AppErrorBoundary caught an error:', error);
    }

    /**
     * 渲染方法
     * 根据错误状态决定渲染错误页面或正常子组件
     * @returns 错误页面或子组件
     */
    render() {
        if ((this.state as any).hasError) {
            return (
                <Result
                    status="error"
                    title="页面发生错误"
                    extra={
                        <Button onClick={() => location.reload()}>
                            刷新
                        </Button>
                    }
                />
            );
        }
        return this.props.children;
    }
}

# ExAI —— AI 模型全生命周期平台（POC 版）
本项目是一个可直接运行的 AI 模型全生命周期平台 POC，覆盖：

- 数据接入与预览

- 工作流编排（数据源 → 训练 → 注册 → 部署）

- 模型训练（H2O）

- 模型注册（MLflow Model Registry）

- 模型部署（FastAPI 内部服务）

- 在线推理（MLflow PyFunc）

- 服务监控（POC 级时间序列）

- 系统管理（用户、审计日志）

本 POC 完整实现了从数据 → 训练 → 注册 → 部署 → 推理的闭环，可用于演示、评估、架构验证。

## 1. 系统架构
```
┌──────────────────────────────┐
│           前端（React）        │
│  数据浏览 / 工作流 / 模型 / 部署 │
└──────────────────────────────┘
┌──────────────────────────────┐
│        后端 API（FastAPI）     │
│  数据 / 工作流 / 模型 / 部署 / 监控 │
└──────────────────────────────┘
┌──────────────────────────────────────────────┐
│                领域服务层                      │
│  Workflow / ModelDev / ModelGovern / Monitor │
└──────────────────────────────────────────────┘
┌──────────────────────────────────────────────┐
│              外部系统适配层                    │
│  H2O / MLflow / Metadata / ResourceManager   │
└──────────────────────────────────────────────┘
┌──────────────────────────────────────────────┐
│                基础设施层                      │
│  PostgreSQL / MLflow Tracking / H2O / Logs   │
└──────────────────────────────────────────────┘
```
## 2. 环境准备
### 2.1 Python 环境
```bash
cd backend
pip install -r requirements.txt
```
### 2.2 Node 环境
```bash
cd frontend
npm install
```
### 2.3 数据库（PostgreSQL 或 MySQL）
示例 PostgreSQL：

```bash
createdb exai_poc
```
配置 backend/app/config.py：

```python
DATABASE_URL = "postgresql://user:password@localhost:5432/exai_poc"
```
### 2.4 启动 MLflow Tracking Server
```bash
mlflow server \
  --backend-store-uri sqlite:///./backend/data/mlflow.db \
  --default-artifact-root ./backend/data/mlruns \
  --host 0.0.0.0 --port 5000
```
### 2.5 启动 H2O
方式一：Python

```python
import h2o
h2o.init()
```
方式二：Standalone

```bash
java -jar h2o.jar
```
确保地址与 config.py 中一致：

```python
H2O_URL = "http://localhost:54321"
```
## 3. 后端启动
```bash
cd backend
uvicorn app.main:app --reload
```
后端地址：

```Code
http://localhost:8000
```
## 4. 前端启动
```bash
cd frontend
npm run dev
```
前端地址：

```Code
http://localhost:5173
```
## 5. 数据库初始化（必做）

平台需要一条数据集元数据记录。

### 5.1 创建物理表（示例：Iris 数据集）
```sql
CREATE TABLE demo_iris (
    sepal_length FLOAT,
    sepal_width FLOAT,
    petal_length FLOAT,
    petal_width FLOAT,
    species VARCHAR(32)
);
```
### 5.2 插入数据（示例 10 行）
```sql
INSERT INTO demo_iris VALUES
(5.1, 3.5, 1.4, 0.2, 'setosa'),
(4.9, 3.0, 1.4, 0.2, 'setosa'),
(6.2, 2.8, 4.8, 1.8, 'virginica'),
(5.9, 3.0, 5.1, 1.8, 'virginica'),
(6.7, 3.1, 4.4, 1.4, 'versicolor'),
(5.6, 2.5, 3.9, 1.1, 'versicolor'),
(5.0, 3.4, 1.5, 0.2, 'setosa'),
(6.3, 3.3, 6.0, 2.5, 'virginica'),
(5.8, 2.7, 5.1, 1.9, 'virginica'),
(6.1, 2.8, 4.0, 1.3, 'versicolor');
```
### 5.3 注册数据集元数据
```sql
INSERT INTO datasets (id, tenant_id, source_id, name, table_name, description, created_at)
VALUES ('iris', 'default_tenant', 'local_db', 'Iris 数据集', 'demo_iris', 'Iris POC', NOW());
```
## 6. 端到端验收用例（最关键部分）
以下步骤将验证整个系统从数据 → 训练 → 注册 → 部署 → 推理的完整链路。

### ✔ Step 1：前端查看数据集
访问：

```Code
前端 → Data → Dataset List
```
应看到：

```Code
Iris 数据集
```
点击进入 → Dataset Preview
应看到 10 行真实数据。

### ✔ Step 2：构建工作流（前端）
进入：

```Code
Workflow → Workflow Canvas
```
依次拖拽节点：

### 1. 数据源节点

- dataset_ref = "iris"

### 2. 训练节点

- target_column = "species"

- feature_columns = ["sepal_length","sepal_width","petal_length","petal_width"]

- experiment_name = "iris_exp"

- algo_params:

```json
{
  "ntrees": 20,
  "max_depth": 5,
  "learn_rate": 0.1
}
```
### 3. 注册节点

- model_name = "iris_model"

### 4. 部署节点

- deploy_config = {}

点击**执行工作流**。

右侧 RunStatusPanel 应显示：

```Code
status: success
context:
  train_result: <H2O model id>
  artifact_uri: runs:/xxxx/model
  registry: { name: "iris_model", version: 1 }
  service: { id: "...", endpoint: "/api/v1/services/predict/<id>" }
```

### ✔ Step 3：查看模型（前端）
进入：

```Code
Model → Model List
```
应看到：

```Code
iris_model   version=1   stage=Staging
```
数据来自 MLflow Model Registry。

### ✔ Step 4：查看服务（前端）
进入：

```Code
Deploy → Service List
```
应看到：

```Code
iris_model_v1   running
```
点击进入 Service Detail。

### ✔ Step 5：在线推理（前端）
在 Service Detail 页面输入推理 JSON：

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```
点击 预测。

应看到类似：

```json
{
  "prediction": "setosa"
}
```
这是 H2O 训练出的模型通过 MLflow PyFunc 加载后的真实预测。

### ✔ Step 6：查看监控（前端）
进入：

```Code
Monitor → Service Monitor
```
选择刚刚部署的服务。

应看到：

- QPS 曲线

- 延迟曲线

- 错误率曲线

（当前为 POC 生成的时间序列，结构真实，可替换为 Prometheus）

## 7. 常见问题（FAQ）
### Q1：训练时报 H2O 连接错误？
检查：

```python
H2O_URL = "http://localhost:54321"
```
并确保：

```python
import h2o
h2o.init()
```
已成功启动。

### Q2：模型注册时报 MLflow 错误？
检查：

```Code
mlflow server --backend-store-uri sqlite:///mlflow.db ...
```
并确保：

```python
MLFLOW_TRACKING_URI = "http://localhost:5000"
```

### Q3：推理时报找不到模型？
确保 deploy 节点写入了：

```json
"model_uri": "models:/iris_model/1"
```

## 8. 结语
本 POC 已完整实现：

- 数据 → 训练 → 注册 → 部署 → 推理

- H2O + MLflow + FastAPI + React 全链路

- 可视化工作流

- 服务监控

- 系统管理

你可以在此基础上扩展：

- 分布式训练（Ray / Dask）

- Prometheus 真实监控

- K8s 部署

- 多租户隔离

- 工作流模板库
# app/domain/model_dev/service.py
from typing import Dict, Any
from app.domain.model_dev.models import TrainRequest, TrainResult, AlgorithmType
from app.adapters.h2o_adapter import H2OClient
from app.adapters.mlflow_adapter import MLflowClientAdapter
from app.constants import MLFLOW_EXPERIMENT_PREFIX


class ModelDevService:
    """
    模型开发服务：
    - 只实现：H2O GBM 训练 + MLflow 记录
    - 预留：算法扩展、分布式训练、资源管理
    """

    def __init__(self, h2o_client: H2OClient, mlflow_client: MLflowClientAdapter):
        self.h2o_client = h2o_client
        self.mlflow_client = mlflow_client

    def train(self, req: TrainRequest) -> TrainResult:
        # 重要：这里只实现 H2O_GBM，其他算法通过枚举扩展
        if req.algorithm != AlgorithmType.H2O_GBM:
            raise ValueError(f"暂不支持算法: {req.algorithm}")

        # 1. 导入数据集（POC 简化为 CSV 路径）
        frame = self.h2o_client.import_dataset(req.dataset_ref)

        # 2. 启动 MLflow Run
        experiment_name = f"{MLFLOW_EXPERIMENT_PREFIX}_{req.experiment_name}"
        run_id = self.mlflow_client.start_run(experiment_name, run_name="train")

        # 3. 训练模型
        model_id = self.h2o_client.train_model(
            frame=frame,
            target=req.target_column,
            params=req.params,
        )

        # 4. 获取指标并记录到 MLflow
        metrics = self.h2o_client.get_model_metrics(model_id)
        self.mlflow_client.log_params(run_id, req.params)
        self.mlflow_client.log_metrics(run_id, metrics)

        # 5. 记录模型到 MLflow（POC：直接用 H2O 模型）
        import h2o
        model = h2o.get_model(model_id)
        artifact_uri = self.mlflow_client.log_model(
            run_id=run_id,
            model=model,
            artifact_path="model",
        )

        return TrainResult(
            model_id=model_id,
            metrics=metrics,
            artifact_uri=artifact_uri,
            mlflow_run_id=run_id,
        )

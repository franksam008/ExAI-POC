# app/adapters/h2o_adapter.py
import h2o
from typing import Dict, Any
from abc import ABC, abstractmethod
from app.config import settings

"""
H2O 适配器：封装 H2O 的训练与预测能力。
POC 中只实现单机 H2O + 一种算法（GBM）。
"""

class H2OClient(ABC):
    @abstractmethod
    def import_dataset(self, source_ref: str):
        """
        导入数据集。
        source_ref：可以是 SQL 或表名，这里简化为 CSV 路径或表名。
        """
        raise NotImplementedError

    @abstractmethod
    def train_model(self, frame, target: str, params: Dict[str, Any]) -> str:
        """
        训练模型，返回模型 ID。
        """
        raise NotImplementedError

    @abstractmethod
    def get_model_metrics(self, model_id: str) -> Dict[str, float]:
        """
        获取模型评估指标。
        """
        raise NotImplementedError


class H2OHttpClient(H2OClient):
    def __init__(self):
        # 重要：初始化 H2O 连接，单机模式即可
        h2o.connect(url=settings.H2O_URL)

    def import_dataset(self, source_ref: str):
        # POC 简化：假设 source_ref 是 CSV 文件路径
        # 实际可扩展为从数据库读取后转为 H2OFrame
        return h2o.import_file(source_ref)

    def train_model(self, frame, target: str, params: Dict[str, Any]) -> str:
        from h2o.estimators import H2OGradientBoostingEstimator

        # 重要：这里只实现一种算法（GBM），但接口预留扩展空间
        model = H2OGradientBoostingEstimator(
            ntrees=params.get("ntrees", 50),
            max_depth=params.get("max_depth", 5),
            learn_rate=params.get("learn_rate", 0.1),
        )
        x = [c for c in frame.columns if c != target]
        model.train(x=x, y=target, training_frame=frame)
        return model.model_id

    def get_model_metrics(self, model_id: str) -> Dict[str, float]:
        model = h2o.get_model(model_id)
        perf = model.model_performance()
        # 重要：只返回少量核心指标，POC 足够
        metrics = {
            "auc": getattr(perf, "auc", None),
            "logloss": getattr(perf, "logloss", None),
        }
        return {k: float(v) for k, v in metrics.items() if v is not None}

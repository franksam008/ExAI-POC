# app/domain/workflow/executor.py
from typing import Dict, Any, List
from datetime import datetime
from uuid import uuid4
from app.domain.workflow.models import (
    WorkflowDefinition,
    WorkflowRun,
    RunStatus,
    WorkflowNode,
    NodeType,
)
from app.domain.model_dev.models import TrainRequest, AlgorithmType
from app.domain.model_dev.service import ModelDevService
from app.domain.model_govern.service import ModelGovernService

"""
工作流执行器：
- POC：单机、顺序执行（按拓扑排序）
- 预留：并行执行、分布式执行
"""

class WorkflowExecutor:
    def __init__(
        self,
        model_dev_service: ModelDevService,
        model_govern_service: ModelGovernService,
    ):
        self.model_dev_service = model_dev_service
        self.model_govern_service = model_govern_service

    def _topo_sort(self, nodes: List[WorkflowNode]) -> List[WorkflowNode]:
        # 简单拓扑排序，POC 版本，假设无环
        id_to_node = {n.id: n for n in nodes}
        indegree = {n.id: 0 for n in nodes}
        for n in nodes:
            for u in n.upstream_ids:
                indegree[n.id] += 1
        queue = [id for id, d in indegree.items() if d == 0]
        result = []
        while queue:
            nid = queue.pop(0)
            node = id_to_node[nid]
            result.append(node)
            for m in nodes:
                if nid in m.upstream_ids:
                    indegree[m.id] -= 1
                    if indegree[m.id] == 0:
                        queue.append(m.id)
        return result

    def execute(self, wf: WorkflowDefinition) -> WorkflowRun:
        run_id = str(uuid4())
        context: Dict[str, Any] = {}
        started_at = datetime.utcnow()
        status = RunStatus.RUNNING

        try:
            ordered_nodes = self._topo_sort(wf.nodes)
            for node in ordered_nodes:
                self._execute_node(node, context)
            status = RunStatus.SUCCESS
        except Exception as e:
            # 重要：POC 简化为直接失败，实际可加重试机制
            status = RunStatus.FAILED
            context["error"] = str(e)

        finished_at = datetime.utcnow()
        return WorkflowRun(
            id=run_id,
            workflow_id=wf.id or "",
            status=status,
            started_at=started_at,
            finished_at=finished_at,
            context=context,
        )

    def _execute_node(self, node: WorkflowNode, context: Dict[str, Any]) -> None:
        """
        核心节点执行逻辑：
        - data_source: 记录数据集引用
        - train: 调用 ModelDevService.train
        - register: 调用 ModelGovernService.register_model
        - deploy: 调用 ModelGovernService.deploy_model
        其他节点 POC 可简单记录参数。
        """
        if node.type == NodeType.DATA_SOURCE:
            # 假设 params 中有 dataset_ref
            context["dataset_ref"] = node.params["dataset_ref"]

        elif node.type == NodeType.TRAIN:
            req = TrainRequest(
                dataset_ref=context["dataset_ref"],
                target_column=node.params["target_column"],
                feature_columns=node.params.get("feature_columns", []),
                algorithm=AlgorithmType.H2O_GBM,
                params=node.params.get("algo_params", {}),
                experiment_name=node.params.get("experiment_name", "default"),
            )
            result = self.model_dev_service.train(req)
            context["train_result"] = result.model_id
            context["artifact_uri"] = result.artifact_uri

        elif node.type == NodeType.REGISTER:
            name = node.params["model_name"]
            artifact_uri = context["artifact_uri"]
            reg = self.model_govern_service.register_model(
                name=name,
                artifact_uri=artifact_uri,
                description=node.params.get("description", ""),
            )
            context["registry"] = reg

        elif node.type == NodeType.DEPLOY:
            reg = context["registry"]
            service = self.model_govern_service.deploy_model(
                name=reg.name,
                version=reg.version,
                config={
                    "model_uri": reg.mlflow_model_uri,
                    **node.params.get("deploy_config", {}),
                },
            )
            context["service"] = service

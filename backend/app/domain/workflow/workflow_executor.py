# backend/app/domain/workflow/workflow_executor.py
from typing import Dict, Any
from app.schemas.workflow_schemas import WorkflowDAGSchema
from app.adapters.h2o_adapter import H2OHttpAdapter
from app.adapters.mlflow_adapter import MLflowAdapter
import os
import tempfile


class WorkflowExecutor:
    def __init__(self):
        self.h2o = H2OHttpAdapter()
        self.mlflow = MLflowAdapter()

    def execute(self, dag: WorkflowDAGSchema) -> Dict[str, Any]:
        context: Dict[str, Any] = {}
        node_results: Dict[str, Any] = {}

        for node in dag.nodes:
            params = {**node.params, **context}

            if node.type == "h2o_import":
                frame_id = self.h2o.import_file(params["path"])
                result = {"frame_id": frame_id}

            elif node.type == "h2o_list_frames":
                frames = self.h2o.list_frames()
                result = {"frames": frames}
            
            elif node.type == "h2o_parse_setup":
                parseSetup = self.h2o.parse_setup(params["source_frames"])
                result = {"parse_setup": parseSetup}

            elif node.type == "h2o_parse":
                parse = self.h2o.parse(destination_frame=params["destination_frame"], 
                                       parse_setup=context["parse_setup"])
                result = {"parse": parse}
            
            elif node.type == "h2o_split_frame":
                destination_frames = self.h2o.split_frame(
                    dataset=params["dataset"],
                    ratios=params["ratios"],
                    destination_frames=params["destination_frames"],
                    seed=params["seed"])
                result = {"destination_frames": destination_frames}

            elif node.type == "h2o_prep":
                result = self.h2o.standardize(params)

            elif node.type == "h2o_pca":
                result = self.h2o.pca(params)

            elif node.type == "h2o_train":
                algo = params["algo"]
                train_params = params["train_params"]
                result = self.h2o.train(algo, train_params)

            elif node.type == "h2o_eval":
                result = self.h2o.evaluate(params["model_id"], params["frame_id"])

            elif node.type == "h2o_predict":
                result = self.h2o.predict(params["model_id"], params["frame_id"])

            elif node.type == "h2o_export":
                tmp_dir = tempfile.gettempdir()
                model_id = params["model_id"]
                path = os.path.join(tmp_dir, f"{model_id}.zip")
                result = self.h2o.download_model(model_id, path)

            elif node.type == "mlflow_log":
                run_id = self.mlflow.log_model_artifact(
                    params["model_path"],
                    params=params.get("mlflow_params"),
                    metrics=params.get("mlflow_metrics"),
                    tags=params.get("mlflow_tags"),
                )
                result = {"mlflow_run_id": run_id}

            elif node.type == "mlflow_register":
                reg_name = self.mlflow.register_model(
                    params["mlflow_run_id"],
                    params["model_name"],
                )
                result = {"registered_model_name": reg_name}

            elif node.type == "mlflow_transition":
                self.mlflow.transition_stage(
                    params["model_name"],
                    params["version"],
                    params["stage"],
                )
                result = {"stage": params["stage"]}

            elif node.type == "mlflow_get_run":
                info = self.mlflow.get_run_params_metrics(params["mlflow_run_id"])
                result = info

            elif node.type == "mlflow_list_versions":
                versions = self.mlflow.list_model_versions(params["model_name"])
                result = {"versions": versions}

            else:
                result = {"warning": f"unknown node type {node.type}"}

            node_results[node.id] = result
            context.update(result)

        return {"context": context, "node_results": node_results}

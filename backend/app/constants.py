# app/constants.py
"""
系统级符号常量定义，所有可配置项、选项统一在此处声明。
"""

# ==== 通用 ====
DEFAULT_TENANT_ID = "default_tenant"

# ==== 数据相关 ====
DATA_SOURCE_TYPE_DB = "db"

# ==== 工作流节点类型 ====
NODE_TYPE_DATA_SOURCE = "data_source"
NODE_TYPE_PREPROCESS = "preprocess"
NODE_TYPE_FEATURE_ENGINEERING = "feature_engineering"
NODE_TYPE_DATASET_PROCESS = "dataset_process"
NODE_TYPE_TRAIN = "train"
NODE_TYPE_EVALUATE = "evaluate"
NODE_TYPE_REGISTER = "register"
NODE_TYPE_DEPLOY = "deploy"

# ==== 模型相关 ====
ALGO_H2O_GBM = "h2o_gbm"  # 只实现一种 H2O 算法
MLFLOW_EXPERIMENT_PREFIX = "exai"

# ==== 服务状态 ====
SERVICE_STATUS_RUNNING = "running"
SERVICE_STATUS_STOPPED = "stopped"

# ==== 资源管理 ====
DEFAULT_CPU_CORES = 4
DEFAULT_MEMORY_GB = 8.0
DEFAULT_GPU_COUNT = 0

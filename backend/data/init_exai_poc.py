import sqlite3
import json
from datetime import datetime

DB_PATH = "exai_poc.db"


def run():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Initializing SQLite database:", DB_PATH)

    # ------------------------------------------------------------
    # 1. 用户表
    # ------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT,
        created_at TEXT
    );
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO users (id, tenant_id, username, password_hash, created_at)
    VALUES ('user_admin', 'default_tenant', 'admin', NULL, ?);
    """, (datetime.utcnow().isoformat(),))

    # ------------------------------------------------------------
    # 2. 审计日志表
    # ------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenant_id TEXT NOT NULL,
        user_id TEXT,
        action TEXT,
        detail_json TEXT,
        created_at TEXT
    );
    """)

    cursor.execute("""
    INSERT INTO audit_logs (tenant_id, user_id, action, detail_json, created_at)
    VALUES ('default_tenant', 'user_admin', 'system_init', '{"msg":"system initialized"}', ?);
    """, (datetime.utcnow().isoformat(),))

    # ------------------------------------------------------------
    # 3. 工作流定义表
    # ------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workflows (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        definition_json TEXT NOT NULL,
        created_at TEXT,
        updated_at TEXT
    );
    """)

    # ------------------------------------------------------------
    # 4. 工作流运行记录表
    # ------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workflow_runs (
        id TEXT PRIMARY KEY,
        workflow_id TEXT NOT NULL,
        status TEXT NOT NULL,
        started_at TEXT,
        finished_at TEXT,
        context_json TEXT,
        FOREIGN KEY (workflow_id) REFERENCES workflows(id)
    );
    """)

    # ------------------------------------------------------------
    # 5. 模型服务表
    # ------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS model_services (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        name TEXT NOT NULL,
        model_name TEXT NOT NULL,
        model_version TEXT NOT NULL,
        endpoint TEXT NOT NULL,
        status TEXT NOT NULL,
        config_json TEXT,
        created_at TEXT
    );
    """)

    # ------------------------------------------------------------
    # 5. 数据源表
    # ------------------------------------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS data_sources (
    id VARCHAR(64) NOT NULL PRIMARY KEY,
    tenant_id VARCHAR(64) NOT NULL,
    name VARCHAR(128) NOT NULL,
    type VARCHAR(32) NOT NULL,
    config_json TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE INDEX idx_data_sources_tenant_id ON data     _sources (tenant_id);
    """)


    # ------------------------------------------------------------
    # 6. 数据集元数据表
    # ------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datasets (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        source_id TEXT NOT NULL,
        name TEXT NOT NULL,
        table_name TEXT NOT NULL,
        description TEXT,
        created_at TEXT
    );
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO datasets (id, tenant_id, source_id, name, table_name, description, created_at)
    VALUES ('iris', 'default_tenant', 'local_db', 'Iris 数据集', 'demo_iris', 'Iris POC dataset', ?);
    """, (datetime.utcnow().isoformat(),))

    # ------------------------------------------------------------
    # 7. Iris 物理数据表
    # ------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS demo_iris (
        sepal_length REAL,
        sepal_width REAL,
        petal_length REAL,
        petal_width REAL,
        species TEXT
    );
    """)

    iris_rows = [
        (5.1, 3.5, 1.4, 0.2, 'setosa'),
        (4.9, 3.0, 1.4, 0.2, 'setosa'),
        (6.2, 2.8, 4.8, 1.8, 'virginica'),
        (5.9, 3.0, 5.1, 1.8, 'virginica'),
        (6.7, 3.1, 4.4, 1.4, 'versicolor'),
        (5.6, 2.5, 3.9, 1.1, 'versicolor'),
        (5.0, 3.4, 1.5, 0.2, 'setosa'),
        (6.3, 3.3, 6.0, 2.5, 'virginica'),
        (5.8, 2.7, 5.1, 1.9, 'virginica'),
        (6.1, 2.8, 4.0, 1.3, 'versicolor'),
    ]

    cursor.executemany("""
    INSERT INTO demo_iris (sepal_length, sepal_width, petal_length, petal_width, species)
    VALUES (?, ?, ?, ?, ?);
    """, iris_rows)

    # ------------------------------------------------------------
    # 8. 工作流模板表
    # ------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workflow_templates (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        category TEXT,
        definition_json TEXT NOT NULL,
        created_at TEXT
    );
    """)

    template_definition = {
        "nodes": [
            {
                "id": "n1",
                "type": "data_source",
                "name": "数据源",
                "params": {"dataset_ref": "iris"},
                "upstream_ids": []
            },
            {
                "id": "n2",
                "type": "train",
                "name": "训练模型",
                "params": {
                    "target_column": "species",
                    "feature_columns": [
                        "sepal_length",
                        "sepal_width",
                        "petal_length",
                        "petal_width"
                    ],
                    "experiment_name": "iris_exp",
                    "algo_params": {"ntrees": 20, "max_depth": 5}
                },
                "upstream_ids": ["n1"]
            },
            {
                "id": "n3",
                "type": "register",
                "name": "注册模型",
                "params": {"model_name": "iris_model"},
                "upstream_ids": ["n2"]
            },
            {
                "id": "n4",
                "type": "deploy",
                "name": "部署模型",
                "params": {},
                "upstream_ids": ["n3"]
            }
        ]
    }

    cursor.execute("""
    INSERT OR IGNORE INTO workflow_templates (
        id, tenant_id, name, description, category, definition_json, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        "tpl_classification",
        "default_tenant",
        "分类模型模板",
        "数据源 → 训练 → 注册 → 部署",
        "classification",
        json.dumps(template_definition, ensure_ascii=False),
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()

    print("Initialization completed successfully.")


if __name__ == "__main__":
    run()

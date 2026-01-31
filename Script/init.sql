CREATE TABLE demo_iris (
    sepal_length FLOAT,
    sepal_width FLOAT,
    petal_length FLOAT,
    petal_width FLOAT,
    species VARCHAR(32)
);
INSERT INTO demo_iris
VALUES (5.1, 3.5, 1.4, 0.2, 'setosa'),
    (4.9, 3.0, 1.4, 0.2, 'setosa'),
    (6.2, 2.8, 4.8, 1.8, 'virginica'),
    (5.9, 3.0, 5.1, 1.8, 'virginica'),
    (6.7, 3.1, 4.4, 1.4, 'versicolor'),
    (5.6, 2.5, 3.9, 1.1, 'versicolor'),
    (5.0, 3.4, 1.5, 0.2, 'setosa'),
    (6.3, 3.3, 6.0, 2.5, 'virginica'),
    (5.8, 2.7, 5.1, 1.9, 'virginica'),
    (6.1, 2.8, 4.0, 1.3, 'versicolor');
INSERT INTO datasets (
        id,
        tenant_id,
        source_id,
        name,
        table_name,
        description,
        created_at
    )
VALUES (
        'iris',
        'default_tenant',
        'local_db',
        'Iris 数据集',
        'demo_iris',
        'Iris POC',
        NOW()
    );
INSERT INTO workflow_templates (
        id,
        tenant_id,
        name,
        description,
        category,
        definition_json,
        created_at
    )
VALUES (
        'tpl_classification',
        'default_tenant',
        '分类模型模板',
        '数据源 → 训练 → 注册 → 部署',
        'classification',
        '{
    "nodes": [
      {
        "id": "n1",
        "type": "data_source",
        "name": "数据源",
        "params": { "dataset_ref": "iris" },
        "upstream_ids": []
      },
      {
        "id": "n2",
        "type": "train",
        "name": "训练模型",
        "params": {
          "target_column": "species",
          "feature_columns": ["sepal_length","sepal_width","petal_length","petal_width"],
          "experiment_name": "iris_exp",
          "algo_params": { "ntrees": 20, "max_depth": 5 }
        },
        "upstream_ids": ["n1"]
      },
      {
        "id": "n3",
        "type": "register",
        "name": "注册模型",
        "params": { "model_name": "iris_model" },
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
  }',
        NOW()
    );
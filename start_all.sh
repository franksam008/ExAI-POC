#!/usr/bin/env bash

set -e

echo "=============================="
echo " ExAI POC - 自动化启动脚本"
echo "=============================="

# -----------------------------
# 1. 启动 MLflow Tracking Server
# -----------------------------
echo "[1/4] 启动 MLflow Tracking Server..."

MLFLOW_BACKEND="sqlite:///mlflow.db"
MLFLOW_ARTIFACTS="./mlruns"

if [ ! -d "mlruns" ]; then
  mkdir mlruns
fi

nohup mlflow server \
  --backend-store-uri ${MLFLOW_BACKEND} \
  --default-artifact-root ${MLFLOW_ARTIFACTS} \
  --host 0.0.0.0 \
  --port 5000 \
  > mlflow.log 2>&1 &

echo "MLflow 已启动：http://localhost:5000"

# -----------------------------
# 2. 启动 H2O
# -----------------------------
echo "[2/4] 启动 H2O..."

nohup java -jar h2o.jar \
  > h2o.log 2>&1 &

echo "H2O 已启动：http://localhost:54321"

# -----------------------------
# 3. 启动 FastAPI 后端
# -----------------------------
echo "[3/4] 启动 FastAPI 后端..."

cd backend
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 \
  > ../fastapi.log 2>&1 &

cd ..
echo "FastAPI 已启动：http://localhost:8000"

# -----------------------------
# 4. 启动前端
# -----------------------------
echo "[4/4] 启动前端..."

cd frontend
nohup npm run dev \
  > ../frontend.log 2>&1 &

cd ..
echo "前端已启动：http://localhost:5173"

echo "=============================="
echo " ExAI POC 已全部启动完成！"
echo "=============================="

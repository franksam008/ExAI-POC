# app/schemas/monitor_schemas.py
from pydantic import BaseModel

class MetricPointSchema(BaseModel):
    timestamp: str
    qps: float
    latency_ms: float
    error_rate: float

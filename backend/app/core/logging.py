# app/core/logging.py
import logging

"""
统一日志配置：
- POC：简单配置 root logger
"""

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )

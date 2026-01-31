# app/adapters/metadata_adapter.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List

"""
外部元数据平台适配器：
- POC：不调用真实平台，返回固定结构
"""

class MetadataClient(ABC):
    @abstractmethod
    def list_data_sources(self) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    def list_datasets(self, source_id: str) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    def get_dataset_schema(self, dataset_id: str) -> Dict[str, Any]:
        ...

    @abstractmethod
    def get_dataset_profile(self, dataset_id: str) -> Dict[str, Any]:
        ...


class DummyMetadataClient(MetadataClient):
    """
    POC 实现：返回固定数据，实际项目中可对接真实元数据平台。
    """

    def list_data_sources(self) -> List[Dict[str, Any]]:
        return [{"id": "local_db", "name": "本地数据库", "type": "db"}]

    def list_datasets(self, source_id: str) -> List[Dict[str, Any]]:
        # 实际可调用 DB / 元数据平台，这里交给 data_api 直接查 DB
        return []

    def get_dataset_schema(self, dataset_id: str) -> Dict[str, Any]:
        return {"id": dataset_id, "columns": []}

    def get_dataset_profile(self, dataset_id: str) -> Dict[str, Any]:
        return {}

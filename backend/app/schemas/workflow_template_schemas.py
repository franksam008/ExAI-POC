from pydantic import BaseModel
from typing import Any, Dict, List, Optional

class WorkflowTemplateSchema(BaseModel):
    id: str
    name: str
    description: Optional[str]
    category: Optional[str]
    definition: Dict[str, Any]


class WorkflowTemplateCreateSchema(BaseModel):
    name: str
    description: Optional[str]
    category: Optional[str]
    definition: Dict[str, Any]

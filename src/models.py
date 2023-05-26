import uuid
from typing import Optional
from pydantic import BaseModel, Field

class Bill(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    payerid: str
    receiverid: str
    paydate: str

class BillUpdate(BaseModel):
    id: str = Field(alias="_id")
    payerid: Optional[str]
    receiverid: Optional[str]
    paydate: Optional[str]

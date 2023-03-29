from pydantic import BaseModel

class BillBase(BaseModel):
    billid: str
    payerid: str
    receiverid: str
    paydate: str

    class Config:
        orm_mode = True

class BillCreate(BillBase):
    pass
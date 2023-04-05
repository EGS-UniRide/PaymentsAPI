from sqlalchemy import Column, String, Integer

from .database import Base


class Bill(Base):
    __tablename__ = "bills"

    billid = Column(Integer, primary_key=True, index=True, autoincrement=True, default=None)
    payerid = Column(String, nullable=False)
    receiverid = Column(String, nullable=False)
    paydate = Column(String, nullable=False)

from sqlalchemy import Column, String

from .database import Base


class Bill(Base):
    __tablename__ = "bills"

    billid = Column(String, primary_key=True, index=True)
    payerid = Column(String, nullable=False)
    receiverid = Column(String, nullable=False)
    paydate = Column(String, nullable=False)

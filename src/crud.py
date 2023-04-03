from sqlalchemy.orm import Session

from . import models, schemas

def get_bill_by_bill_id(db: Session, bill_id: str):
    return db.query(models.Bill).filter(models.Bill.billid == bill_id).first()

def get_bill_by_payer_id(db: Session, payer_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.Bill).filter(models.Bill.payerid == payer_id).offset(skip).limit(limit).all()

def get_bills(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Bill).offset(skip).limit(limit).all()

def delete_bill(db: Session, bill_id: str):
    bill = db.query(models.Bill).filter(models.Bill.billid == bill_id).delete()
    db.commit()
    return bill



def create_bill(db: Session, bill: schemas.BillCreate):
    db_bill = models.Bill(billid=bill.billid, payerid= bill.payerid, receiverid=bill.receiverid, paydate=bill.paydate)
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill
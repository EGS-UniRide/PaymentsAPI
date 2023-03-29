from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
import stripe
from sqlalchemy.orm import Session

from . import crud, models, schemas, deps

# This is your test secret API key.
stripe.api_key = 'sk_test_51MgbCTA6JRbT2gXKNmijZDF27Sohjjd8hNaod7hjO7FnIJDMK98Fom4S2tpKjzobi2VnuWxQTlnSulNBpUk0vtd500F4ilsDKu'

router = APIRouter(
    prefix="/payments",
    tags=["payments"],
    responses={404: {"description": "Not found"}},
)

YOUR_DOMAIN = 'http://localhost:8000/'
# eu é que tenho q fazer o tracking com uma BD
@router.post('/create-checkout-session/{priceid}')
def create_checkout_session(priceid: str):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, price_1MkrnbA6JRbT2gXKP8tazKO8) of the product you want to sell
                    'price': priceid,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN,
            cancel_url=YOUR_DOMAIN,
        )
    except Exception as e:
        return str(e)

    return RedirectResponse(checkout_session.url, status_code=303)

@router.get("/bills", response_model=list[schemas.BillBase])
async def all_bills(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return crud.get_bills(db=db, skip=skip, limit=limit)

@router.get("/bill/{billid}", response_model=schemas.BillBase)
async def get_bill(billid: str, db: Session = Depends(deps.get_db)):
    db_bill = crud.get_bill_by_bill_id(db=db, bill_id=billid)
    if db_bill != None:
        return db_bill
    else:
        raise HTTPException(status_code=404, detail="Bill not found")

@router.post("/bill")
async def post_bill(bill: schemas.BillCreate, db: Session = Depends(deps.get_db)):
    db_bill = crud.get_bill_by_bill_id(db, bill_id=bill.billid)
    if db_bill:
        raise HTTPException(status_code=400, detail="Bill already registered")
    return crud.create_bill(db=db, bill=bill)

@router.delete("/bill/{billid}")
async def del_bill(billid: str, db: Session = Depends(deps.get_db)):
    db_bill = crud.get_bill_by_bill_id(db, bill_id=billid)
    if db_bill != None:
        return crud.delete_bill(db, bill_id=billid)
    else:
        raise HTTPException(status_code=404, detail="Bill not found")
    
@router.put("/bill/{billid}")
async def put_bill(billid: str, bill: schemas.BillCreate, db: Session = Depends(deps.get_db)):
    db_bill = crud.get_bill_by_bill_id(db, bill_id=billid)
    if db_bill != None:
        crud.delete_bill(db, bill_id=billid)
        return crud.create_bill(db=db, bill=bill)
    else:
        raise HTTPException(status_code=404, detail="Bill not found")

from fastapi import APIRouter, Depends, HTTPException, Body, Request, Response, status
from fastapi.responses import RedirectResponse
import stripe
from sqlalchemy.orm import Session
from src import models
from fastapi.encoders import jsonable_encoder

# This is your test secret API key.
stripe.api_key = 'sk_test_51MgbCTA6JRbT2gXKNmijZDF27Sohjjd8hNaod7hjO7FnIJDMK98Fom4S2tpKjzobi2VnuWxQTlnSulNBpUk0vtd500F4ilsDKu'

router = APIRouter(
    prefix="/payments",
    tags=["payments"],
    responses={404: {"description": "Not found"}},
)

YOUR_DOMAIN = 'http://localhost:8000/'

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

    print(checkout_session.url)

    return RedirectResponse(checkout_session.url, status_code=303)


@router.get("/bills", response_description="List all Bills", response_model=list[models.Bill])
async def list_books(request: Request):
    bills = list(request.app.database["bills"].find(limit=100))
    return bills

@router.get("/bills/{userid}", response_description="List all Bills of a given user", response_model=list[models.Bill])
async def list_books(userid: str, request: Request):
    bills = list(request.app.database["bills"].find({"payerid": userid}, limit=100))
    return bills

@router.get("/bill/{billid}", response_description="Get a single bill by id", response_model=models.Bill)
async def get_bill(billid: str, request: Request):
    if (bill := request.app.database["bills"].find_one({"_id": billid})) is not None:
        return bill
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bill with ID {billid} not found")

@router.put("/bill/{billid}", response_description="Update a bill", response_model=models.Bill)
async def put_bill(billid: str, request: Request, bill: models.BillUpdate = Body(...)):
    bill = {k: v for k, v in bill.dict().items() if v is not None}
    if len(bill) >= 1:
        update_result = request.app.database["bills"].update_one(
            {"_id": billid}, {"$set": bill}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bill with ID {billid} not found")

    if (
        existing_bill := request.app.database["bills"].find_one({"_id": billid})
    ) is not None:
        return existing_bill

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bill with ID {billid} not found")

@router.post("/bill")
async def post_bill(request: Request, bill: models.Bill = Body(...)):
    bill = jsonable_encoder(bill)
    new_bill = request.app.database["bills"].insert_one(bill)
    created_bill = request.app.database["bills"].find_one(
        {"_id": new_bill.inserted_id}
    )

    return created_bill

@router.delete("/bill/{billid}", response_description="Delete a bill")
async def delete_book(billid: str, request: Request, response: Response):
    delete_result = request.app.database["bills"].delete_one({"_id": billid})
    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bill with ID {billid} not found")

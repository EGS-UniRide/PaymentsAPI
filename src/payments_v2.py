from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import stripe

# This is your test secret API key.
stripe.api_key = 'sk_test_51MgbCTA6JRbT2gXKNmijZDF27Sohjjd8hNaod7hjO7FnIJDMK98Fom4S2tpKjzobi2VnuWxQTlnSulNBpUk0vtd500F4ilsDKu'

router = APIRouter(
    prefix="/v2",
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

    return RedirectResponse(checkout_session.url, status_code=303)

import stripe
stripe.api_key = "sk_test_51MgbCTA6JRbT2gXKNmijZDF27Sohjjd8hNaod7hjO7FnIJDMK98Fom4S2tpKjzobi2VnuWxQTlnSulNBpUk0vtd500F4ilsDKu"

stripe.Account.create(
  country="US",
  type="express",
  capabilities={"card_payments": {"requested": True}, "transfers": {"requested": True}},
  business_type="individual",
  business_profile={"url": ""},
)
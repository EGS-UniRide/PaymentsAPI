from fastapi import FastAPI
from pydantic import BaseModel

class Bill(BaseModel):
    billid: str
    payerid: str
    receiverid: str
    limitDate: str
    paydate: str | None = ""

app = FastAPI()

b1 = Bill(billid="0", payerid="12345", receiverid="12346", limitDate="2023-12-27 08:26:49", paydate="2023-12-20 09:00:00")
b2 = Bill(billid="1", payerid="12333", receiverid="12348", limitDate="2023-12-26 09:26:49", paydate="2023-12-21 12:00:00")
b3 = Bill(billid="2", payerid="12222", receiverid="12349", limitDate="2023-12-25 10:26:49", paydate="2023-12-22 11:00:00")

bills = {   b1.billid : b1,
            b2.billid : b2,
            b3.billid : b3}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/bills")
async def all_bills():
    return bills

@app.get("/bill/{billid}")
async def get_bill(billid: str):
    if billid in bills:
        return bills[billid]
    else:
        return {"bill not found"}
    
@app.post("/bill")
async def post_bill(bill: Bill):
    bills[bill.billid] = bill
    return bill

@app.delete("/bill/{billid}")
async def del_bill(billid: str):
    if billid in bills:
        bills.pop(billid)
        return {"bill deleted successfully"}
    else:
        return {"bill not found"}
    
@app.put("/bill/{billid}")
async def put_bill(billid: str, bill: Bill):
    if billid in bills:
        bills[billid] = bill
        return {"bill updated successfully"}
    else:
        return {"bill not found"}
# PaymentsAPI
Payments API

# Create Virtual Environment
```
$ python3 -m venv env
$ source env/bin/activate
```

# Install
```
$ pip install -r requirements.txt
```

# How to run

While in the API directory type in the terminal `$ uvicorn paymentsAPI:app --reload` to launch the API. 

Then you can go to the main route: http://127.0.0.1:8000/, if you are greeted with "{"message":"Hello World"}" the app is running successfully.

To test this API I recommend using [Postman](https://www.postman.com/) to test each endpoint individually.

The docs are available at: https://app.swaggerhub.com/apis-docs/RLMARTINS740/BillsAPI/1.0.0 and in http://127.0.0.1:8000/docs .

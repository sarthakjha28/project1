from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from db import get_connection
app = FastAPI()

# do not remove this below code it is the framework
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/save-user")
async def save_user(request:Request):
    data = await request.json()
    firstname= data.get("firstname","")
    lastname= data.get("lastname","")
    email= data.get("email","")
    phone= data.get("phone","")
    password= data.get("password","")
    gender= data.get("gender","") 
    dob= data.get("dob","")
    age= data.get("age","")
    department= data.get("department","")
    Joining_date= data.get("Joining_date","")

    if not firstname:
        return{"status":False,"message":"Firstname is mandtory !!!"}
    
    if not email or "@" not in email or "." not in email:
        return{"status":False,"message":"CHECK YOUR EMAIL AGAIN !!!" }

    if not phone.isdigit(): # check kr rahe hein user ne alphabet ya !,@,# ye sab to nhi daal diya
        return{"status":False,"message":"PHONE MUST BE IN DIGITS !!!"}

    if len(phone)!=10: # check kr rahe hein phone ki length 10 digit se kam to nhi 
        return{"status":False,"message":"PHONE MUST BE IN 10 DIGIT !!!"}
    
    if len(password)<8:
        return{"status":False,"message":"PASSWORD AT LEAST HAVE 8 CHARACTERS !!!"}
    
    if password.isdigit():
        return{"status":False,"message":"Password cannot be only numbers"}
    
    if not age: # age ke baad bracket nhi laga because age is not a function
        return{"status":False,"message":"AGE IS MISSING"}
    
    if not age.isdigit():
        return{"status":False,"message":"AGE CANNOT BE ALPHABET"}
    
    age= int(age)
    if age<0 or age>120:
        return{"status":False,"message":"CHECK YOUR AGE"}
    
    valid_department = ["HR", "IT", "Finance", "Sales"]
    if department not in valid_department:
        return{"status":False,"message":"Invalid department"}
    
    
    conn= get_connection()
    cursor=conn.cursor()

    sql="insert into office (firstname,lastname,email,phone,password,gender,dob,age,department,Joining_date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql,(firstname,lastname,email,phone,password,gender,dob,age,department,Joining_date))

    conn.commit()
    cursor.close()
    conn.close()


    return {"status": True, "message":"user saved successfully"}

@app.get("/")
def home():
    return {"msg": "API office  working"}
#venv\Scripts\activate 
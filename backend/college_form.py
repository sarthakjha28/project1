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
    firstname= data.get("firstname")
    lastname= data.get("lastname")
    date= data.get("date")
    stream= data.get("stream")
    percent10= data.get("percent10")
    percent12= data.get("percent12")
    board10= data.get("board10")
    board12= data.get("board12")
    phone= data.get("phone")
    email=data.get("email")
    father_occupation= data.get("father_occupation")
    mother_occupation= data.get("mother_occupation")

    if not firstname:
        return{"status":False,"message":"firstname is mandtory"}
    
    if not date:
        return{"status":False,"message":"Date is not mentioned"}
    

    if not percent10:
        return {"status": False, "message": "10th percentage is required"}

    if not percent10.isdigit():
        return {"status": False, "message": "Enter valid number"}

    if int(percent10) < 10 or int(percent10) > 100:
        return {"status": False, "message": "Invalid 10th percentage"}
    
    
    if not percent12:
        return {"status": False, "message": "12th percentage is required"}

    if not percent12.isdigit():
        return {"status": False, "message": "Enter valid number"}

    if int(percent12) < 10 or int(percent12) > 100:
        return {"status": False, "message": "Invalid 12th percentage"}
    
    if not phone or not phone.isdigit() or len(phone) != 10:
        return {"status": False, "message": "Enter valid 10 digit phone number"}
    
    if not email or "@" not in email or "." not in email:
        return{"status":False,"message":"Check Your email again"}
    
    conn= get_connection()
    cursor=conn.cursor()

    sql= "insert into college(firstname,lastname,dob,stream,percent10,percent12,board10,board12,phone,email,father_occupation,mother_occupation) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql,(firstname,lastname,date,stream,percent10,percent12,board10,board12,phone,email,father_occupation,mother_occupation))

    conn.commit()
    cursor.close()
    conn.close()
    
    return {"status": True, "message":"user saved successfully"}


@app.get("/")
def home():
    return {"msg": "API college_form is working"}
#venv\Scripts\activate

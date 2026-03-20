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


    firstname = data.get("firstname","")
    lastname  = data.get("lastname","")
    email     = data.get("email","")
    dob      = data.get("dob","")
    age       = data.get("age","")
    time      = data.get("time","")


    if not firstname:
        return{"status":False,"message":"Firstname is mandtory !!!"}
    
    if not email or "@" not in email or "." not in email:
        return{"status":False,"message":"CHECK YOUR EMAIL AGAIN !!!" }
    
    if not dob:
        return{"status":False ,"message":"DOB IS MISSING!!!"}

    if not age :        
        return{"status":False,"message":"AGE IS MISSING"}
    
    if not age.isdigit(): # yaha par age check hua ki digit hai ki string...agar string hua to return
        return{"status":False,"message":"AGE MUST BE IN NUMBER"}
    
    age = int(age)      # yaha pe age agar string ke form mai aya  eg-"12" to usse normal integer mai badla 12 

    if age<0 or age>120:
        return{"status":False,"message":"CHECK YOUR AGE"}

    if not time:
        return{"status": False, "message":"YOU HAVE NOT ENTERED TIME !!!"}    
    


    conn= get_connection()
    cursor=conn.cursor()

    sql="insert into human (firstname,lastname,email,dob,age) values (%s,%s,%s,%s,%s)"
    cursor.execute(sql,(firstname,lastname,email,dob,age))

    conn.commit()
    cursor.close()
    conn.close()


    return {"status": True, "message":"user saved successfully"}    
     


@app.post("/get-user")
async def get_user(request:Request):
    data = await request.json()
   
    id = data["id"]

    conn= get_connection()
    cursor=conn.cursor()

    sql = "select * from human where id = %s"
    cursor.execute(sql, (id,))   
    data = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()


     # Define keys for the dictionary
    keys = ["id","firstname","lastname","email","dob","age"]

    # Convert to dict
    data_dict = dict(zip(keys, data))

    return data_dict


@app.get("/")
def home():
    return {"msg": "API human_reg  working"}
#venv\Scripts\activate
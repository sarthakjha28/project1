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

    society_name = data["society_name"]
    president = data["president"]
    reg_number = data["reg_number"]
    date_of_purchase = data ["date_of_purchase"]
    room_size = data["room_size"]
    house = data["house"]
    city = data["city"]
    pincode = data["pincode"]
    # file = data["file"]
    bank_details = data["bank_details"]

    conn= get_connection()
    cursor=conn.cursor()

    sql= "insert into society(society_name,president,reg_number,date_of_purchase,room_size,house,city,pincode,bank_details)values(%s, %s, %s, %s, %s, %s, %s, %s,%s)"
    cursor.execute(sql,(society_name,president,reg_number,date_of_purchase,room_size,house,city,pincode,bank_details))

    conn.commit()
    cursor.close()
    conn.close()

    return {"message":"user saved successfully"}



@app.post("/get-user")
async def get_user(request:Request):
    data = await request.json()
   
    id = data["id"]

    conn= get_connection()
    cursor=conn.cursor()

    sql = "select * from society where id = %s"
    cursor.execute(sql, (id,))   
    data = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()


     # Define keys for the dictionary
    keys = ["id","society_name","president","reg_number","date_of_purchase","room_size","house","city","pincode","bank_details"]

    # Convert to dict
    data_dict = dict(zip(keys, data))



    return data_dict
@app.get("/")
def home():
    return {"msg": "API society working"}
#venv\Scripts\activate
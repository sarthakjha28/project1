from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from db import get_connection
app = FastAPI()
import json

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

    firstname= data["firstname"]
    lastname= data["lastname"]
    Gender= data["gender"]
    email= data["email"]
    age = data["age"]
    password= data["password"]
    dateofsubmitting= data["dateofsubmitting"]

    subjects = json.dumps(data["subjects"])

    conn= get_connection()
    cursor=conn.cursor()

    sql= "insert into people (firstname,lastname,gender,email,age,password,subjects,dateofsubmitting) values (%s, %s, %s, %s, %s,%s,%s,%s)"
    cursor.execute(sql,(firstname, lastname,Gender,email,age,password,subjects,dateofsubmitting))

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

    sql = "select * from people where id = %s"
    cursor.execute(sql, (id,))
    data = cursor.fetchone()



    conn.commit()
    cursor.close()
    conn.close()


    keys = ['id', 'firstname', 'lastname', 'gender', 'email', 'age','password','subjects','date']

    data_dict = dict(zip(keys, data))

    return data_dict


@app.get("/")
def home():
    return {"msg": "API  3 is working"}

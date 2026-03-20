from fastapi import FastAPI
from pydantic import BaseModel
import random
import smtplib
from email.mime.text import MIMEText
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

otp_store = {}

class EmailRequest(BaseModel):
    email: str

class VerifyRequest(BaseModel):
    email: str
    otp: str


@app.post("/send-otp")
def send_otp(data: EmailRequest):

    otp = str(random.randint(100000, 999999))
    otp_store[data.email] = otp

    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"

    msg = MIMEText(f"Your OTP is {otp}")
    msg["Subject"] = "OTP Verification"
    msg["From"] = sender_email
    msg["To"] = data.email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, data.email, msg.as_string())
    server.quit()

    return {"message": "OTP sent"}


@app.post("/verify-otp")
def verify_otp(data: VerifyRequest):

    if data.email in otp_store and otp_store[data.email] == data.otp:
        return {"message": "OTP Verified"}
    else:
        return {"message": "Invalid OTP"}
    

@app.get("/")
def home():
    return {"msg": "API otp working"}
from pydantic import BaseModel

class User(BaseModel):
    first_name: str
    last_name: str
    gender: str
    dob: str
    marital_status: str

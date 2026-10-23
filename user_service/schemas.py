from pydantic import BaseModel,EmailStr

class UserCreate(BaseModel):
	username: str
	email: EmailStr
	password: str

class UserLogin(BaseModel):
	identifier: str 
	password: str 
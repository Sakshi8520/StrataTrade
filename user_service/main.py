from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session 
from database import get_db
from typing import Annotated
from sqlalchemy import text
from schemas import UserCreate,UserLogin
from security import hash_password,verify_password,create_access_token,decode_token
from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError
from models import User
from config import settings
from fastapi.security import APIKeyCookie
from jwt.exceptions import InvalidTokenError
from revocation import revoke_token

app = FastAPI()

@app.get("/health/db")
def health_db(db: Annotated[Session,Depends(get_db)]):
	result = db.execute(text("SELECT 1"))
	return {"database":"connected","result":result.scalar()}


@app.post("/register/users",status_code=201)
def register_user(user:UserCreate,db:Annotated[Session,Depends(get_db)]):
	
	stmt = select(User).where(
			or_(User.username==user.username,
				User.email==user.email))
	existing_user = db.execute(stmt).scalar_one_or_none()
	if existing_user:
		raise HTTPException(status_code=409,detail="Username or email is already registered")
		
	hashed_password = hash_password(user.password)
	new_user = User(
		username=user.username,
		email=user.email,
		password_hash=hashed_password)
	try:
		db.add(new_user)
		db.commit()
		db.refresh(new_user)
	except IntegrityError:
		db.rollback()
		raise HTTPException(status_code=409,detail="Username or email is already registered")
		return {
		"id":new_user.id,
		"username":new_user.username,
		"email":new_user.email}

@app.post("/login/users",status_code=200)
def login(user:UserLogin,db:Annotated[Session,Depends(get_db)],response:Response):
	stmt = select(User).where(
		or_(User.username==user.identifier,User.email==user.identifier))
	db_user = db.execute(stmt).scalar_one_or_none()
	if not db_user:
		raise HTTPException(status_code=401,detail="Unauthorized access")
	valid_password=verify_password(user.password,db_user.password_hash)
	if not valid_password:
		raise HTTPException(status_code=401,detail="Unauthorized access")
	token = create_access_token(db_user.id)
	response.set_cookie(key="access_token",value=token,httponly=True,secure=settings.COOKIE_SECURE)
	return {
	"id": db_user.id,
	"token":token
	}

cookie_scheme = APIKeyCookie(name="access_token",auto_error=False)
def get_current_user(db:Annotated[Session,Depends(get_db)],token:Annotated[str | None,Depends(cookie_scheme)]):
	if not token:
		raise HTTPException(status_code=401,detail="Unauthorized")
	#if token in redis:
		#raise HTTPException(status_code=401,detail="Unauthorized")
	try:
		payload = decode_token(token)
	except InvalidTokenError:
		raise HTTPException(status_code=401,detail="Unauthorized")
	try:
		user_id = int(payload["sub"])
	except (KeyError, ValueError, TypeError):
		raise HTTPException(status_code=401,detail="Unauthorized")
	if user_id <= 0:
		raise HTTPException(status_code=401,detail="Unauthorized")
	stmt = select(User).where(User.id==user_id)
	user = db.execute(stmt).scalar_one_or_none()
	if not user:
		raise HTTPException(status_code=401,detail="Unauthorized")
	return user

@app.get("/users/me",status_code=200)
def me(user:Annotated[User,Depends(get_current_user)]):
	return {
	"id":user.id,
	"username":user.username,
	"email":user.email}

@app.post("/logout/users",status_code=200)
def logout(token:Annotated[str|None,Depends(cookie_scheme)],response:Response):
	try:
		if token is not None:
			revoke_token(token)
	except InvalidTokenError:
		pass 
	finally:
		response.delete_cookie(key="access_token")
	return {"msg":"Logged out successfully!"}
		
	
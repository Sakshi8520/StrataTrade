from pwdlib import PasswordHash
from config import settings
from datetime import datetime,timedelta,timezone
import jwt
import uuid 

password_hash = PasswordHash.recommended()

def hash_password(password:str) -> str:
	return password_hash.hash(password)

def verify_password(password:str,hashed_password:str) -> bool:
	return password_hash.verify(password,hashed_password)

def create_access_token(user_id:int) -> str:
	expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
	payload = {
	"sub": str(user_id),
	"jti": str(uuid.uuid4()),
	"exp": expires_at
	}
	token = jwt.encode(payload,settings.JWT_SECRET_KEY,algorithm=settings.JWT_ALGORITHM,)
	return token

def decode_token(token:str):
	payload = jwt.decode(token,settings.JWT_SECRET_KEY,algorithms=settings.JWT_ALGORITHM)
	print(payload)
	return payload
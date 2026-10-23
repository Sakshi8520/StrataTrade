import time
from security import decode_token
from jwt.exceptions import InvalidTokenError

def revoke_token(token:str):
	payload = decode_token(token)
	if payload.get("jti") is None:
		raise InvalidTokenError("Token is missing jti")
	jti = payload["jti"]
	if payload.get("exp") is None:
		raise InvalidTokenError("Token is missing exp")
	exp = payload["exp"]
	current_time = time.time()
	ttl = exp - current_time
	#if ttl > 0: 
		#to redis
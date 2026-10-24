import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
from config import settings
import jwt 

@pytest.fixture
def client():
	return TestClient(app)

def test_logout_without_cookie(client):  
	response = client.post("/logout/users")
	assert response.status_code==200
	assert response.json() == {"msg":"Logged out successfully!"}

def test_revocation_function(client):
	with patch("main.revoke_token") as mock_revoke:
		response = client.post("/logout/users",cookies={"access_token":"fake-token"})
		assert response.status_code==200
		mock_revoke.assert_called_once_with("fake-token")

def test_invalid_token(client):
	response = client.post("/logout/users",cookies={"access_token":"not-a-real-token"})
	assert response.status_code==200
	assert response.json() == {"msg":"Logged out successfully!"}

def test_expired_token(client):
	payload = {
	"sub": "1",
	"jti": "test-id",
	"exp":1
	}
	token = jwt.encode(payload,settings.JWT_SECRET_KEY,algorithm=settings.JWT_ALGORITHM)
	response = client.post("/logout/users",cookies={"access_token":token})
	assert response.status_code==200
	assert response.json() == {"msg":"Logged out successfully!"}

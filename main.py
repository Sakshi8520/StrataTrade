from fastapi import FastAPI
from config import settings 
from pydantic import BaseModel, Field
import uuid 
from uuid import UUID 


app = FastAPI(title=settings.APP_NAME)

class OrderRequest(BaseModel):
	symbol: str
	quantity: int = Field(gt=0)

class OrderResponse(BaseModel):
	order_id: UUID 
	symbol: str
	quantity: int
	status: str


@app.get("/health")
def health_check():
	return {"status":"healthy"}


@app.post("/orders", response_model=OrderResponse)
def create_order(order: OrderRequest):
	return {
		"order_id": uuid.uuid4(),
		"symbol": order.symbol,
		"quantity": order.quantity,
		"status": "Pending"}


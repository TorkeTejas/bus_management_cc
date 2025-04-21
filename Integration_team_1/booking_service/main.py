from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4, UUID
import os
import httpx

app = FastAPI()

# Simulating agent service URL
AGENT_SERVICE_URL = os.getenv("AGENT_SERVICE_URL", "http://agent_service:8000")
SALES_SERVICE_URL = os.getenv("SALES_SERVICE_URL", "http://sales_service:8002")

# Mock database for bookings and commissions
bookings_db = {}
commissions_db = {}

class Booking(BaseModel):
    agent_id: UUID
    customer_name: str
    service_type: str
    price: float

class Commission(BaseModel):
    agent_id: UUID
    booking_id: UUID
    commission_percentage: float
    commission_amount: float

@app.post("/bookings")
async def create_booking(booking: Booking):
    # Validate agent exists via Agent Service
    async with httpx.AsyncClient() as client:
        agent_resp = await client.get(f"{AGENT_SERVICE_URL}/agents/{booking.agent_id}")
        if agent_resp.status_code != 200:
            raise HTTPException(status_code=404, detail="Agent not found")

    booking_id = uuid4()
    bookings_db[booking_id] = booking
    commission_amount = booking.price * 0.1  # Example commission 10%
    commission = Commission(
        agent_id=booking.agent_id,
        booking_id=booking_id,
        commission_percentage=10,
        commission_amount=commission_amount,
    )
    commissions_db[booking_id] = commission

    # Record sale in sales service
    async with httpx.AsyncClient() as client:
        sale_data = {"agent_id": str(booking.agent_id), "price": booking.price}
        sale_resp = await client.post(f"{SALES_SERVICE_URL}/sales/record", json=sale_data)
        if sale_resp.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to record sale")

    return {"booking_id": booking_id, "commission_amount": commission_amount}

@app.get("/agents/{agent_id}/bookings")
def get_agent_bookings(agent_id: UUID):
    agent_bookings = [booking for booking in bookings_db.values() if booking.agent_id == agent_id]
    return agent_bookings

@app.get("/agents/{agent_id}/commission")
def get_agent_commission(agent_id: UUID):
    agent_commissions = [commission for commission in commissions_db.values() if commission.agent_id == agent_id]
    return agent_commissions

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import uuid
from datetime import datetime

app = FastAPI(title="Bus Booking Service")

# In-memory storage
bookings = {}

class Booking(BaseModel):
    user_id: str
    bus_id: str
    seat_number: int
    journey_date: str
    status: str = "confirmed"

@app.get("/")
async def root():
    return {"message": "Welcome to Bus Booking Service"}

@app.get("/bookings")
async def get_bookings():
    return list(bookings.values())

@app.post("/bookings")
async def create_booking(booking: Booking):
    booking_id = str(uuid.uuid4())
    booking_dict = booking.dict()
    booking_dict["booking_id"] = booking_id
    booking_dict["created_at"] = datetime.now().isoformat()
    bookings[booking_id] = booking_dict
    return booking_dict

@app.get("/bookings/{booking_id}")
async def get_booking(booking_id: str):
    if booking_id not in bookings:
        raise HTTPException(status_code=404, detail="Booking not found")
    return bookings[booking_id]

@app.delete("/bookings/{booking_id}")
async def cancel_booking(booking_id: str):
    if booking_id not in bookings:
        raise HTTPException(status_code=404, detail="Booking not found")
    booking = bookings[booking_id]
    booking["status"] = "cancelled"
    return booking

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 
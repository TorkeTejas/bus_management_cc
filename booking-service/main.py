#booking service main file
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI(title="Booking Service")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
bookings = []

class Booking(BaseModel):
    user_id: str
    bus_id: str
    seat_number: int
    journey_date: date
    agent_id: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Welcome to Booking Service"}

@app.get("/bookings")
async def get_bookings():
    return bookings

@app.post("/bookings")
async def create_booking(booking: Booking):
    # Check if seat is already booked for the given bus and date
    if any(b.bus_id == booking.bus_id and 
           b.seat_number == booking.seat_number and 
           b.journey_date == booking.journey_date for b in bookings):
        raise HTTPException(status_code=400, detail="Seat already booked")
    
    bookings.append(booking)
    return {"message": "Booking created successfully", "booking": booking}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007) 
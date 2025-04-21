from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import uuid

app = FastAPI(title="Bus Service")

# In-memory storage
buses = {}

class Bus(BaseModel):
    bus_number: str
    source: str
    destination: str
    total_seats: int
    available_seats: int
    departure_time: str
    arrival_time: str
    price: float

# Initialize with some sample buses
sample_buses = [
    {
        "bus_number": "KA01AB1234",
        "source": "Bangalore",
        "destination": "Mysore",
        "total_seats": 40,
        "available_seats": 40,
        "departure_time": "08:00",
        "arrival_time": "12:00",
        "price": 500.00
    },
    {
        "bus_number": "KA02CD5678",
        "source": "Bangalore",
        "destination": "Chennai",
        "total_seats": 45,
        "available_seats": 45,
        "departure_time": "10:00",
        "arrival_time": "18:00",
        "price": 800.00
    }
]

for bus in sample_buses:
    bus_id = str(uuid.uuid4())
    bus["bus_id"] = bus_id
    buses[bus_id] = bus

@app.get("/")
async def root():
    return {"message": "Welcome to Bus Service"}

@app.get("/buses")
async def get_buses():
    return list(buses.values())

@app.get("/buses/{bus_id}")
async def get_bus(bus_id: str):
    if bus_id not in buses:
        raise HTTPException(status_code=404, detail="Bus not found")
    return buses[bus_id]

@app.post("/buses")
async def create_bus(bus: Bus):
    bus_id = str(uuid.uuid4())
    bus_dict = bus.dict()
    bus_dict["bus_id"] = bus_id
    buses[bus_id] = bus_dict
    return bus_dict

@app.put("/buses/{bus_id}/seats")
async def update_seats(bus_id: str, seats: int):
    if bus_id not in buses:
        raise HTTPException(status_code=404, detail="Bus not found")
    bus = buses[bus_id]
    if seats > bus["total_seats"]:
        raise HTTPException(status_code=400, detail="Seats cannot exceed total seats")
    bus["available_seats"] = seats
    return bus

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002) 
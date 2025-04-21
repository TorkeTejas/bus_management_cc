from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI(title="Bus Booking System API Gateway")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service URLs
BUS_BOOKING_URL = os.getenv("BUS_BOOKING_URL", "http://bus-booking:8001")
BUS_SERVICE_URL = os.getenv("BUS_SERVICE_URL", "http://bus-service:8002")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8003")

@app.get("/")
async def root():
    return {"message": "Welcome to Bus Booking System API Gateway"}

# Bus Booking Routes
@app.get("/bookings")
async def get_bookings():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BUS_BOOKING_URL}/bookings")
        return response.json()

@app.post("/bookings")
async def create_booking(booking_data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BUS_BOOKING_URL}/bookings", json=booking_data)
        return response.json()

# Bus Service Routes
@app.get("/buses")
async def get_buses():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BUS_SERVICE_URL}/buses")
        return response.json()

@app.get("/buses/{bus_id}")
async def get_bus(bus_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BUS_SERVICE_URL}/buses/{bus_id}")
        return response.json()

# User Service Routes
@app.post("/users/register")
async def register_user(user_data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{USER_SERVICE_URL}/users/register", json=user_data)
        return response.json()

@app.post("/users/login")
async def login_user(credentials: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{USER_SERVICE_URL}/users/login", json=credentials)
        return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8084) 
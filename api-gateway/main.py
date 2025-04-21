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
AGENT_SERVICE_URL = os.getenv("AGENT_SERVICE_URL", "http://agent-service:8006")
BOOKING_SERVICE_URL = os.getenv("BOOKING_SERVICE_URL", "http://booking-service:8007")

@app.get("/")
async def root():
    return {"message": "Welcome to Bus Booking System API Gateway"}

# Bus Booking Routes
@app.get("/bookings")
async def get_bookings():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BOOKING_SERVICE_URL}/bookings")
        return response.json()

@app.post("/bookings")
async def create_booking(booking_data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BOOKING_SERVICE_URL}/bookings", json=booking_data)
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

# Agent Service Routes
@app.get("/agents")
async def get_agents():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{AGENT_SERVICE_URL}/agents")
        return response.json()

@app.post("/agents/register")
async def register_agent(agent_data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AGENT_SERVICE_URL}/agents/register", json=agent_data)
        return response.json()

@app.post("/agents/login")
async def login_agent(credentials: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AGENT_SERVICE_URL}/agents/login", json=credentials)
        return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8084) 
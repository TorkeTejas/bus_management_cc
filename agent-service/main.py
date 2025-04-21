from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Agent Service")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
agents = []

class Agent(BaseModel):
    username: str
    email: str
    password: str
    full_name: str
    phone_number: str
    agency_name: str

class AgentLogin(BaseModel):
    username: str
    password: str

@app.get("/")
async def root():
    return {"message": "Welcome to Agent Service"}

@app.get("/agents")
async def get_agents():
    return agents

@app.post("/agents/register")
async def register_agent(agent: Agent):
    # Check if username or email already exists
    if any(a.username == agent.username for a in agents):
        raise HTTPException(status_code=400, detail="Username already exists")
    if any(a.email == agent.email for a in agents):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    agents.append(agent)
    return {"message": "Agent registered successfully"}

@app.post("/agents/login")
async def login_agent(credentials: AgentLogin):
    agent = next((a for a in agents if a.username == credentials.username and a.password == credentials.password), None)
    if not agent:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006) 
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4, UUID

app = FastAPI()

agents_db = {}

class Availability(BaseModel):
    days: List[str]
    shift: str

class Agent(BaseModel):
    id: UUID
    name: str
    email: str
    phone: str
    rating: Optional[float] = 0.0
    availability: Optional[Availability] = None

class AgentCreate(BaseModel):
    name: str
    email: str
    phone: str
    availability: Optional[Availability] = None

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    rating: Optional[float] = None
    availability: Optional[Availability] = None

@app.post("/agents", response_model=Agent)
def create_agent(agent: AgentCreate):
    agent_id = uuid4()
    new_agent = Agent(id=agent_id, **agent.dict())
    agents_db[agent_id] = new_agent
    return new_agent

@app.get("/agents", response_model=List[Agent])
def list_agents():
    return list(agents_db.values())

@app.get("/agents/{agent_id}", response_model=Agent)
def get_agent(agent_id: UUID):
    agent = agents_db.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@app.put("/agents/{agent_id}", response_model=Agent)
def update_agent(agent_id: UUID, update: AgentUpdate):
    agent = agents_db.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    update_data = update.dict(exclude_unset=True)
    updated_agent = agent.copy(update=update_data)
    agents_db[agent_id] = updated_agent
    return updated_agent

@app.delete("/agents/{agent_id}")
def delete_agent(agent_id: UUID):
    if agent_id in agents_db:
        del agents_db[agent_id]
        return {"detail": "Agent deleted"}
    raise HTTPException(status_code=404, detail="Agent not found")

@app.get("/agents/{agent_id}/availability", response_model=Availability)
def get_availability(agent_id: UUID):
    agent = agents_db.get(agent_id)
    if not agent or not agent.availability:
        raise HTTPException(status_code=404, detail="Availability not found")
    return agent.availability

@app.put("/agents/{agent_id}/availability", response_model=Availability)
def update_availability(agent_id: UUID, availability: Availability):
    agent = agents_db.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    agent.availability = availability
    agents_db[agent_id] = agent
    return availability

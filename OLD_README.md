# README BEFORE INTEGRATION :
# Bus Booking System Microservices

This is a microservices-based bus booking system that provides a scalable solution for managing bus bookings, bus information, user accounts, and agent operations.

## System Components
- API Gateway (Port 8084)
- Bus Booking Service (Port 8001)
- Bus Service (Port 8002)
- User Service (Port 8003)
- Agent Service (Port 8006)
- Booking Service (Port 8007)

## Prerequisites
- Docker
- Docker Compose
- Linux/Unix environment (for running health check script)

## Architecture
The system follows a microservices architecture with:
- Each service running in its own container
- Services communicating through HTTP
- API Gateway as the single entry point
- Services connected through a dedicated Docker network (bus-network)
- In-memory storage (non-persistent)

## Running the System

1. Clone the repository and navigate to the project root directory:
```bash
cd bus-booking-system
```

2. Build and start all services:
```bash
docker-compose up --build -d
```

3. Check service health (optional):
```bash
chmod +x check_services.sh
./check_services.sh
```

## Available Endpoints

### API Gateway (http://localhost:8084)
- `GET /` - Health check
- `GET /bookings` - List all bookings
- `POST /bookings` - Create a new booking
- `GET /buses` - List all buses
- `POST /users/register` - Register a new user
- `POST /users/login` - User login
- `GET /agents` - List all agents
- `POST /agents/register` - Register a new agent
- `POST /agents/login` - Agent login

### Bus Booking Service (http://localhost:8001)
- `GET /` - Health check
- `GET /bookings` - List all bookings
- `POST /bookings` - Create a new booking

### Bus Service (http://localhost:8002)
- `GET /` - Health check
- `GET /buses` - List all buses

### User Service (http://localhost:8003)
- `GET /` - Health check
- `POST /users/register` - Register a new user
- `POST /users/login` - User login

### Agent Service (http://localhost:8006)
- `GET /` - Health check
- `GET /agents` - List all agents
- `POST /agents/register` - Register a new agent
- `POST /agents/login` - Agent login

### Booking Service (http://localhost:8007)
- `GET /` - Health check
- `GET /bookings` - List all bookings
- `POST /bookings` - Create a new booking

## Sample API Usage

1. Register a new user:
```bash
curl -X POST "http://localhost:8084/users/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "email": "test@example.com",
       "password": "password123",
       "full_name": "Test User",
       "phone_number": "1234567890"
     }'
```

2. Register a new agent:
```bash
curl -X POST "http://localhost:8084/agents/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testagent",
       "email": "agent@example.com",
       "password": "password123",
       "full_name": "Test Agent",
       "phone_number": "1234567890",
       "agency_name": "Test Agency"
     }'
```

3. Create a new booking:
```bash
curl -X POST "http://localhost:8084/bookings" \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "user123",
       "bus_id": "bus456",
       "seat_number": 1,
       "journey_date": "2024-03-20",
       "agent_id": "agent789"
     }'
```

## Integration Details

### Newly Integrated Services

#### Agent Service (Port 8006)
- Dedicated service for managing travel agents
- Features:
  - Agent registration and authentication
  - Agent profile management
  - Agency information tracking
- Endpoints:
  - `/agents/register` - Register new agents
  - `/agents/login` - Agent authentication
  - `/agents` - List all registered agents

#### Booking Service (Port 8007)
- Specialized service for handling booking operations
- Features:
  - Booking creation and management
  - Seat allocation and tracking
  - Integration with agent and user services
- Endpoints:
  - `/bookings` - Create and list bookings
  - Support for both direct user bookings and agent-assisted bookings

### Integration Points
1. API Gateway Integration:
   - Routes all agent-related requests to Agent Service
   - Forwards booking requests to Booking Service
   - Maintains consistent API interface for clients

2. Service Communication:
   - Services communicate through HTTP
   - API Gateway acts as the central router
   - All services are connected through the bus-network

3. Data Flow:
   - User Service → Booking Service: User authentication
   - Agent Service → Booking Service: Agent-assisted bookings
   - Bus Service → Booking Service: Bus availability and seat information

### Health Monitoring
- New health check script (check_services.sh) monitors all services
- Tests endpoints of all integrated services
- Provides real-time status of the entire system

### Deployment
- All services are containerized using Docker
- Services can be deployed independently
- Easy scaling of individual components
- Consistent environment across development and production

## Health Check Script
The repository includes a health check script (`
# Bus Booking System Microservices

This is a microservices-based bus booking system that provides a scalable solution for managing bus bookings, bus information, and user accounts.

## System Components
- API Gateway (Port 8084)
- Bus Booking Service (Port 8001)
- Bus Service (Port 8002)
- User Service (Port 8003)

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
chmod +x vedika.sh
./vedika.sh
```

## Available Endpoints

### API Gateway (http://localhost:8084)
- `GET /` - Health check
- `GET /bookings` - List all bookings
- `POST /bookings` - Create a new booking
- `GET /buses` - List all buses
- `POST /users/register` - Register a new user
- `POST /users/login` - User login

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

2. Login:
```bash
curl -X POST "http://localhost:8084/users/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "password": "password123"
     }'
```

3. View available buses:
```bash
curl "http://localhost:8084/buses"
```

4. Create a booking:
```bash
curl -X POST "http://localhost:8084/bookings" \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "user_id_here",
       "bus_id": "bus_id_here",
       "seat_number": 1,
       "journey_date": "2024-01-01"
     }'
```

## Health Check Script
The repository includes a health check script (`vedika.sh`) that tests all service endpoints and reports their status. The script:
- Tests connectivity to all services
- Verifies endpoint availability
- Reports HTTP status codes
- Supports both GET and POST requests
- Provides visual feedback with ✅ for success and ❌ for failure

## Notes
- This is a development/demo system with non-persistent storage
- All data will be lost when services are restarted
- For production use, consider:
  - Adding persistent database storage
  - Implementing proper authentication and authorization
  - Adding input validation and error handling
  - Implementing logging and monitoring
  - Setting up SSL/TLS for secure communication 
#old end point check script
#!/bin/bash

echo "Checking all service endpoints..."

declare -A services=(
  ["API Gateway"]="http://0.0.0.0:8084"
  ["Bus Booking Service"]="http://0.0.0.0:8001"
  ["Bus Service"]="http://0.0.0.0:8002"
  ["User Service"]="http://0.0.0.0:8003"
)

declare -A endpoints=(
  ["API Gateway"]="/ GET:/bookings POST:/bookings GET:/buses POST:/users/register POST:/users/login"
  ["Bus Booking Service"]="/ GET:/bookings POST:/bookings"
  ["Bus Service"]="/ GET:/buses  GET:/buses"
  ["User Service"]="/ POST:/users/register POST:/users/login"
)

for service in "${!services[@]}"; do
  base_url="${services[$service]}"
  echo ""
  echo "Checking $service at $base_url"

  for endpoint in ${endpoints[$service]}; do
    if [[ $endpoint == *":"* ]]; then
      method=${endpoint%%:*}
      path=${endpoint#*:}
    else
      method="GET"
      path=$endpoint
    fi

    full_url="$base_url$path"
    
    if [ "$method" == "POST" ]; then
      status=$(curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" -d '{"test": "data"}' "$full_url")
    else
      status=$(curl -s -o /dev/null -w "%{http_code}" "$full_url")
    fi

    if [[ "$status" == "200" || "$status" == "201" || "$status" == "422" ]]; then
      echo "✅ $method $path --> HTTP $status"
    else
      echo "❌ $method $path --> HTTP $status"
    fi
  done
done
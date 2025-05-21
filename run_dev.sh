#!/bin/bash
# Development server script for running Django with WebSockets support

# Exit on any error
set -e

echo "Starting Haircat Server in development mode..."

# Install requirements if needed
if [ "$1" == "--install" ] || [ "$2" == "--install" ] || [ "$3" == "--install" ]; then
    echo "Installing dependencies..."
    pip install daphne channels channels-redis
fi

# Set up environment for development mode
export DEBUG=True
export DJANGO_SETTINGS_MODULE=haircat.settings

# Create a temporary settings file with InMemoryChannelLayer
cat > src/haircat/channel_layers_memory.py << EOL
# Channel layers config for development (InMemory)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    },
}
EOL

# Create a temporary settings file with Redis channel layer
cat > src/haircat/channel_layers_redis.py << EOL
# Channel layers config for development (Redis)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}
EOL

# Run migrations if needed
if [ "$1" == "--migrate" ] || [ "$2" == "--migrate" ] || [ "$3" == "--migrate" ]; then
    echo "Running migrations..."
    cd src && python manage.py migrate && cd ..
fi

# Check if we should use Redis
USE_REDIS=false
if [ "$1" == "--redis" ] || [ "$2" == "--redis" ] || [ "$3" == "--redis" ]; then
    USE_REDIS=true
fi

if [ "$USE_REDIS" = true ]; then
    echo "Using Redis channel layer..."
    
    # Check if redis is running
    echo "Checking Redis connection..."
    if ! command -v redis-cli &> /dev/null; then
        echo "Redis client not found. Please install Redis first."
        exit 1
    fi
    
    redis-cli ping > /dev/null 2>&1 || { 
        echo "Redis is not running. Please start Redis first with: redis-server"
        exit 1 
    }
    echo "Redis is running!"
    
    export CHANNEL_LAYERS_MODULE="haircat.channel_layers_redis"
else
    echo "Using InMemory channel layer..."
    export CHANNEL_LAYERS_MODULE="haircat.channel_layers_memory"
fi

# Start the development server with Daphne
echo "Starting development server with Daphne..."
echo "Development server will be running at http://127.0.0.1:8000/"
echo "WebSocket endpoint will be available at ws://127.0.0.1:8000/ws/webhooks/"
echo "Press Ctrl+C to stop the server"
cd src && python -m daphne -b 0.0.0.0 -p 8000 haircat.asgi:application

# Trap Ctrl+C and perform cleanup
trap 'echo "Shutting down..."; rm -f src/haircat/channel_layers_memory.py src/haircat/channel_layers_redis.py; exit 0' INT TERM EXIT 
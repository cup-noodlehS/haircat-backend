# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir daphne channels channels-redis

# Copy project files
COPY . /app/

# Create static files directory
RUN mkdir -p staticfiles

# Collect static files
RUN cd src && python manage.py collectstatic --noinput

# Set the Python path to include the src directory
ENV PYTHONPATH=/app/src

# Set channel layers to use in-memory by default
ENV CHANNEL_LAYERS_MODULE=haircat.channel_layers_memory

# Create channel layers configuration files
RUN echo "# Channel layers config for development (InMemory)" > src/haircat/channel_layers_memory.py \
    && echo "CHANNEL_LAYERS = {" >> src/haircat/channel_layers_memory.py \
    && echo "    \"default\": {" >> src/haircat/channel_layers_memory.py \
    && echo "        \"BACKEND\": \"channels.layers.InMemoryChannelLayer\"" >> src/haircat/channel_layers_memory.py \
    && echo "    }," >> src/haircat/channel_layers_memory.py \
    && echo "}" >> src/haircat/channel_layers_memory.py \
    && echo "# Channel layers config for production (Redis)" > src/haircat/channel_layers_redis.py \
    && echo "CHANNEL_LAYERS = {" >> src/haircat/channel_layers_redis.py \
    && echo "    \"default\": {" >> src/haircat/channel_layers_redis.py \
    && echo "        \"BACKEND\": \"channels_redis.core.RedisChannelLayer\"," >> src/haircat/channel_layers_redis.py \
    && echo "        \"CONFIG\": {" >> src/haircat/channel_layers_redis.py \
    && echo "            \"hosts\": [(\"redis\", 6379)]," >> src/haircat/channel_layers_redis.py \
    && echo "        }," >> src/haircat/channel_layers_redis.py \
    && echo "    }," >> src/haircat/channel_layers_redis.py \
    && echo "}" >> src/haircat/channel_layers_redis.py

# Expose the port
EXPOSE 8000

# Start Daphne server for both HTTP and WebSocket support
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "haircat.asgi:application"]

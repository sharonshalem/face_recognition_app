# Simplified single-container deployment for AWS Elastic Beanstalk
FROM python:3.11-slim

# Install only essential system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    nginx \
    supervisor \
    curl \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir rembg onnxruntime

# Copy application code
COPY backend/ ./backend/
COPY frontend/ /usr/share/nginx/html/

# Create nginx configuration
RUN rm -f /etc/nginx/sites-enabled/default && \
    echo 'server { \n\
    listen 80; \n\
    server_name _; \n\
    location / { \n\
        root /usr/share/nginx/html; \n\
        index index.html; \n\
    } \n\
    location /api/ { \n\
        proxy_pass http://127.0.0.1:5000/; \n\
        proxy_set_header Host $host; \n\
    } \n\
}' > /etc/nginx/sites-enabled/default

# Create supervisor configuration
RUN echo '[supervisord] \n\
nodaemon=true \n\
\n\
[program:nginx] \n\
command=nginx -g "daemon off;" \n\
autostart=true \n\
autorestart=true \n\
\n\
[program:backend] \n\
command=python app.py \n\
directory=/app/backend \n\
autostart=true \n\
autorestart=true' > /etc/supervisor/conf.d/supervisord.conf

# Create known_faces directory
RUN mkdir -p /app/backend/known_faces

# Expose port 80
EXPOSE 80

# Start supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

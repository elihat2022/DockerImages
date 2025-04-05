FROM python:3.12-slim

# Set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip
# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV MONGO="mongodb"
ENV PORT=8080  

# Expose port for the application
EXPOSE $PORT

# Command to run the application (fixed to properly use environment variable)
CMD ["sh", "-c", "uvicorn Lesson1.main:app --host 0.0.0.0 --port $PORT"]
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV MONGO="mongodb"

# Expose port for the application
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "Lesson1.main:app", "--host", "0.0.0.0", "--port", "8000"]
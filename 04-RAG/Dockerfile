FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of application
COPY . .

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Expose port for API if needed
EXPOSE 8000

# Command will come from docker-compose.yml
CMD ["python", "01-rag.py"]

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8000

# Using runserver for development as per typical Django flow, 
# but the website suggests gunicorn for the CMD. 
# I'll use runserver for now to make it easier for the user to see changes.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

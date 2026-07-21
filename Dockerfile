# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install Git (Flask & other dependencies via requirements.txt)
RUN apt-get update && apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Configure Git identity (Q3)
RUN git config --global user.name "Lee Zhen Fong Jonas" && \
    git config --global user.email "2401243@sit.singaporetech.edu.sg"

# Copy only the requirements file first to cache install step
COPY web/requirements.txt .

# Install all dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY web/ .

# Start the Flask app
CMD ["python", "app.py"]
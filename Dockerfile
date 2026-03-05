FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY app/requirements.txt .
RUN pip install --retries=10 --timeout=120 -r requirements.txt

# Copy the rest of the application
COPY app/ .

# Create data directory
RUN mkdir -p /app/data

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]

FROM python:3.9-bullseye

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libportaudio2 \
    libportaudiocpp0 \
    portaudio19-dev \
    libasound-dev \
    libsndfile1-dev \
    ffmpeg

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/call_transcripts
RUN mkdir -p /app/db

# Expose the port the app runs on
EXPOSE 8501
EXPOSE 8000

# Command to run Streamlit
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
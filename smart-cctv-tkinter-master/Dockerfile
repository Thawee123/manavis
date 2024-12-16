# Use the official Python 3.9 slim image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required by OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Clean pip cache to avoid issues
RUN rm -rf /root/.cache/pip

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all necessary files into the container
COPY . .

# Set environment variables (optional, if not passed via .env)
# ENV RTSP_LINK=""
# ENV MONGO_URI=""
# ENV ZONES_FILE=""
# ENV MYDB=""
# ENV MYCOL=""

# Set the default command to run your script
CMD ["python", "easymoneystorezone.py"]

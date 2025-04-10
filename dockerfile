# Use official Python image
FROM python:3.8

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Set Tesseract path (for pytesseract)
ENV TESSERACT_CMD=/usr/bin/tesseract

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose FastAPI port
EXPOSE 30082

# Run FastAPI app using Uvicorn
CMD ["uvicorn", "api.asgi:app", "--host", "0.0.0.0", "--port", "30082"]

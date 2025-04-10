# docker build --no-cache -t fastapi_app .
# docker run -p 8000:8000 fastapi_app

#!/bin/bash

# Build the Docker image without cache
echo "Building Docker image..."
docker build --no-cache -t br_data_extraction .

# Check if the build was successful
if [ $? -eq 0 ]; then
    echo "Build successful. Running the container..."
    docker run -p 30082:30082 br_data_extraction
else
    echo "Build failed. Exiting."
    exit 1
fi

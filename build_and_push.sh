#!/bin/bash

# Function to check the version format
validate_version() {
    if [[ ! "$1" =~ ^v[0-9]+(\.[0-9]+)?$ ]]; then
        echo "Invalid version format. Use format like 'v1', 'v2', or 'v1.1'"
        exit 1
    fi
}

# Prompt the user for a version number
read -p "Enter version number (e.g., v1, v2, v1.1): " VERSION

# Validate the version number
validate_version "$VERSION"

# Build the Docker base image
echo "Building Docker base image..."
docker build -t lead-collector:latest -f Dockerfile.base .
if [ $? -ne 0 ]; then
    echo "Error: Docker build failed."
    exit 1
fi

echo "Tagging the Docker image..."
docker tag lead-collector:latest atishaydev123/lead-collector:$VERSION
if [ $? -ne 0 ]; then
    echo "Error: Failed to tag the image."
    exit 1
fi

echo "Pushing the Docker image to Docker Hub..."
docker push atishaydev123/lead-collector:$VERSION
if [ $? -ne 0 ]; then
    echo "Error: Failed to push the image to Docker Hub."
    exit 1
fi

echo "Verifying the image by pulling it from Docker Hub..."
docker pull atishaydev123/lead-collector:$VERSION
if [ $? -ne 0 ]; then
    echo "Error: Failed to pull the image from Docker Hub."
    exit 1
fi

echo "Docker image v$VERSION successfully built, tagged, pushed, and verified!"

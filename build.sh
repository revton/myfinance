#!/bin/bash
set -e

echo "Starting build for Render deployment..."
echo "Python version: $(python --version)"

# Upgrade pip
pip install --upgrade pip

# Install dependencies directly with pip
pip install -r requirements.txt

echo "Build completed successfully!"
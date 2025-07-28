#!/bin/bash
set -e

echo "Starting Render build script..."
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"

# Upgrade pip to latest version
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements directly with pip
echo "Installing requirements..."
python -m pip install -r requirements.txt

echo "Build completed successfully!"
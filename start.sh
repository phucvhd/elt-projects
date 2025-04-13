#!/bin/bash
# Define the virtual environment name as a constant
VENV_NAME="stock-env"

# Create a virtual environment
python3 -m venv $VENV_NAME

# Activate the virtual environment
source $VENV_NAME/bin/activate

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    # Install dependencies from requirements.txt
    pip install -r requirements.txt
    echo "Dependencies installed successfully."
else
    echo "requirements.txt not found. Skipping dependency installation."
fi

echo "Setup complete. Virtual environment is ready."
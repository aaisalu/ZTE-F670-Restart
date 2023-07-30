#!/bin/bash

# Create the virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the required packages
pip install -r requirements.txt

# Run the Python program
python restart.py

# Deactivate the virtual environment
deactivate

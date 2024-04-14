#!/bin/bash

# Exit script on error
set -e

# Upgrade pip and install required packages
echo "Upgrading pip and installing required packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Run unit tests
echo "Running unit tests..."
python -m unittest discover -s tests -v

# Run coverage analysis
echo "Analyzing code coverage..."
coverage run -m unittest discover -s tests -v
coverage html

# Run the simulation example
echo "Running the stock market simulation..."
python3 -m examples.simulation

echo "Process completed successfully."

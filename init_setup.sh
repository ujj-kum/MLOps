#!/bin/bash
echo [$(date)]: "START"

echo [$(date)]: "Creating virtual environment with Python 3.8" 

# Create virtual environment 
python3 -m venv envName

echo [$(date)]: "Activating virtual environment"

source envName/Scripts/activate

echo [$(date)]: "Installing required packages"

# Install required packages
pip install -r requirements_dev.txt

echo [$(date)]: "END"


# To run the script, execute the following command
# Open terminal -> Git bash
# bash init_setup.sh
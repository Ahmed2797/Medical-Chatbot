#!/bin/bash

# ================================
# Create Project Structure
# ================================

# Root files
touch app.py
touch main.py
touch README.md
touch requirements.txt
touch notex.txt

# Notebooks
touch medical_chatbot.ipynb

# Project package
mkdir -p project/{chatmodel,chunk,data,embed,fronted,load_data,pipeline,prompt,store}

# __init__.py files
touch project/__init__.py
touch project/chatmodel/__init__.py
touch project/chunk/__init__.py
touch project/embed/__init__.py
touch project/load_data/__init__.py
touch project/pipeline/__init__.py
touch project/prompt/__init__.py
touch project/store/__init__.py

# Data
touch project/data

# Frontend files
touch project/fronted


echo "✅ Project structure created successfully"

# bash template.sh

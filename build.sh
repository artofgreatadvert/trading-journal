#!/bin/bash

echo ""
echo "=========================================="
echo "   Trading Journal Build Script (Unix)"
echo "=========================================="
echo ""

echo "Step 1: Creating virtual environment..."
python3 -m venv venv

echo "Step 2: Activating virtual environment..."
source venv/bin/activate

echo "Step 3: Installing dependencies..."
pip install -r requirements.txt

echo "Step 4: Building executable..."
python3 build_exe.py

echo ""
echo "=========================================="
echo "   Build Complete!"
echo "=========================================="
echo ""
echo "Your executable is in: dist/Trading Journal"
echo ""

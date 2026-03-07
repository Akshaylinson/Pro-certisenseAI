@echo off
cd backend
python -m uvicorn certisense_main:app --reload --port 8000

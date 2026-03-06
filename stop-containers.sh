#!/bin/bash

echo "🛑 Stopping CertiSense AI Containers..."

docker stop certisense-backend certisense-frontend
docker rm certisense-backend certisense-frontend

echo "✅ All containers stopped and removed"
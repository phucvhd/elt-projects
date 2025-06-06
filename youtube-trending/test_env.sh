#!/bin/bash

set -e  # Exit on any error

COMMAND=$1

if [[ "$COMMAND" == "up" ]]; then
  echo "🔧 Starting test environment..."
  docker-compose --env-file .env.test -f docker-compose.test.yaml up -d youtube_trending_test_postgres

  echo "⏳ Waiting for PostgreSQL to become healthy..."
  sleep 10

  echo "🗂️ Running Alembic migrations..."
  ENV_PROFILE=.env.test alembic upgrade head

  echo "✅ Test environment is ready."

elif [[ "$COMMAND" == "down" ]]; then
  echo "🧹 Shutting down test environment..."
  docker-compose -f docker-compose.test.yaml down

  echo "✅ Test environment stopped."

else
  echo "❌ Unknown command: $COMMAND"
  echo "Usage: ./test_env.sh [up|down]"
  exit 1
fi

#!/bin/bash

# Docker management script for SaveDriveNow

case "$1" in
  "dev")
    echo "Starting development environment..."
    docker-compose -f docker-compose.dev.yml up --build
    ;;
  "prod")
    echo "Starting production environment..."
    docker-compose -f docker-compose.prod.yml up --build -d
    ;;
  "stop")
    echo "Stopping all containers..."
    docker-compose -f docker-compose.dev.yml down
    docker-compose -f docker-compose.prod.yml down
    ;;
  "build")
    echo "Building Docker image..."
    docker build -t savedrivenow .
    ;;
  "logs")
    echo "Showing logs..."
    docker-compose -f docker-compose.dev.yml logs -f
    ;;
  "shell")
    echo "Opening shell in web container..."
    docker-compose -f docker-compose.dev.yml exec web bash
    ;;
  "migrate")
    echo "Running migrations..."
    docker-compose -f docker-compose.dev.yml exec web python manage.py migrate
    ;;
  "collectstatic")
    echo "Collecting static files..."
    docker-compose -f docker-compose.dev.yml exec web python manage.py collectstatic --noinput
    ;;
  *)
    echo "Usage: $0 {dev|prod|stop|build|logs|shell|migrate|collectstatic}"
    echo ""
    echo "Commands:"
    echo "  dev           - Start development environment"
    echo "  prod          - Start production environment"
    echo "  stop          - Stop all containers"
    echo "  build         - Build Docker image"
    echo "  logs          - Show container logs"
    echo "  shell         - Open shell in web container"
    echo "  migrate       - Run Django migrations"
    echo "  collectstatic - Collect static files"
    exit 1
    ;;
esac

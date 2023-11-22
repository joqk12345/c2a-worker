#!/bin/bash

start() {
    echo "Starting the service..."
    uvicorn main:app --reload &
    echo "Service started."
}

stop() {
    echo "Stopping the service..."
    pid=$(lsof -i :8000 | awk 'NR==2 {print $2}')
    if [ -n "$pid" ]; then
        kill "$pid"
        echo "Service stopped."
    else
        echo "No service is currently running."
    fi
}

health() {
    echo "Checking service health..."
    response=$(curl -s http://127.0.0.1:8000/api/state)
    state=$(echo "$response" | awk -F'"state":"' '{print $2}' | awk -F'"' '{print $1}')
    echo "Service state: $state"
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    health)
        health
        ;;
    *)
        echo "Usage: $0 {start|stop|health}"
        exit 1
        ;;
esac

exit 0

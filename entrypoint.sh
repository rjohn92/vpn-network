#!/bin/bash

# Start the Flask app
gunicorn --timeout 120 --bind 0.0.0.0:5000 web.app:app

# Wait for Flask app to start
sleep 5


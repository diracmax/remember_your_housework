#!/bin/bash
export FLASK_ENV=development
FLASK_APP=application.py flask run --host=0.0.0.0 -p 8000
python3 notification.py
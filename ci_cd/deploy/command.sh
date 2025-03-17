#!/bin/bash
alembic upgrade head
gunicorn source.main:app --workers 1 --bind 0.0.0.0:8000 --worker-class uvicorn.workers.UvicornWorker

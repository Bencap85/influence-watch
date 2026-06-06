#!/bin/sh
set -e

python -u -m shared.db.seed
uvicorn main.api.main:app --host 0.0.0.0 --port 8000

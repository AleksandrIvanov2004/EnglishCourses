#!/bin/sh

SCRIPT_DIR=$(dirname "$0")
export PYTHONPATH='/app/src'
alembic upgrade head
python "${SCRIPT_DIR}/main.py"
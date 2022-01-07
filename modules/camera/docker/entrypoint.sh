#!/usr/bin/env bash

WORKERS=${WORKERS:=1}

uvicorn --host 0.0.0.0 --workers $WORKERS __init__:app

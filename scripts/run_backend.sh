#!/usr/bin/env bash

cd "$(dirname "$0")/../backend" || exit 1

source .venv/bin/activate

uvicorn app.main:app --reload

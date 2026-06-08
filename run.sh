#!/bin/bash
set -e

source .venv/bin/activate

export PYTHONPATH=$(pwd)

streamlit run app/streamlit_app.py
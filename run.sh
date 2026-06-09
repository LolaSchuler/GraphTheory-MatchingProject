#!/bin/bash
set -e

source .venv/bin/activate

export PYTHONPATH=$(pwd)

streamlit run app/ui/streamlit_app.py
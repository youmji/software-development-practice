#!/bin/bash

cd "$HOME/devops/week03/qwen-web" || exit 1

source .venv/bin/activate

python chat.py


#!/bin/bash

# Jump to "self" folder
cd "$(dirname "$0")"

# Setup sample .app.env.secret
if [[ ! -f ".env" ]]; then
    echo "INFO: copying sample .env.example"
    cp .env.example .env
fi
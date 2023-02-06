#!/bin/bash
cd "$(dirname "$0")"

# frontend init
docker-compose build
docker compose run --rm frontend sh -c "yarn"

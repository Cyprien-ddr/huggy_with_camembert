#!/usr/bin/env bash
rsync -rv --delete-after --exclude="deploy.sh" --exclude=".git" --exclude=".venv" --exclude="config/database.yml" --exclude="docker-compose.yml"  ./ huggy_camembert@15.236.43.31:production/
ssh huggy_camembert@15.236.43.31 "cd production; source .venv/bin/activate; pip install -r requirements.txt"
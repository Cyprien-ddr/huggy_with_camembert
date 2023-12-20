#!/usr/bin/env bash
rsync -rv --delete-after --exclude="deploy.sh" --exclude=".git" --exclude=".venv" --exclude="config/database.yml" --exclude="docker-compose.yml"  ./ huggy_camembert@13.37.178.168:production/
ssh huggy_camembert@13.37.178.168 "cd production; source .venv/bin/activate; pip install -r requirements.txt"
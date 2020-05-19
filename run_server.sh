#!/usr/bin/env bash
export ENV="dev"

source venv/bin/activate
mysql.server restart

python -m main.app


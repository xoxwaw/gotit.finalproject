#!/usr/bin/env bash
source venv/bin/activate
mysql.server restart
export ENV="test"

pytest
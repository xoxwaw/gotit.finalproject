#!/usr/bin/env bash
source venv/bin/activate
export ENV="test"

coverage run -m pytest
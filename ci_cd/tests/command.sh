#!/bin/bash
coverage run -m pytest -v
coverage json -o coverage/coverage.json

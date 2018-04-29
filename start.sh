#!/bin/bash
service postgresql start
psql -h localhost -U docker -d docker -f ./src/dbscheme.sql
python3 ./src/index.py
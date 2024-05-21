#!/bin/bash

nohup python3 app/manage.py runserver &
python3 api/main.py


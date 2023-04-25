#!/bin/bash

python -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd constructor_telegram_bots
python manage.py makemigrations
python manage.py migrate

#!/bin/bash

python -m venv env
source env/bin/activate

pip install -U pip
pip install -r requirements.txt

SECRET_KEY=$(python scripts/generate_django_secret_key.py)

read -p "Enter Telegram bot username: " TELEGRAM_BOT_USERNAME
read -p "Enter Telegram bot API-Token: " TELEGRAM_BOT_TOKEN
read -p "Enter PostgreSQL database name: " POSTGRESQL_DATABASE_NAME
read -p "Enter PostgreSQL database user: " POSTGRESQL_DATABASE_USER
read -p "Enter PostgreSQL database password: " POSTGRESQL_DATABASE_PASSWORD

cd constructor_telegram_bots

cat << EOF > .env
SECRET_KEY='$SECRET_KEY'
DEBUG=True
DEBUG_ENVIRONMENT=True

TELEGRAM_BOT_USERNAME=$TELEGRAM_BOT_USERNAME
TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN

POSTGRESQL_DATABASE_NAME=$POSTGRESQL_DATABASE_NAME
POSTGRESQL_DATABASE_USER=$POSTGRESQL_DATABASE_USER
POSTGRESQL_DATABASE_PASSWORD=$POSTGRESQL_DATABASE_PASSWORD
EOF

python manage.py compilemessages
python manage.py migrate

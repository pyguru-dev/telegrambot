#!/bin/bash

python -m venv env
source env/bin/activate

pip install -U pip
pip install -r requirements.txt

SECRET_KEY=$(python scripts/generate_django_secret_key.py)

read -p "Enter username Telegram bot: " TELEGRAM_BOT_USERNAME
read -p "Enter API-Token Telegram bot: " TELEGRAM_BOT_TOKEN

cd constructor_telegram_bots

cat << EOF > .env
SECRET_KEY='$SECRET_KEY'
DEBUG=True

TELEGRAM_BOT_USERNAME=$TELEGRAM_BOT_USERNAME
TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
EOF

python manage.py compilemessages --ignore=../env
python manage.py migrate

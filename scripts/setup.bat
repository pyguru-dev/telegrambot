@echo off

python -m venv env
env\Scripts\activate

pip install -U pip
pip install -r requirements.txt

python scripts\generate_django_secret_key.py > secret_key.txt
set /p SECRET_KEY=<secret_key.txt

set /p TELEGRAM_BOT_USERNAME="Enter username Telegram bot: "
set /p TELEGRAM_BOT_TOKEN="Enter API-Token Telegram bot: "

cd constructor_telegram_bots

(
  echo SECRET_KEY='%SECRET_KEY%'
  echo DEBUG=True
  echo.
  echo TELEGRAM_BOT_USERNAME=%TELEGRAM_BOT_USERNAME%
  echo TELEGRAM_BOT_TOKEN=%TELEGRAM_BOT_TOKEN%
) > .env

python manage.py compilemessages --ignore=..\env
python manage.py migrate

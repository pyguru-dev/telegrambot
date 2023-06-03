from constructor_telegram_bots.functions import generate_random_string

from pathlib import Path
import locale
import sys
import os


BASE_DIR = Path(__file__).resolve().parent.parent


DEBUG = True

if sys.argv[0] == 'manage.py':
	if sys.argv[1] == 'test':
		TEST = True
	else:
		TEST = False
else:
	TEST = False


if DEBUG:
	SITE_DOMAIN = 'http://127.0.0.1:8000/'
else:
	SITE_DOMAIN = 'https://constructor.exg1o.org/'

ALLOWED_HOSTS = ['127.0.0.1', 'constructor.exg1o.org']

if TEST is False:
	CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
	CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
	CELERY_ACCEPT_CONTENT = ['application/json']
	CELERY_RESULT_SERIALIZER = 'json'
	CELERY_TASK_SERIALIZER = 'json'


folders = ('data', 'logs',)
for folder in folders:
	if os.path.exists(BASE_DIR / folder) is False:
		os.mkdir(BASE_DIR / folder)


if os.path.exists(BASE_DIR / 'data/secret.key') is False:
	SECRET_KEY = f"django-insecure-{generate_random_string(length=50, chars='abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_')}"
	
	with open(BASE_DIR / 'data/secret.key', 'w') as secret_key_file:
		secret_key_file.write(SECRET_KEY)
else:
	with open(BASE_DIR / 'data/secret.key', 'r') as secret_key_file:
		SECRET_KEY = secret_key_file.read()

if sys.argv[1] not in ['test', 'makemigrations', 'migrate']:
	open(BASE_DIR / 'data/constructor_telegram_bot_api.token', 'a')
	with open(BASE_DIR / 'data/constructor_telegram_bot_api.token', 'r') as constructor_telegram_bot_api_token_file:
		CONSTRUCTOR_TELEGRAM_BOT_API_TOKEN = constructor_telegram_bot_api_token_file.read().replace('\n', '')

	if CONSTRUCTOR_TELEGRAM_BOT_API_TOKEN == '':
		print(f"Enter the Constructor Telegram bot API-token in the file {BASE_DIR / 'data/constructor_telegram_bot_api.token'}!")

		exit()


LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'verbose': {
			'format': '[{asctime}]: {levelname}: {name} > {funcName} || {message}',
			'style': '{',
		},
		'simple': {
			'format': '[{asctime}]: {message}',
			'style': '{',
		},
	},
	'handlers': {
		'console': {
			'level': 'INFO',
			'class': 'logging.StreamHandler',
			'formatter': 'simple',
		},
		'django_info_file': { 
			'level': 'DEBUG',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': BASE_DIR / 'logs/django_info.log',
			'maxBytes': 10485760,
			'backupCount': 10,
			'formatter': 'verbose',
		},
		'django_error_file': { 
			'level': 'WARNING',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': BASE_DIR / 'logs/django_error.log',
			'maxBytes': 10485760,
			'backupCount': 10,
			'formatter': 'verbose',
		},
		'telegram_bots_info_file': {
			'level': 'DEBUG',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': BASE_DIR / 'logs/telegram_bots_info.log',
			'maxBytes': 10485760,
			'backupCount': 10,
			'formatter': 'verbose',
		},
		'telegram_bots_error_file': {
			'level': 'WARNING',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': BASE_DIR / 'logs/telegram_bots_error.log',
			'maxBytes': 10485760,
			'backupCount': 10,
			'formatter': 'verbose',
		},
	},
	'loggers': {
		'django': {
			'handlers': [
				'console',
				'django_info_file',
				'django_error_file',
			],
			'propagate': True,
		},
		'aiogram': {
			'handlers': [
				'telegram_bots_info_file',
				'telegram_bots_error_file',
			],
			'propagate': True,
		},
	},
}


INSTALLED_APPS = [
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.staticfiles',

	'user.apps.UserConfig',
	'telegram_bot.apps.TelegramBotConfig',

	'home.apps.HomeConfig',
	'donation.apps.DonationConfig',
	'personal_cabinet.apps.PersonalCabinetConfig',
	'privacy_policy.apps.PrivacyPolicyConfig',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'constructor_telegram_bots.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [BASE_DIR / 'templates'],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
			],
		},
	}
]


WSGI_APPLICATION = 'constructor_telegram_bots.wsgi.application'


AUTH_USER_MODEL = 'user.User'
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': BASE_DIR / 'data/DataBase.db',
	}
}


LANGUAGE_CODE = 'ru'
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

TIME_ZONE = 'Europe/Tallinn'
USE_I18N = True
USE_TZ = True


STATIC_URL = '/static/'
if DEBUG:
	STATICFILES_DIRS = [
		BASE_DIR / 'static/',
	]
else:
	STATIC_ROOT = BASE_DIR / 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

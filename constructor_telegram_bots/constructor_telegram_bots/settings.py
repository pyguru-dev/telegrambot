from constructor_telegram_bots.functions import generate_random_string

from pathlib import Path
import locale
import sys
import os


BASE_DIR = Path(__file__).resolve().parent.parent


DEBUG = False
TEST = True if sys.argv[1] == 'test' else False


SITE_DOMAIN = 'http://127.0.0.1:8000/'
ALLOWED_HOSTS = ['127.0.0.1']


folders = ('data', 'logs', 'logs/site', 'logs/telegram_bots',)
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

if sys.argv[1] == 'runserver':
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
		'site_info_file': { 
			'level': 'DEBUG',
			'class': 'logging.FileHandler',
			'filename': BASE_DIR / 'logs/site/info.log',
			'formatter': 'verbose',
		},
		'site_error_file': { 
			'level': 'WARNING',
			'class': 'logging.FileHandler',
			'filename': BASE_DIR / 'logs/site/error.log',
			'formatter': 'verbose',
		},
		'telegram_bots_info_file': {
			'level': 'DEBUG',
			'class': 'logging.FileHandler',
			'filename': BASE_DIR / 'logs/telegram_bots/info.log',
			'formatter': 'verbose',
		},
		'telegram_bots_error_file': {
			'level': 'WARNING',
			'class': 'logging.FileHandler',
			'filename': BASE_DIR / 'logs/telegram_bots/error.log',
			'formatter': 'verbose',
		},
	},
	'loggers': {
		'django': {
			'handlers': [
				'console',
				'site_info_file',
				'site_error_file',
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

from django.utils.translation import gettext_lazy as _

from constructor_telegram_bots.functions import generate_random_string

from dotenv import load_dotenv
from pathlib import Path
import sys
import os


BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', f"django-insecure-{generate_random_string(length=50, chars='abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_')}")
DEBUG = os.getenv('DEBUG', 'False') == 'True'

try:
	TEST = sys.argv[0] == 'manage.py' and sys.argv[1] == 'test'
except:
	TEST = False

CONSTRUCTOR_TELEGRAM_BOT_API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CONSTRUCTOR_TELEGRAM_BOT_USERNAME = os.getenv('TELEGRAM_BOT_USERNAME')


SITE_DOMAIN = 'http://127.0.0.1:8000/' if DEBUG else 'https://constructor.exg1o.org/'
ALLOWED_HOSTS = ['127.0.0.1', 'constructor.exg1o.org']


CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'


INSTALLED_APPS = [
	'modeltranslation',
	'ckeditor',

	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',

	'user',
	'telegram_bot',

	'home',
	'team',
	'updates',
	'instruction',
	'donation',
	'personal_cabinet',
	'privacy_policy',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.middleware.locale.LocaleMiddleware'
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
				'django.contrib.messages.context_processors.messages',

				'constructor_telegram_bots.context_processors.add_constructor_telegram_bot_username',
				'team.context_processors.team_members',
				'updates.context_processors.updates',
				'instruction.context_processors.instruction_sections',
				'donation.context_processors.donations',
			],
		},
	}
]


WSGI_APPLICATION = 'constructor_telegram_bots.wsgi.application'


AUTH_USER_MODEL = 'user.User'

if sys.argv[0] == 'manage.py' and sys.argv[1] == 'test':
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.sqlite3',
			'NAME': BASE_DIR / 'DataBase.db',
		},
	}
else:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql',
			'NAME': os.getenv('POSTGRESQL_DATABASE_NAME'), 
			'USER': os.getenv('POSTGRESQL_DATABASE_USER'),
			'PASSWORD': os.getenv('POSTGRESQL_DATABASE_PASSWORD'),
			'HOST': '127.0.0.1', 
			'PORT': '5432',
		},
	}


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LOCALE_PATHS = (BASE_DIR / 'locale',)

# Language
USE_I18N = True
USE_L10N = True

LANGUAGE_CODE = 'ru-ru'
LANGUAGES = (
	('en', _('Английский')),
	('uk', _('Украинский')),
	('ru', _('Русский')),
)
MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'

# Timezone
TIME_ZONE = 'UTC'
USE_TZ = True


STATIC_URL = '/static/'
if DEBUG:
	STATICFILES_DIRS = [
		BASE_DIR / 'static/',
	]
else:
	STATIC_ROOT = BASE_DIR / 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


if os.path.exists(BASE_DIR / 'logs') is False:
	os.mkdir(BASE_DIR / 'logs')

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
			'level': 'INFO',
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

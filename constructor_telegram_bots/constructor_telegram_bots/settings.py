from pathlib import Path
from dotenv import load_dotenv
import sys
import os


BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = bool(os.getenv('DEBUG'))

if SECRET_KEY is None:
	SECRET_KEY = 'django-insecure-zXK4D%xx5Mv!L#FS10xU6p(Ztq3HvQA&#CKvt0Kd%Tn&9H1YKa'

if DEBUG is None:
	DEBUG = True

CONSTRUCTOR_TELEGRAM_BOT_API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CONSTRUCTOR_TELEGRAM_BOT_USERNAME = os.getenv('TELEGRAM_BOT_USERNAME')


if sys.argv[0] == 'manage.py':
	if sys.argv[1] == 'test':
		TEST = True
	else:
		TEST = False
else:
	TEST = False


SITE_DOMAIN = 'http://127.0.0.1:8000/' if DEBUG else 'https://constructor.exg1o.org/'
ALLOWED_HOSTS = ['127.0.0.1', 'constructor.exg1o.org']


CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'


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
	'django.contrib.messages',
	'django.contrib.staticfiles',

	'user',
	'telegram_bot',

	'home',
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
			],
		},
	}
]


WSGI_APPLICATION = 'constructor_telegram_bots.wsgi.application'


AUTH_USER_MODEL = 'user.User'
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': BASE_DIR / 'DataBase.db',
	}
}


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale/'), )

# Language
USE_I18N = True
USE_L10N = True

LANGUAGE_CODE = 'ru-ru'
gettext = lambda s: s
LANGUAGES = (
	('en', gettext('Английский')),
	('uk', gettext('Украиский')),
	('pl', gettext('Польский')),
	('ru', gettext('Русский')),
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

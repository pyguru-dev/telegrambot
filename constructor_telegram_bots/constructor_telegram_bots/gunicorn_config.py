from constructor_telegram_bots.settings import BASE_DIR

import os


workers = 1
max_requests = 1000
max_requests_jitter = 100


if os.path.exists(BASE_DIR / 'logs/gunicorn') is False:
    os.mkdir(BASE_DIR / 'logs/gunicorn')

accesslog = str(BASE_DIR / 'logs/gunicorn/info.log')
errorlog = str(BASE_DIR / 'logs/gunicorn/error.log')

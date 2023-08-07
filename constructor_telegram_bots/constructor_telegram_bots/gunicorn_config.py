from .settings import BASE_DIR


workers = 9
max_requests = 1000
max_requests_jitter = 100


capture_output = True
accesslog = str(BASE_DIR / 'logs/gunicorn_info.log')
errorlog = str(BASE_DIR / 'logs/gunicorn_info.log')

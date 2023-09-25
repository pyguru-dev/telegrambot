from celery import shared_task

from .models import User

import time


@shared_task
def update_users_first_name():
	for user in User.objects.all():
		user.update_first_name()
		time.sleep(0.1)

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AccountIconModel(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	icon = models.TextField(default='')
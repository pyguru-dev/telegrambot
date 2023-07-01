from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import User


class Update(models.Model):
	image = models.ImageField(upload_to='static/images/updates/')
	title = models.CharField(_('Заголовок'), max_length=255)
	description = models.TextField(_('Описание'))
	views = models.BigIntegerField(_('Просмотры'), default=0)
	date_added = models.DateTimeField(_('Дата добавления'), auto_now_add=True)

	class Meta:
		db_table = 'update'

		verbose_name = _('Обновление')
		verbose_name_plural = _('Обновления')

class UpdateComment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	update = models.ForeignKey(Update, on_delete=models.CASCADE, related_name='comments')
	text = models.TextField()
	date_added = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'update_comment'

class UpdateLike(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	update = models.ForeignKey(Update, on_delete=models.CASCADE, related_name='likes')
	date_added = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'update_like'

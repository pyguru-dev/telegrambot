from django.core.handlers.wsgi import WSGIRequest

def get_user_data(func):
	def wrapper(*args, **kwargs):
		request: WSGIRequest = args[0]

		kwargs.update(
			{
				'data': {
					'user': {
						'is_authenticated': request.user.is_authenticated,
					},
				},
			}
		)

		return func(*args, **kwargs)
	return wrapper
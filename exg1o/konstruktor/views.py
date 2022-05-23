from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseBadRequest, Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse, render
from konstruktor.models import TelegramBot
import global_methods as GlobalMethods
import json

# Create your views here.
def konstruktor_page(request: WSGIRequest, nickname: str): # Отрисовка konstruktor.html
	if request.user.is_authenticated:
		login = request.user.username
		if nickname == login:
			bots, num = {
				'bots': {}
			}, 1
			for bot in TelegramBot.objects.filter(owner=login).all():
				bots['bots'].update(
					{
						f'bot_{num}': {
							'bot_name': bot.bot_name
						}
					}
				)
				num += 1

			data = GlobalMethods.get_navbar_buttons_data(request)
			data.update(bots)
			return render(request, 'konstruktor.html', data)
		else:
			HttpResponseBadRequest(f'Ваш Login "{login}", а не "{nickname}"')
	else:
		raise Http404('Сначала войдите в акканут!')

def add_bot_page(request: WSGIRequest, nickname: str): # Отрисовка add_bot.html
	if request.user.is_authenticated:
		login = request.user.username
		if nickname == login:
			data = GlobalMethods.get_navbar_buttons_data(request)
			return render(request, 'add_bot.html', data)
		else:
			HttpResponseBadRequest(f'Ваш Login "{login}", а не "{nickname}"')
	else:
		raise Http404('Сначала войдите в акканут!')

@csrf_exempt
def add_bot(request: WSGIRequest, nickname: str): # Добавление бота
	if request.user.is_authenticated:
		login = request.user.username
		if nickname == login:
			if request.method == 'POST':
				data = json.loads(request.body)
				data_items = tuple(data.items())
				if (data_items[0][0], data_items[1][0]) == ('bot_name', 'bot_token'):
					owner, bot_name, bot_token = request.user.username , data['bot_name'], data['bot_token']

					if TelegramBot.objects.filter(owner=owner).count() >= 5 and request.user.groups.filter(name='paid_accounts').exists():
						return HttpResponseBadRequest('У вас уже максимальное количество ботов!')
					elif TelegramBot.objects.filter(owner=owner).count() >= 1 and request.user.groups.filter(name='free_accounts').exists():
						return HttpResponseBadRequest('У вас уже максимальное количество ботов!')
					else:
						bot = TelegramBot(id, owner, bot_name, bot_token)
						bot.save()

						return HttpResponse('Успешное добавление бота.')
				else:
					return HttpResponseBadRequest('В тело запроса переданы неправильные данные!')
			else:
				return HttpResponseBadRequest('Неправильный метод запроса!')
		else:
			HttpResponseBadRequest(f'Ваш Login "{login}", а не "{nickname}"')
	else:
		raise Http404('Сначала войдите в акканут!')
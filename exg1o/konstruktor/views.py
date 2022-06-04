from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse, redirect, render
from konstruktor.models import TelegramBot
import global_functions as GlobalFunctions
import global_decorators as GlobalDecorators
import json

# Create your views here.
def get_bots_data(request: WSGIRequest, nickname: str): # Функция для получения данных о ботах
	bots, num = {
		'bots': []
	}, 1
	for bot in TelegramBot.objects.filter(owner=nickname).all():
		bots['bots'].append(
			{
				'bot_name': bot.bot_name,
				'bot_positsion': 'normal' if num != 5 else 'last',
				'onclick': f"deleteBotButtonClick('{bot.bot_name}', '{request.user.username}');"
			}
		)
		num += 1

	data = GlobalFunctions.get_navbar_buttons_data(request)
	data.update(bots)
	return data

@GlobalDecorators.if_user_authed
def main_konstruktor_page(request: WSGIRequest, nickname: str): # Отрисовка main_konstruktor.html
	data = get_bots_data(request, nickname)
	return render(request, 'main_konstruktor.html', data)

@csrf_exempt
@GlobalDecorators.if_user_authed
def delete_bot(request: WSGIRequest, nickname: str): # Удаление бота
	if request.method == 'POST':
		data = json.loads(request.body)
		data_items = tuple(data.items())
		if (data_items[0][0]) == ('bot_name'):
			bot_name = data['bot_name']
			if TelegramBot.objects.filter(owner=nickname).filter(bot_name=bot_name).exists():
				bot: TelegramBot = TelegramBot.objects.filter(owner=nickname).get(bot_name=bot_name)
				bot.delete()

				return HttpResponse('Успешное удаление бота.')
			else:
				return HttpResponseBadRequest(f'У вас нет бота "{bot_name}"!')
		else:
			return HttpResponseBadRequest('В тело запроса переданы неправильные данные!')
	else:
		return HttpResponseBadRequest('Неправильный метод запроса!')

@GlobalDecorators.if_user_authed
def add_bot_page(request: WSGIRequest, nickname: str): # Отрисовка add_bot.html
	data = GlobalFunctions.get_navbar_buttons_data(request)
	return render(request, 'add_bot.html', data)

@csrf_exempt
@GlobalDecorators.if_user_authed
def add_bot(request: WSGIRequest, nickname: str): # Добавление бота
	if request.method == 'POST':
		data = json.loads(request.body)
		data_items = tuple(data.items())
		if (data_items[0][0], data_items[1][0]) == ('bot_name', 'bot_token'):
			owner, bot_name, bot_token = nickname, data['bot_name'], data['bot_token']

			if TelegramBot.objects.filter(owner=owner).count() >= 5 and request.user.groups.filter(name='paid_accounts').exists():
				return HttpResponseBadRequest('У вас уже максимальное количество ботов!')
			elif TelegramBot.objects.filter(owner=owner).count() >= 1 and request.user.groups.filter(name='free_accounts').exists():
				return HttpResponseBadRequest('У вас уже максимальное количество ботов!')
			else:
				bot: TelegramBot = TelegramBot(id, owner, bot_name, bot_token, json.dumps([], ensure_ascii=False, indent=2))
				bot.save()

				return HttpResponse('Успешное добавление бота.')
		else:
			return HttpResponseBadRequest('В тело запроса переданы неправильные данные!')
	else:
		return HttpResponseBadRequest('Неправильный метод запроса!')

@GlobalDecorators.if_user_authed
def view_konstruktor_bot_page(request: WSGIRequest, nickname: str, bot_name: str): # Отрисовка view_bot_konstruktor.html
	if TelegramBot.objects.filter(owner=nickname).filter(bot_name=bot_name).exists():
		bot = TelegramBot.objects.filter(owner=nickname).get(bot_name=bot_name)
		bot_commands = json.loads(bot.bot_commands)
		data = get_bots_data(request, nickname)
		data.update(
			{
				'bot': {
					'bot_name': bot_name,
					'bot_token': bot.bot_token,
					'bot_commands': bot_commands
				}
			}
		)
		data['bot']['bot_commands'][len(bot_commands) - 1].update(
			{
				'bot_commands_positsion': 'last'
			}
		)
		return render(request, 'view_bot_konstruktor.html', data)
	else:
		return redirect(f'/account/konstruktor/{nickname}/')

@GlobalDecorators.if_user_authed
def add_command_page(request: WSGIRequest, nickname: str, bot_name: str):
	data = GlobalFunctions.get_navbar_buttons_data(request)
	return render(request, 'add_command.html', data)

@csrf_exempt
@GlobalDecorators.if_user_authed
def add_command(request: WSGIRequest, nickname: str, bot_name: str):
	if request.method == 'POST':
		data = json.loads(request.body)
		data_items = tuple(data.items())
		if (data_items[0][0]) == ('command_name'):
			command_name = data['command_name']
			bot = TelegramBot.objects.filter(owner=nickname).get(bot_name=bot_name)
			bot_commands = json.loads(bot.bot_commands)
			bot_commands.append(
				{
					'command_name': command_name
				}
			)
			bot.bot_commands = json.dumps(bot_commands, ensure_ascii=False, indent=2)
			bot.delete()
			bot.save()

			return HttpResponse('Успешное добавление команды.')
		else:
			return HttpResponseBadRequest('В тело запроса переданы неправильные данные!')
	else:
		return HttpResponseBadRequest('Неправильный метод запроса!')
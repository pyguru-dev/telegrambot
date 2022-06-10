from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse, redirect, render
from konstruktor.models import TelegramBotModel, TelegramBotCommandModel
import global_functions as GlobalFunctions
import global_decorators as GlobalDecorators
import global_variable as GlobalVariable
from telegram_bot import TelegramBot
from threading import Thread

# Create your views here.
def get_bots_data(request: WSGIRequest, nickname: str): # Функция для получения данных о ботах
	bots, num = {
		'bots': []
	}, 1
	for bot in TelegramBotModel.objects.filter(owner=nickname).all():
		bots['bots'].append(
			{
				'bot_name': bot.name,
				'bot_positsion': 'normal' if num != 5 else 'last',
				'onclick': f"deleteBotButtonClick('{bot.name}', '{request.user.username}');"
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
@GlobalDecorators.check_request_data_items(needs_items=['bot_name'])
def delete_bot(request: WSGIRequest, nickname: str, data: dict): # Удаление бота
	bot_name = data['bot_name']

	bot = TelegramBotModel.objects.filter(owner=nickname)
	if bot.filter(name=bot_name).exists():
		bot = bot.get(name=bot_name)
		bot.delete()

		for bot_command in TelegramBotCommandModel.objects.filter(owner=nickname).filter(bot_name=bot_name):
			bot_command.delete()

		return HttpResponse('Успешное удаление бота.')
	else:
		return HttpResponseBadRequest(f'У вас нет бота "{bot_name}"!')

@GlobalDecorators.if_user_authed
def add_bot_page(request: WSGIRequest, nickname: str): # Отрисовка add_bot.html
	data = GlobalFunctions.get_navbar_buttons_data(request)
	return render(request, 'add_bot.html', data)

@csrf_exempt
@GlobalDecorators.if_user_authed
@GlobalDecorators.check_request_data_items(needs_items=['bot_name', 'bot_token'])
def add_bot(request: WSGIRequest, nickname: str, data: dict): # Добавление бота
	owner, bot_name, bot_token = nickname, data['bot_name'], data['bot_token']
	if TelegramBotModel.objects.filter(owner=owner).count() >= 5 and request.user.groups.filter(name='paid_accounts').exists():
		return HttpResponseBadRequest('У вас уже максимальное количество ботов!')
	elif TelegramBotModel.objects.filter(owner=owner).count() >= 1 and request.user.groups.filter(name='free_accounts').exists():
		return HttpResponseBadRequest('У вас уже максимальное количество ботов!')
	else:
		bot: TelegramBotModel = TelegramBotModel(id, owner, bot_name, bot_token)
		bot.save()

		return HttpResponse('Успешное добавление бота.')

@GlobalDecorators.if_user_authed
def view_konstruktor_bot_page(request: WSGIRequest, nickname: str, bot_name: str): # Отрисовка view_bot_konstruktor.html
	bot = TelegramBotModel.objects.filter(owner=nickname)
	if bot.filter(name=bot_name).exists():
		bot = bot.get(name=bot_name)

		data = get_bots_data(request, nickname)
		data.update(
			{
				'bot': {
					'bot_name': bot_name,
					'bot_token': bot.token,
					'bot_commands': []
				}
			}
		)
		for bot_command in TelegramBotCommandModel.objects.filter(owner=nickname).filter(bot_name=bot_name):
			data['bot']['bot_commands'].append(
				{
					'command_id': bot_command.id,
					'command_name': bot_command.command_name
				}
			)
		if len(data['bot']['bot_commands']) > 4:
			data['bot']['bot_commands'][-1].update(
				{
					'bot_commands_positsion': 'last'
				}
			)

		return render(request, 'view_bot_konstruktor.html', data)
	else:
		return redirect(f'/account/konstruktor/{nickname}/')

@csrf_exempt
@GlobalDecorators.if_user_authed
def start_bot(request: WSGIRequest, nickname: str, bot_name: str): # Запуск бота
	token = TelegramBotModel.objects.filter(owner=nickname).get(name=bot_name).token
	bot = TelegramBot(nickname, bot_name, token)
	if bot.auth():
		Thread(target=bot.start, daemon=True).start()

		GlobalVariable.online_bots.update(
			{
				nickname: {
					bot_name: bot
				}
			}
		)

		return HttpResponse('Бот успешно запушен.')
	else:
		return HttpResponseBadRequest('Неверный "Token" бота!')

@GlobalDecorators.if_user_authed
def add_command_page(request: WSGIRequest, nickname: str, bot_name: str): # Отрисовка add_command.html
	data = GlobalFunctions.get_navbar_buttons_data(request)
	return render(request, 'add_command.html', data)

@csrf_exempt
@GlobalDecorators.if_user_authed
@GlobalDecorators.check_request_data_items(needs_items=['command_name', 'command', 'command_answer'])
def add_command(request: WSGIRequest, nickname: str, bot_name: str, data: dict): # Добавление команды
	command_name, command, command_answer = data['command_name'], data['command'], data['command_answer']

	bot_command = TelegramBotCommandModel(id, nickname, bot_name, command_name, command, command_answer)
	bot_command.save()

	return HttpResponse('Успешное добавление команды.')

@GlobalDecorators.if_user_authed
def view_command(request: WSGIRequest, nickname: str, bot_name: str, command_id: int): # Отрисовка view_command.html
	bot_command = TelegramBotCommandModel.objects.filter(owner=nickname).filter(bot_name=bot_name)
	if bot_command.filter(id=command_id).exists():
		bot_command = bot_command.get(id=command_id)

		data = GlobalFunctions.get_navbar_buttons_data(request)
		data.update(
			{
				'bot_command': {
					'command_name': bot_command.command_name,
					'command': bot_command.command,
					'command_answer': bot_command.command_answer
				}
			}
		)

		return render(request, 'view_command.html', data)
	else:
		return redirect(f'/account/konstruktor/{nickname}/view_bot/{bot_name}/')

@csrf_exempt
@GlobalDecorators.if_user_authed
@GlobalDecorators.check_request_data_items(needs_items=['command_name', 'command', 'command_answer'])
def save_command(request: WSGIRequest, nickname: str, bot_name: str, command_id: int, data: dict): # Сохранение команды
	command_name, command, command_answer = data['command_name'], data['command'], data['command_answer']

	bot_command = TelegramBotCommandModel.objects.filter(owner=nickname)
	if bot_command.filter(id=command_id).exists():
		bot_command = TelegramBotCommandModel(command_id, nickname, bot_name, command_name, command, command_answer)
		bot_command.save()

		return HttpResponse('Успешное cохранение команды.')
	else:
		return redirect(f'/account/konstruktor/{nickname}/view_bot/{bot_name}/')

@csrf_exempt
@GlobalDecorators.if_user_authed
def delete_command(request: WSGIRequest, nickname: str, bot_name: str, command_id: int): # Удаление команды
	bot_command = TelegramBotCommandModel.objects.filter(owner=nickname)
	if bot_command.filter(id=command_id).exists():
		bot_command = bot_command.get(id=command_id)
		bot_command.delete()

		return HttpResponse('Успешное удаление команды.')
	else:
		return redirect(f'/account/konstruktor/{nickname}/view_bot/{bot_name}/')
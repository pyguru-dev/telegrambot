from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse, redirect, render
from konstruktor.models import TelegramBotModel, TelegramBotLogModel, TelegramBotCommandModel
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
				'bot_id': bot.id,
				'bot_name': bot.name,
				'bot_positsion': 'normal' if num != 5 else 'last',
				'onclick': f"deleteBotButtonClick('{bot.id}', '{bot.name}', '{request.user.username}');"
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
@GlobalDecorators.check_request_data_items(needs_items=['bot_id'])
def delete_bot(request: WSGIRequest, nickname: str, data: dict): # Удаление бота
	bot_id = int(data['bot_id'])

	bot = TelegramBotModel.objects.filter(owner=nickname)
	if bot.filter(id=bot_id).exists():
		bot = bot.get(id=bot_id)
		bot.delete()

		for bot_command in TelegramBotCommandModel.objects.filter(owner=nickname).filter(bot_id=bot_id):
			bot_command.delete()

		return HttpResponse('Успешное удаление бота.')
	else:
		return redirect(f'/account/konstruktor/{nickname}/')

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
		bot = TelegramBotModel(id, owner, bot_name, bot_token)
		bot.save()

		return HttpResponse('Успешное добавление бота.')

@GlobalDecorators.if_user_authed
@GlobalDecorators.check_bot_id
def view_konstruktor_bot_page(request: WSGIRequest, nickname: str, bot_id: int, bot: TelegramBotModel): # Отрисовка view_bot_konstruktor.html
	data = get_bots_data(request, nickname)
	data.update(
		{
			'bot': {
				'name': bot.name,
				'token': bot.token,
				'online': bot.online,
				'commands': [],
				'log': []
			}
		}
	)

	for bot_command in TelegramBotCommandModel.objects.filter(owner=nickname).filter(bot_id=bot_id):
		data['bot']['commands'].append(
			{
				'id': bot_command.id,
				'name': bot_command.command_name
			}
		)
	if len(data['bot']['commands']) > 4:
		data['bot']['commands'][-1].update(
			{
				'bot_command_positsion': 'last'
			}
		)

	for log in TelegramBotLogModel.objects.filter(owner=nickname).filter(bot_id=bot_id):
		data['bot']['log'].append(
			{
				'id': log.id,
				'user_name': log.user_name,
				'user_message': log.user_message
			}
		)
	if len(data['bot']['log']) > 2:
		data['bot']['log'][-1].update(
			{
				'log_data_positsion': 'last'
			}
		)

	return render(request, 'view_bot_konstruktor.html', data)

@csrf_exempt
@GlobalDecorators.if_user_authed
@GlobalDecorators.check_request_data_items(needs_items=['bot_name', 'bot_token'])
@GlobalDecorators.check_bot_id
def save_bot_settings(request: WSGIRequest, nickname: str, bot_id: int, data: dict, bot: TelegramBotModel):
	bot_name, bot_token = data['bot_name'], data['bot_token']

	bot.name = bot_name
	bot.token = bot_token
	bot.save()

	return HttpResponse('Успешное сохрание настроек бота.')

@csrf_exempt
@GlobalDecorators.if_user_authed
@GlobalDecorators.check_bot_id
def start_bot(request: WSGIRequest, nickname: str, bot_id: int, bot: TelegramBotModel): # Запуск бота
	telegram_bot = TelegramBot(nickname, bot_id, bot.token)
	if telegram_bot.auth():
		Thread(target=telegram_bot.start, daemon=True).start()

		bot.online = True
		bot.save()

		GlobalVariable.online_bots.update(
			{
				nickname: {
					bot_id: telegram_bot
				}
			}
		)

		return HttpResponse('Бот успешно запушен.')
	else:
		return HttpResponseBadRequest('Неверный "Token" бота!')

@csrf_exempt
@GlobalDecorators.if_user_authed
@GlobalDecorators.check_bot_id
def stop_bot(request: WSGIRequest, nickname: str, bot_id: int, bot: TelegramBotModel): # Остоновка бота
	telegram_bot = GlobalVariable.online_bots[nickname][bot_id]
	Thread(target=telegram_bot.stop, daemon=True).start()

	bot.online = False
	bot.save()

	del GlobalVariable.online_bots[nickname][bot_id]

	return HttpResponse('Бот успешно остоновлен.')

@GlobalDecorators.if_user_authed
def add_command_page(request: WSGIRequest, nickname: str, bot_id: int): # Отрисовка add_command.html
	data = GlobalFunctions.get_navbar_buttons_data(request)
	return render(request, 'add_command.html', data)

@csrf_exempt
@GlobalDecorators.if_user_authed
@GlobalDecorators.check_bot_id
def clear_log(request: WSGIRequest, nickname: str, bot_id: int, bot: TelegramBotModel): # Очистка логов
	for log in TelegramBotLogModel.objects.filter(owner=nickname).filter(bot_id=bot_id):
		log.delete()

	return HttpResponse('Успешная очистка логов.')

@csrf_exempt
@GlobalDecorators.if_user_authed
@GlobalDecorators.check_request_data_items(needs_items=['command_name', 'command', 'command_answer'])
@GlobalDecorators.check_bot_id
def add_command(request: WSGIRequest, nickname: str, bot_id: int, data: dict, bot: TelegramBotModel): # Добавление команды
	command_name, command, command_answer = data['command_name'], data['command'], data['command_answer']

	bot_command = TelegramBotCommandModel(id, bot_id, nickname, command_name, command, command_answer)
	bot_command.save()

	return HttpResponse('Успешное добавление команды.')

@GlobalDecorators.if_user_authed
@GlobalDecorators.check_bot_id
@GlobalDecorators.check_command_id
def view_command(request: WSGIRequest, nickname: str, bot_id: int, command_id: int, bot: TelegramBotModel, bot_command: TelegramBotCommandModel): # Отрисовка view_command.html
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

@csrf_exempt
@GlobalDecorators.if_user_authed
@GlobalDecorators.check_request_data_items(needs_items=['command_name', 'command', 'command_answer'])
@GlobalDecorators.check_bot_id
@GlobalDecorators.check_command_id
def save_command(request: WSGIRequest, nickname: str, bot_id: int, command_id: int, data: dict, bot: TelegramBotModel, bot_command: TelegramBotCommandModel): # Сохранение команды
	command_name, command, command_answer = data['command_name'], data['command'], data['command_answer']

	bot_command = TelegramBotCommandModel(command_id, bot_id, nickname, command_name, command, command_answer)
	bot_command.save()

	return HttpResponse('Успешное cохранение команды.')

@csrf_exempt
@GlobalDecorators.if_user_authed
@GlobalDecorators.check_bot_id
@GlobalDecorators.check_command_id
def delete_command(request: WSGIRequest, nickname: str, bot_id: str, command_id: int, bot: TelegramBotModel, bot_command: TelegramBotCommandModel): # Удаление команды
	bot_command.delete()
	return HttpResponse('Успешное удаление команды.')
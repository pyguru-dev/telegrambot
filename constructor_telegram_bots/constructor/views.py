from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse, redirect, render
from constructor.models import TelegramBotModel, TelegramBotLogModel, TelegramBotCommandModel
import global_decorators as GlobalDecorators
import global_variable as GlobalVariable
from telegram_bot import TelegramBot
from threading import Thread

# Create your views here.
@GlobalDecorators.get_navbar_data
def get_bots_data(request: WSGIRequest, data: dict):
	data.update(
		{
			'bots': [],
			'user': {
				'username': request.user.username,
				'status': 'Бесплатный' if request.user.groups.get().name == 'free_accounts' else 'Платный'
			}
		}
	)

	num = 1
	for bot in TelegramBotModel.objects.filter(owner_id=request.user.id):
		data['bots'].append(
			{
				'bot_id': bot.id,
				'bot_name': bot.name,
				'onclick': f"deleteBotButtonClick('{bot.id}', '{bot.name}', '{request.user.username}');"
			}
		)
		num += 1

	return data

@GlobalDecorators.if_user_authed
def main_constructor_page(request: WSGIRequest, username: str): # Отрисовка main_constructor.html
	data = get_bots_data(request)
	return render(request, 'main_constructor.html', data)

@csrf_exempt
@GlobalDecorators.if_user_authed
@GlobalDecorators.check_request_data_items(needs_items=['bot_id'])
def delete_bot(request: WSGIRequest, username: str, data: dict): # Удаление бота
	bot_id = int(data['bot_id'])

	bot = TelegramBotModel.objects.filter(owner_id=request.user.id)
	if bot.filter(id=bot_id).exists():
		bot = bot.get(id=bot_id)
		bot.delete()

		return HttpResponse('Успешное удаление бота.')
	else:
		return redirect(f'/constructor/{username}/')

@csrf_exempt
@GlobalDecorators.if_user_authed
@GlobalDecorators.check_max_bots_count_for_account
@GlobalDecorators.get_navbar_data
def add_bot_page(request: WSGIRequest, username: str, data: dict): # Отрисовка add_bot.html
	return render(request, 'add_bot.html', data)

@csrf_exempt
@GlobalDecorators.if_user_authed
@GlobalDecorators.check_request_data_items(needs_items=['bot_name', 'bot_token'])
@GlobalDecorators.check_max_bots_count_for_account
def add_bot(request: WSGIRequest, username: str, data: dict): # Добавление бота
	bot_name, bot_token = data['bot_name'], data['bot_token']

	bot = TelegramBotModel(None, request.user.id, bot_name, bot_token)
	bot.save()

	return HttpResponse('Успешное добавление бота.')

@GlobalDecorators.if_user_authed
@GlobalDecorators.check_bot_id
def view_bot_page(request: WSGIRequest, username: str, bot_id: int, bot: TelegramBotModel): # Отрисовка view_bot_page.html
	data = get_bots_data(request)
	data.update(
		{
			'user': {
				'username': username,
				'status': 'Бесплатный' if request.user.groups.get().name == 'free_accounts' else 'Платный'
			}
		}
	)
	data.update(
		{
			'bot': {
				'name': bot.name,
				'token': bot.token,
				'online': bot.online,
				'commands': [],
				'logs': []
			}
		}
	)

	for bot_command in TelegramBotCommandModel.objects.filter(bot_id=bot_id):
		data['bot']['commands'].append(
			{
				'id': bot_command.id,
				'command': bot_command.command
			}
		)
	if len(data['bot']['commands']) > 4:
		data['bot']['commands'][-1].update(
			{
				'command_positsion': 'last'
			}
		)

	for log in TelegramBotLogModel.objects.filter(bot_id=bot_id):
		data['bot']['logs'].append(
			{
				'id': log.id,
				'user_name': log.user_name,
				'user_message': log.user_message
			}
		)
	if len(data['bot']['logs']) > 2:
		data['bot']['logs'][-1].update(
			{
				'log_data_positsion': 'last'
			}
		)

	return render(request, 'view_bot.html', data)

@csrf_exempt
@GlobalDecorators.if_user_authed
@GlobalDecorators.check_bot_id
def start_bot(request: WSGIRequest, username: str, bot_id: int, bot: TelegramBotModel): # Запуск бота
	if bot.online == False:
		telegram_bot = TelegramBot(bot.id, bot.token)
		if telegram_bot.auth():
			Thread(target=telegram_bot.start, daemon=True).start()

			bot.online = True
			bot.save()

			return HttpResponse('Бот успешно запушен.')
		else:
			return HttpResponseBadRequest('Неверный "Token" бота!')
	else:
		return HttpResponseBadRequest('Вы уже запустили бота!')

@csrf_exempt
@GlobalDecorators.if_user_authed
@GlobalDecorators.check_bot_id
def stop_bot(request: WSGIRequest, username: str, bot_id: int, bot: TelegramBotModel): # Остоновка бота
	if bot.online:
		bot.online = False
		bot.save()

		return HttpResponse('Бот успешно остоновлен.')
	else:
		return HttpResponseBadRequest('Вы уже остоновили бота!')

@csrf_exempt
@GlobalDecorators.if_user_authed
@GlobalDecorators.check_request_data_items(needs_items=['bot_name', 'bot_token'])
@GlobalDecorators.check_bot_id
def save_bot_settings(request: WSGIRequest, username: str, bot_id: int, data: dict, bot: TelegramBotModel):
	bot_name, bot_token = data['bot_name'], data['bot_token']

	bot.name = bot_name
	bot.token = bot_token
	bot.save()

	return HttpResponse('Успешное сохрание настроек бота.')

@csrf_exempt
@GlobalDecorators.if_user_authed
@GlobalDecorators.check_bot_id
def clear_bot_logs(request: WSGIRequest, username: str, bot_id: int, bot: TelegramBotModel): # Очистка логов бота
	for log in TelegramBotLogModel.objects.filter(bot_id=bot_id):
		log.delete()

	return HttpResponse('Успешная очистка логов.')

@csrf_exempt
@GlobalDecorators.if_user_authed
@GlobalDecorators.check_bot_id
def get_bot_logs(request: WSGIRequest, username: str, bot_id: int, bot: TelegramBotModel): # Отправка логов бота
	finally_log = ''
	log = TelegramBotLogModel.objects.filter(bot_id=bot_id)
	for i in range(log.count()):
		if i + 1 == log.count() and log.count() > 2:
			finally_log += '<div class="bot-log" id="last">'
		else:
			finally_log += '<div class="bot-log">'

		finally_log += f"""
				<p class="bot-log-data">{log[i].user_name}:</p>
				<p class="bot-log-data">{log[i].user_message}</p>
			</div>
		"""

	return HttpResponse(finally_log)

@csrf_exempt
@GlobalDecorators.if_user_authed
@GlobalDecorators.check_max_commands_count_for_account
@GlobalDecorators.get_navbar_data
def add_bot_command_page(request: WSGIRequest, username: str, bot_id: int, data: dict): # Отрисовка view_bot_command.html
	data.update(
		{
			'variables_for_commands': GlobalVariable.VARIABLES_FOR_COMMANDS
		}
	)
	return render(request, 'view_bot_command.html', data)

@csrf_exempt
@GlobalDecorators.if_user_authed
@GlobalDecorators.check_request_data_items(needs_items=['command', 'command_answer'])
@GlobalDecorators.check_bot_id
@GlobalDecorators.check_max_commands_count_for_account
def add_bot_command(request: WSGIRequest, username: str, bot_id: int, data: dict, bot: TelegramBotModel): # Добавление команды боту
	command, command_answer = data['command'], data['command_answer']

	bot_command = TelegramBotCommandModel(None, bot_id, command, command_answer)
	bot_command.save()

	return HttpResponse('Успешное добавление команды.')

@GlobalDecorators.if_user_authed
@GlobalDecorators.check_bot_id
@GlobalDecorators.check_command_id
@GlobalDecorators.get_navbar_data
def view_bot_command_page(request: WSGIRequest, username: str, bot_id: int, command_id: int, bot: TelegramBotModel, bot_command: TelegramBotCommandModel, data: dict): # Отрисовка view_bot_command.html
	data.update(
		{
			'variables_for_commands': GlobalVariable.VARIABLES_FOR_COMMANDS,
			'bot_command': {
				'command': bot_command.command,
				'command_answer': bot_command.command_answer
			}
		}
	)

	return render(request, 'view_bot_command.html', data)

@csrf_exempt
@GlobalDecorators.if_user_authed
@GlobalDecorators.check_request_data_items(needs_items=['command', 'command_answer'])
@GlobalDecorators.check_bot_id
@GlobalDecorators.check_command_id
def save_bot_command(request: WSGIRequest, username: str, bot_id: int, command_id: int, data: dict, bot: TelegramBotModel, bot_command: TelegramBotCommandModel): # Сохранение команды бота
	command, command_answer = data['command'], data['command_answer']

	bot_command = TelegramBotCommandModel(command_id, bot_id, command, command_answer)
	bot_command.save()

	return HttpResponse('Успешное cохранение команды.')

@csrf_exempt
@GlobalDecorators.if_user_authed
@GlobalDecorators.check_bot_id
@GlobalDecorators.check_command_id
def delete_bot_command(request: WSGIRequest, username: str, bot_id: str, command_id: int, bot: TelegramBotModel, bot_command: TelegramBotCommandModel): # Удаление команды бота
	bot_command.delete()
	return HttpResponse('Успешное удаление команды.')
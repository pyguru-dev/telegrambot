"""
Exemple:
online_bots = {
	'USER-ID': {
		'BOT-ID' : telegram_bot.object
	}
}
"""

# Словарь для ботов, которые сейчас онлайн
online_bots = {}

# Словарь переменных для команд
variables_for_commands = [
	{
		'variable_name': 'Имя пользователя',
		'variable': '{user_name}',
		'{user_name}': 'update.effective_user.first_name'
	},
	{
		'variable_name': 'Фамилия пользователя',
		'variable': '{user_surname}',
		'{user_surname}': 'update.effective_user.last_name'
	},
	{
		'variable_name': 'Имя аккаунта',
		'variable': '{account_name}',
		'{account_name}': 'update.effective_user.name'
	},
	{
		'variable_name': 'ID аккаунта',
		'variable': '{account_id}',
		'{account_id}': 'update.effective_user.id'
	},
	{
		'variable_name': 'Ссылка на аккаунт',
		'variable': '{account_link}',
		'{account_link}': 'update.effective_user.link'
	}
]
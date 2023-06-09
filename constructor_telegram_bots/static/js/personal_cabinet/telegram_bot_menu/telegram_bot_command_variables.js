{
	let telegramBotCommandVariables = {
		'#telegramBotCommandUserIdVariableButton': '${user_id}',
		'#telegramBotCommandUserUsernameVariableButton': '${user_username}',
		'#telegramBotCommandUserFirstNameVariableButton': '${user_first_name}',
		'#telegramBotCommandUserLastNameVariableButton': '${user_last_name}',
		'#telegramBotCommandUserMessageIdVariableButton': '${user_message_id}',
		'#telegramBotCommandUserMessageTextVariableButton': '${user_message_text}',
	};
	let allowedTelegramBotCommandInputs = [telegramBotCommandTextInput, telegramBotCommandApiRequestUrlInput, telegramBotCommandApiRequestDataInput];
	let selectedTelegramBotCommandVariable = null;

	allowedTelegramBotCommandInputs.forEach(function(allowedTelegramBotCommandInput) {
		allowedTelegramBotCommandInput.onmouseover = function (event) {
			if (selectedTelegramBotCommandVariable != null) {
				event.target.style.cursor = 'copy';
			} else {
				event.target.style.cursor = 'auto';
			}
		}

		allowedTelegramBotCommandInput.onclick = function (event) {
			if (selectedTelegramBotCommandVariable != null) {
				event.target.style.cursor = 'auto';
				event.target.value = `${event.target.value}${selectedTelegramBotCommandVariable}`;

				selectedTelegramBotCommandVariable = null;

				for (telegramBotCommandVariable in telegramBotCommandVariables) {
					let telegramBotCommandVariableButton = document.querySelector(telegramBotCommandVariable);

					telegramBotCommandVariableButton.classList.replace('btn-secondary', 'btn-dark');
				}
			}
		}
	});

	for (telegramBotCommandVariable in telegramBotCommandVariables) {
		document.querySelector(telegramBotCommandVariable).onclick = function(event) {
			if (event.target.classList.contains('btn-dark')) {
				event.target.classList.replace('btn-dark', 'btn-secondary');

				selectedTelegramBotCommandVariable = telegramBotCommandVariables[`#${event.target.id}`];
			} else {
				event.target.classList.replace('btn-secondary', 'btn-dark');

				selectedTelegramBotCommandVariable = null;
			}
		}
	}
}
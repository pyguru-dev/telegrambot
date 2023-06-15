{	
	let telegramBotCommandVariablesButtons = {
		userId:  document.querySelector('#telegramBotCommandUserIdVariableButton'),
		userUsername:  document.querySelector('#telegramBotCommandUserUsernameVariableButton'),
		userFirstName: document.querySelector('#telegramBotCommandUserFirstNameVariableButton'),
		userLastName: document.querySelector('#telegramBotCommandUserLastNameVariableButton'),
		userMessageId:  document.querySelector('#telegramBotCommandUserMessageIdVariableButton'),
		userMessageText: document.querySelector('#telegramBotCommandUserMessageTextVariableButton'),
		apiResponse: document.querySelector('#telegramBotCommandApiResponseVariableButton'),
	};
	
	var telegramBotCommand = {
		cardHeader: document.querySelector('#telegramBotCommandCardHeader'),

		nameInput: document.querySelector('#telegramBotCommandNameInput'),
		textInput: document.querySelector('#telegramBotCommandTextInput'),

		additions: {
			command: {
				button: document.querySelector('#telegramBotCommandAddCommandAdditionButton'),
				div: document.querySelector('#telegramBotCommandCommandAddition'),
				variablesButtons: [],
				input: document.querySelector('#telegramBotCommandCommandInput'),
			},
			image: {
				button: document.querySelector('#telegramBotCommandAddImageAdditionButton'),
				div: document.querySelector('#telegramBotCommandImageAddition'),
				variablesButtons: [],
				preview: document.querySelector('#telegramBotCommandImagePreview'),
				input: document.querySelector('#telegramBotCommandImageInput'),
				file: null,
			},
			keyboard: {
				button: document.querySelector('#telegramBotCommandAddKeyboardAdditionButton'),
				div: document.querySelector('#telegramBotCommandKeyboardAddition'),
				variablesButtons: [],
				defaultRadio: document.querySelector('#telegramBotCommandDefaultKeyboardRadio'),
				inlineRadio: document.querySelector('#telegramBotCommandInlineKeyboardRadio'),
				buttons: document.querySelector('#telegramBotCommandKeyboardButtons'),
				addKeyboardButton: document.querySelector('#telegramBotCommandAddKeyboardButton'),
			},
			apiRequest: {
				button: document.querySelector('#telegramBotCommandAddApiRequestAdditionButton'),
				div: document.querySelector('#telegramBotCommandApiRequestAddition'),
				variablesButtons: [
					telegramBotCommandVariablesButtons.apiResponse
				],
				urlInput: document.querySelector('#telegramBotCommandApiRequestUrlInput'),
				dataInput: document.querySelector('#telegramBotCommandApiRequestDataInput'),
			},
		},

		backToAddButton: document.querySelector('.back-add-telegram-bot-command-button'),
		addOrEditButton: document.querySelector('.add-or-edit-telegram-bot-command-button'),
	};

	let telegramBotCommandVariables = {
		userId: {
			button: telegramBotCommandVariablesButtons.userId,
			allowedInputs: [],
			value: '${user_id}',
		},
		userUsername: {
			button: telegramBotCommandVariablesButtons.userUsername,
			allowedInputs: [],
			value: '${user_username}',
		},
		userFirstName: {
			button: telegramBotCommandVariablesButtons.userFirstName,
			allowedInputs: [],
			value: '${user_first_name}',
		},
		userLastName: {
			button: telegramBotCommandVariablesButtons.userLastName,
			allowedInputs: [],
			value: '${user_last_name}',
		},
		userMessageId: {
			button: telegramBotCommandVariablesButtons.userMessageId,
			allowedInputs: [],
			value: '${user_message_id}',
		},
		userMessageText: {
			button: telegramBotCommandVariablesButtons.userMessageText,
			allowedInputs: [],
			value: '${user_message_text}',
		},
		apiResponse: {
			button: telegramBotCommandVariablesButtons.apiResponse,
			allowedInputs: [
				telegramBotCommand.textInput,
			],
			value: '${api_response}',
		},

		allowedInputs: [
			telegramBotCommand.textInput,
			telegramBotCommand.additions.command.input,
			telegramBotCommand.additions.apiRequest.urlInput,
			telegramBotCommand.additions.apiRequest.dataInput,
		],

		selected: null,
	};

	function checkTelegramBotCommandVariable(variable) {
		if (variable != 'allowedInputs' &&  variable != 'selected') {
			return true;
		}
		return false;
	}

	function searchAllowedInputInTelegramBotCommandVariable(allowedInput) {
		if (telegramBotCommandVariables.selected != null) {
			for (let variable in telegramBotCommandVariables) {
				if (checkTelegramBotCommandVariable(variable) == true) {
					if (
						telegramBotCommandVariables[variable].value == telegramBotCommandVariables.selected && 
						(
							telegramBotCommandVariables[variable].allowedInputs.length == 0 ||
							telegramBotCommandVariables[variable].allowedInputs.indexOf(allowedInput) != -1
						)
					) {
						return true;
					}
				}
			}
		}
		return false;
	}

	telegramBotCommandVariables.allowedInputs.forEach(allowedInput => {
		allowedInput.addEventListener('mouseover', function() {
			if (searchAllowedInputInTelegramBotCommandVariable(allowedInput) == true) {
				allowedInput.style.cursor = 'copy';
			} else {
				allowedInput.style.cursor = 'auto';
			}
		});

		allowedInput.addEventListener('click', function() {
			if (searchAllowedInputInTelegramBotCommandVariable(allowedInput) == true) {
				allowedInput.style.cursor = 'auto';
				allowedInput.value = `${allowedInput.value}${telegramBotCommandVariables.selected}`;

				telegramBotCommandVariables.selected = null;

				for (let variable in telegramBotCommandVariables) {
					if (checkTelegramBotCommandVariable(variable) == true) {
						telegramBotCommandVariables[variable].button.classList.replace('btn-secondary', 'btn-dark');
					}
				}
			}
		})
	});

	for (let variable in telegramBotCommandVariables) {
		if (checkTelegramBotCommandVariable(variable) == true) {
			telegramBotCommandVariables[variable].button.addEventListener('click', function() {
				if (telegramBotCommandVariables[variable].button.classList.contains('btn-dark')) {
					telegramBotCommandVariables[variable].button.classList.replace('btn-dark', 'btn-secondary');
					telegramBotCommandVariables.selected = telegramBotCommandVariables[variable].value;
				} else {
					telegramBotCommandVariables[variable].button.classList.replace('btn-secondary', 'btn-dark');
					telegramBotCommandVariables.selected = null;
				}
			});
		}
	}

	telegramBotCommand.additions.image.input.addEventListener('change', function(event) {
		telegramBotCommand.additions.image.file = event.target.files[0];
		
		let telegramBotCommandImageReader = new FileReader();
		telegramBotCommandImageReader.addEventListener('load', function() {
			telegramBotCommand.additions.image.preview.classList.remove('d-none');
			telegramBotCommand.additions.image.preview.src = telegramBotCommandImageReader.result;
		});
		telegramBotCommandImageReader.readAsDataURL(telegramBotCommand.additions.image.file);
	});

	function telegramBotCommandAddKeyboardButton(id, value) {
		let inputGroup = document.createElement('div');
		inputGroup.classList = 'input-group mb-1';

		let telegramBotCommandKeyboardButton = document.createElement('input');
		telegramBotCommandKeyboardButton.classList = 'form-control btn btn-sm btn-outline-dark keyboard-button';
		telegramBotCommandKeyboardButton.id = id;
		telegramBotCommandKeyboardButton.type = 'text';
		telegramBotCommandKeyboardButton.style.cursor = 'text';
		telegramBotCommandKeyboardButton.value = value;

		let telegramBotCommandKeyboardButtonDelete = document.createElement('button');
		telegramBotCommandKeyboardButtonDelete.classList = 'btn btn-sm btn-danger';
		telegramBotCommandKeyboardButtonDelete.type = 'button';
		telegramBotCommandKeyboardButtonDelete.onclick = function () {
			inputGroup.remove();
		}

		let telegramBotCommandKeyboardButtonDeleteIcon = document.createElement('i');
		telegramBotCommandKeyboardButtonDeleteIcon.classList = 'bi bi-x-lg';
		telegramBotCommandKeyboardButtonDeleteIcon.style.webkitTextStroke = '1.5px';

		inputGroup.append(telegramBotCommandKeyboardButton);
		telegramBotCommandKeyboardButtonDelete.append(telegramBotCommandKeyboardButtonDeleteIcon);
		inputGroup.append(telegramBotCommandKeyboardButtonDelete);
		telegramBotCommand.additions.keyboard.buttons.append(inputGroup);

		telegramBotCommandKeyboardButton.focus();
	}

	telegramBotCommand.additions.keyboard.addKeyboardButton.addEventListener('click', () => telegramBotCommandAddKeyboardButton('', ''));

	for (let addition in telegramBotCommand.additions) {
		telegramBotCommand.additions[addition].button.addEventListener('click', function() {
			if (telegramBotCommand.additions[addition].div.classList.toggle('d-none') == false) {
				telegramBotCommand.additions[addition].button.classList.replace('btn-dark', 'btn-secondary');
			} else {
				telegramBotCommand.additions[addition].button.classList.replace('btn-secondary', 'btn-dark');
			}

			telegramBotCommand.additions[addition].variablesButtons.forEach(variableButton => variableButton.classList.toggle('d-none'));
		});
	}

	function telegramBotCommandClearAll() {
		telegramBotCommand.cardHeader.innerHTML = 'Добавление команды';

		telegramBotCommand.nameInput.value = '';
		telegramBotCommand.textInput.value = '';

		telegramBotCommand.additions.command.input.value = '';

		telegramBotCommand.additions.image.preview.classList.add('d-none');
		telegramBotCommand.additions.image.preview.src = '';
		telegramBotCommand.additions.image.input.value = null;
		telegramBotCommand.additions.image.file = null;

		telegramBotCommand.additions.keyboard.defaultRadio.checked = true;
		telegramBotCommand.additions.keyboard.buttons.innerHTML = '';

		telegramBotCommand.additions.apiRequest.urlInput.value = '';
		telegramBotCommand.additions.apiRequest.dataInput.value = '';

		for (let addition in telegramBotCommand.additions) {
			telegramBotCommand.additions[addition].button.classList.replace('btn-secondary', 'btn-dark');
			telegramBotCommand.additions[addition].div.classList.add('d-none');
		}

		telegramBotCommand.backToAddButton.classList.add('d-none');

		telegramBotCommand.addOrEditButton.id = '0';
		telegramBotCommand.addOrEditButton.innerHTML = 'Добавить команду';
	}

	telegramBotCommand.backToAddButton.addEventListener('click', telegramBotCommandClearAll);

	function editTelegramBotCommand(telegramBotCommand_) {
		telegramBotCommandClearAll();

		telegramBotCommand.cardHeader.innerHTML = 'Редактирование команды';

		telegramBotCommand.nameInput.value = telegramBotCommand_['name'];
		telegramBotCommand.textInput.value = telegramBotCommand_['message_text'];

		if (telegramBotCommand_['command'] != null) {
			telegramBotCommand.additions.command.button.classList.replace('btn-dark', 'btn-secondary');
			telegramBotCommand.additions.command.div.classList.remove('d-none');
			telegramBotCommand.additions.command.input.value = telegramBotCommand_['command'];
		}

		if (telegramBotCommand_['image'] != '') {
			telegramBotCommand.additions.image.button.classList.replace('btn-dark', 'btn-secondary');
			telegramBotCommand.additions.image.div.classList.remove('d-none');
			telegramBotCommand.additions.image.preview.classList.remove('d-none');
			telegramBotCommand.additions.image.preview.src = `/${telegramBotCommand_['image']}`;
		}

		if (telegramBotCommand_['keyboard'] != null) {
			telegramBotCommand.additions.keyboard.button.classList.replace('btn-dark', 'btn-secondary');
			telegramBotCommand.additions.keyboard.div.classList.remove('d-none');

			if (telegramBotCommand_['keyboard']['type'] == 'default') {
				telegramBotCommand.additions.keyboard.defaultRadio.checked = true;
			} else {
				telegramBotCommand.additions.keyboard.inlineRadio.checked = true;
			}

			telegramBotCommand_['keyboard']['buttons'].forEach(telegramBotCommandKeyboardButton => telegramBotCommandAddKeyboardButton(
				telegramBotCommandKeyboardButton['id'],
				telegramBotCommandKeyboardButton['text']
			));
		}

		if (telegramBotCommand_['api_request'] != null) {
			telegramBotCommand.additions.apiRequest.button.classList.replace('btn-dark', 'btn-secondary');
			telegramBotCommand.additions.apiRequest.div.classList.remove('d-none');
			telegramBotCommand.additions.apiRequest.urlInput.value = telegramBotCommand_['api_request']['link'];
			telegramBotCommand.additions.apiRequest.dataInput.value = telegramBotCommand_['api_request']['data'];
		}

		telegramBotCommand.backToAddButton.classList.remove('d-none');

		telegramBotCommand.addOrEditButton.id = telegramBotCommand_['id'];
		telegramBotCommand.addOrEditButton.innerHTML = 'Сохранить команду';
	}

	telegramBotCommand.addOrEditButton.addEventListener('click', function() {
		let telegramBotCommandData_ = {
			'name': telegramBotCommand.nameInput.value,
			'command': null,
			'message_text': telegramBotCommand.textInput.value,
			'keyboard': null,
			'api_request': null,
		}
	
		if (telegramBotCommand.additions.command.div.classList.contains('d-none') == false) {
			telegramBotCommandData_['command'] = telegramBotCommand.additions.command.input.value;
		}

		let telegramBotCommandData = new FormData();
		if (telegramBotCommand.additions.image.div.classList.contains('d-none') == false && telegramBotCommand.additions.image.file == null) {
			telegramBotCommandData.append('image', 'not_edited');
		} else {
			telegramBotCommandData.append('image', telegramBotCommand.additions.image.file);
		}

		if (telegramBotCommand.additions.keyboard.div.classList.contains('d-none') == false) {
			let telegramBotCommandKeyboardButtons_ = [];
			
			telegramBotCommand.additions.keyboard.buttons.querySelectorAll('input').forEach(telegramBotCommandKeyboardButton => telegramBotCommandKeyboardButtons_.push(
				{
					'id': telegramBotCommandKeyboardButton.id,
					'text': telegramBotCommandKeyboardButton.value,
				}
			));

			telegramBotCommandData_['keyboard'] = {
				'type': (telegramBotCommand.additions.keyboard.defaultRadio.checked) ? 'default' : 'inline',
				'buttons': telegramBotCommandKeyboardButtons_,
			}
		}

		if (telegramBotCommand.additions.apiRequest.div.classList.contains('d-none') == false) {
			telegramBotCommandData_['api_request'] = {
				'url': telegramBotCommand.additions.apiRequest.urlInput.value,
				'data': telegramBotCommand.additions.apiRequest.dataInput.value,
			}
		}

		telegramBotCommandData.append('data', JSON.stringify(telegramBotCommandData_));

		fetch(
			(this.id == '0') ? addTelegramBotCommandUrl : `/telegram-bot/${telegramBotId}/command/${this.id}/edit/`,
			{
				method: 'POST',
				body: telegramBotCommandData
			}
		).then(response => {
			if (response.ok) {
				updateTelegramBotCommands();
				telegramBotCommandClearAll();

				response.text().then(responseText => createAlert(mainAlertContainer, responseText, 'success'));
			} else {
				response.text().then(responseText => createAlert(mainAlertContainer, responseText, 'danger'));
			}
		});
	});
}
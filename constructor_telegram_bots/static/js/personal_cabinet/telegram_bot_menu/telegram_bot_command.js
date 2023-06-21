{
	const telegramBotCommandVariablesButtons = {
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

	const telegramBotCommandVariables = {
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
		return (variable != 'allowedInputs' &&  variable != 'selected');
	}

	function searchAllowedInputInTelegramBotCommandVariable(allowedInput) {
		if (telegramBotCommandVariables.selected != null) {
			for (const variable in telegramBotCommandVariables) {
				if (checkTelegramBotCommandVariable(variable)) {
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

	function telegramBotCommandVariablesAllClear() {
		for (const variable in telegramBotCommandVariables) {
			if (checkTelegramBotCommandVariable(variable)) {
				telegramBotCommandVariables[variable].button.classList.replace('btn-secondary', 'btn-dark');
			}
		}

		telegramBotCommandVariables.selected = null;
	}

	telegramBotCommandVariables.allowedInputs.forEach(allowedInput => {
		allowedInput.addEventListener('mouseover', function() {
			allowedInput.style.cursor = (searchAllowedInputInTelegramBotCommandVariable(allowedInput)) ? 'copy' : 'auto';
		});

		allowedInput.addEventListener('click', function() {
			if (searchAllowedInputInTelegramBotCommandVariable(allowedInput)) {
				allowedInput.style.cursor = 'auto';
				allowedInput.value = `${allowedInput.value}${telegramBotCommandVariables.selected}`;

				telegramBotCommandVariablesAllClear();
			}
		})
	});

	for (const variable in telegramBotCommandVariables) {
		if (checkTelegramBotCommandVariable(variable) == true) {
			telegramBotCommandVariables[variable].button.addEventListener('click', function() {
				telegramBotCommandVariablesAllClear();

				if (telegramBotCommandVariables[variable].button.classList.contains('btn-dark')) {
					telegramBotCommandVariables[variable].button.classList.replace('btn-dark', 'btn-secondary');
					telegramBotCommandVariables.selected = telegramBotCommandVariables[variable].value;
				}
			});
		}
	}

	telegramBotCommand.additions.image.input.addEventListener('change', function(event) {
		telegramBotCommand.additions.image.file = event.target.files[0];

		const telegramBotCommandImageReader = new FileReader();
		telegramBotCommandImageReader.addEventListener('load', function() {
			telegramBotCommand.additions.image.preview.classList.remove('d-none');
			telegramBotCommand.additions.image.preview.src = telegramBotCommandImageReader.result;
		});
		telegramBotCommandImageReader.readAsDataURL(telegramBotCommand.additions.image.file);
	});

	function telegramBotCommandAddKeyboardButtonLinkInput(
		telegramBotCommandKeyboardButton,
		telegramBotCommandKeyboardButtonAddLinkButton,
		telegramBotCommandKeyboardButtonUrl
	) {
		const telegramBotCommandKeyboardButtonLinkInput = document.createElement('input');
		telegramBotCommandKeyboardButtonLinkInput.classList = 'form-control form-control-sm link-input';
		telegramBotCommandKeyboardButtonLinkInput.type = 'text';
		telegramBotCommandKeyboardButtonLinkInput.placeholder = telegramBotCommandKeyboardButtonUrlText;
		telegramBotCommandKeyboardButtonLinkInput.value = telegramBotCommandKeyboardButtonUrl;

		if (telegramBotCommandKeyboardButtonAddLinkButton == null) {
			telegramBotCommandKeyboardButton.insertBefore(
				telegramBotCommandKeyboardButtonLinkInput,
				telegramBotCommandKeyboardButton.querySelector('.delete-button')
			);
		} else {
			telegramBotCommandKeyboardButton.replaceChild(
				telegramBotCommandKeyboardButtonLinkInput,
				telegramBotCommandKeyboardButtonAddLinkButton
			);
		} 

		telegramBotCommandKeyboardButtonLinkInput.focus();	
	}

	function telegramBotCommandAddKeyboardButtonAddLinkButton(telegramBotCommandKeyboardButton) {
		const telegramBotCommandKeyboardButtonAddLinkButton = document.createElement('button');
		telegramBotCommandKeyboardButtonAddLinkButton.classList = 'btn btn-sm btn-secondary add-link-button';
		telegramBotCommandKeyboardButtonAddLinkButton.type = 'button';
		telegramBotCommandKeyboardButtonAddLinkButton.innerHTML = '<i class="bi bi-link-45deg" style="-webkit-text-stroke: 0.25px;"></i>';
		telegramBotCommandKeyboardButtonAddLinkButton.addEventListener('click', function() {
			telegramBotCommandAddKeyboardButtonLinkInput(
				telegramBotCommandKeyboardButton,
				telegramBotCommandKeyboardButtonAddLinkButton,
				null
			);
		});

		telegramBotCommandKeyboardButton.insertBefore(
			telegramBotCommandKeyboardButtonAddLinkButton,
			telegramBotCommandKeyboardButton.querySelector('.delete-button')
		);
	}

	function telegramBotCommandAddKeyboardButton(
		telegramBotCommandKeyboardButtonId,
		telegramBotCommandKeyboardButtonText,
		telegramBotCommandKeyboardButtonUrl
	) {
		const telegramBotCommandKeyboardButton = document.createElement('div');
		telegramBotCommandKeyboardButton.classList = 'input-group keyboard-button mb-1';

		const telegramBotCommandKeyboardButtonMoveUp = document.createElement('button');
		telegramBotCommandKeyboardButtonMoveUp.classList = 'btn btn-sm btn-dark';
		telegramBotCommandKeyboardButtonMoveUp.type = 'button';
		telegramBotCommandKeyboardButtonMoveUp.innerHTML = '<i class="bi bi-arrow-up" style="-webkit-text-stroke: 1px;"></i>';
		telegramBotCommandKeyboardButtonMoveUp.addEventListener('click', function() {
			const telegramBotCommandKeyboardButtonPrevious = telegramBotCommandKeyboardButton.previousElementSibling;
			
			if (telegramBotCommandKeyboardButtonPrevious != null) {
				telegramBotCommandKeyboardButton.parentNode.insertBefore(
					telegramBotCommandKeyboardButton,
					telegramBotCommandKeyboardButtonPrevious
				);
			}
		});

		telegramBotCommandKeyboardButton.append(telegramBotCommandKeyboardButtonMoveUp)

		const telegramBotCommandKeyboardButtonMoveDown = document.createElement('button');
		telegramBotCommandKeyboardButtonMoveDown.classList = 'btn btn-sm btn-dark';
		telegramBotCommandKeyboardButtonMoveDown.type = 'button';
		telegramBotCommandKeyboardButtonMoveDown.innerHTML = '<i class="bi bi-arrow-down" style="-webkit-text-stroke: 1px;"></i>';
		telegramBotCommandKeyboardButtonMoveDown.addEventListener('click', function() {
			const telegramBotCommandKeyboardButtonNext = telegramBotCommandKeyboardButton.nextElementSibling;
			
			if (telegramBotCommandKeyboardButtonNext != null) {
				telegramBotCommandKeyboardButton.parentNode.insertBefore(
					telegramBotCommandKeyboardButtonNext,
					telegramBotCommandKeyboardButton
				);
			}
		});

		telegramBotCommandKeyboardButton.append(telegramBotCommandKeyboardButtonMoveDown)

		const telegramBotCommandKeyboardButtonNameInput = document.createElement('input');
		telegramBotCommandKeyboardButtonNameInput.classList = 'form-control form-control-sm name-input';
		telegramBotCommandKeyboardButtonNameInput.id = telegramBotCommandKeyboardButtonId;
		telegramBotCommandKeyboardButtonNameInput.type = 'text';
		telegramBotCommandKeyboardButtonNameInput.placeholder = telegramBotCommandKeyboardButtonNameText;
		telegramBotCommandKeyboardButtonNameInput.value = telegramBotCommandKeyboardButtonText;

		telegramBotCommandKeyboardButton.append(telegramBotCommandKeyboardButtonNameInput);

		if (telegramBotCommand.additions.keyboard.inlineRadio.checked) {
			if (telegramBotCommandKeyboardButtonUrl == null) {
				telegramBotCommandAddKeyboardButtonAddLinkButton(telegramBotCommandKeyboardButton);
			} else {
				telegramBotCommandAddKeyboardButtonLinkInput(
					telegramBotCommandKeyboardButton,
					null,
					telegramBotCommandKeyboardButtonUrl
				);
			}
		}

		const telegramBotCommandKeyboardButtonDelete = document.createElement('button');
		telegramBotCommandKeyboardButtonDelete.classList = 'btn btn-sm btn-danger delete-button';
		telegramBotCommandKeyboardButtonDelete.type = 'button';
		telegramBotCommandKeyboardButtonDelete.innerHTML = '<i class="bi bi-x-lg" style="-webkit-text-stroke: 1.25px;"></i>';
		telegramBotCommandKeyboardButtonDelete.addEventListener('click', () => telegramBotCommandKeyboardButton.remove());

		telegramBotCommandKeyboardButton.append(telegramBotCommandKeyboardButtonDelete);

		telegramBotCommand.additions.keyboard.buttons.append(telegramBotCommandKeyboardButton);

		telegramBotCommandKeyboardButtonNameInput.focus();
	}

	telegramBotCommand.additions.keyboard.defaultRadio.addEventListener('click', function() {
		telegramBotCommand.additions.keyboard.buttons.querySelectorAll('.add-link-button').forEach(
			telegramBotCommandKeyboardButtonAddLinkButton => telegramBotCommandKeyboardButtonAddLinkButton.remove()
		);
		telegramBotCommand.additions.keyboard.buttons.querySelectorAll('.link-input').forEach(
			telegramBotCommandKeyboardButtonLinkInput => telegramBotCommandKeyboardButtonLinkInput.remove()
		);
	});

	telegramBotCommand.additions.keyboard.inlineRadio.addEventListener('click', function() {
		telegramBotCommand.additions.keyboard.buttons.querySelectorAll('.keyboard-button').forEach(
			telegramBotCommandKeyboardButton => {
				if (
					telegramBotCommandKeyboardButton.querySelector('.add-link-button') == null && 
					telegramBotCommandKeyboardButton.querySelector('.link-input') == null
				) {
					telegramBotCommandAddKeyboardButtonAddLinkButton(telegramBotCommandKeyboardButton);
				}
			}
		);
	});

	telegramBotCommand.additions.keyboard.addKeyboardButton.addEventListener('click', function() {
		telegramBotCommandAddKeyboardButton('', null, null);
	});

	for (const addition in telegramBotCommand.additions) {
		telegramBotCommand.additions[addition].button.addEventListener('click', function() {
			if (telegramBotCommand.additions[addition].div.classList.toggle('d-none')) {
				telegramBotCommand.additions[addition].button.classList.replace('btn-secondary', 'btn-dark');
			} else {
				telegramBotCommand.additions[addition].button.classList.replace('btn-dark', 'btn-secondary');
			}

			telegramBotCommand.additions[addition].variablesButtons.forEach(variableButton => {
				variableButton.classList.toggle('d-none');
			});
		});
	}

	function telegramBotCommandClearAll() {
		telegramBotCommand.cardHeader.innerHTML = telegramBotCommandCardHeaderAddCommandTitleText;

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

		for (const addition in telegramBotCommand.additions) {
			telegramBotCommand.additions[addition].button.classList.replace('btn-secondary', 'btn-dark');
			telegramBotCommand.additions[addition].div.classList.add('d-none');
		}

		telegramBotCommand.backToAddButton.classList.add('d-none');

		telegramBotCommand.addOrEditButton.id = '0';
		telegramBotCommand.addOrEditButton.innerHTML = telegramBotCommandFooterAddCommandButtonText;
	}

	telegramBotCommand.backToAddButton.addEventListener('click', telegramBotCommandClearAll);

	function editTelegramBotCommand(telegramBotCommand_) {
		telegramBotCommandClearAll();

		telegramBotCommand.cardHeader.innerHTML = telegramBotCommandCardHeaderEditCommandTitleText;

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
				telegramBotCommandKeyboardButton['text'],
				telegramBotCommandKeyboardButton['url']
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
		telegramBotCommand.addOrEditButton.innerHTML = telegramBotCommandFooterSaveCommandButtonText;
	}

	telegramBotCommand.addOrEditButton.addEventListener('click', function() {
		const telegramBotCommandData_ = {
			'name': telegramBotCommand.nameInput.value,
			'command': null,
			'message_text': telegramBotCommand.textInput.value,
			'keyboard': null,
			'api_request': null,
		}
	
		if (telegramBotCommand.additions.command.div.classList.contains('d-none') == false) {
			telegramBotCommandData_['command'] = telegramBotCommand.additions.command.input.value;
		}

		const telegramBotCommandData = new FormData();

		if (
			telegramBotCommand.additions.image.div.classList.contains('d-none') == false &&
			telegramBotCommand.additions.image.preview.classList.contains('d-none') == false
		) {
			if (telegramBotCommand.additions.image.file != null) {
				telegramBotCommandData.append('image', telegramBotCommand.additions.image.file);
			} else {
				telegramBotCommandData.append('image', 'not_edited');
			}
		} else {
			telegramBotCommandData.append('image', 'null');
		}

		if (telegramBotCommand.additions.keyboard.div.classList.contains('d-none') == false) {
			const telegramBotCommandKeyboardButtons_ = [];
			
			telegramBotCommand.additions.keyboard.buttons.querySelectorAll('.keyboard-button').forEach(telegramBotCommandKeyboardButton => {
				const telegramBotCommandKeyboardButtonNameInput = telegramBotCommandKeyboardButton.querySelector('.name-input');
				const telegramBotCommandKeyboardButtonLinkInput = telegramBotCommandKeyboardButton.querySelector('.link-input');
				
				telegramBotCommandKeyboardButtons_.push(
					{
						'id': telegramBotCommandKeyboardButton.id,
						'text': (telegramBotCommandKeyboardButtonNameInput == null) ? null : telegramBotCommandKeyboardButtonNameInput.value,
						'url': (telegramBotCommandKeyboardButtonLinkInput == null) ? null : telegramBotCommandKeyboardButtonLinkInput.value,
					}
				);
			});

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
			(telegramBotCommand.addOrEditButton.id == '0') ? addTelegramBotCommandUrl : `/telegram-bot/${telegramBotId}/command/${telegramBotCommand.addOrEditButton.id}/edit/`,
			{
				method: 'POST',
				body: telegramBotCommandData,
			}
		).then(response => {
			if (response.ok) {
				updateTelegramBotCommands();
				telegramBotCommandClearAll();
			}

			response.json().then(jsonResponse => createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']));
		});
	});
}
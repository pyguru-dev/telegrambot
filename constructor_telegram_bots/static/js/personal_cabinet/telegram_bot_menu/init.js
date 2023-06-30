var intervalUpdateUsersIsRunning = false;
var intervalUpdateUsersId;

{
	const telegramBotUsername = document.querySelector('#telegramBotUsername');
	const telegramBotApiToken = document.querySelector('#telegramBotApiToken');

	function updateTelegramBot() {
		fetch (getTelegramBotDataUrl, {
			method: 'POST'
		}).then(response => {
			if (response.ok) {
				response.json().then(telegramBot => {
					telegramBotUsername.href = `tg://resolve?domain=${telegramBot['username']}`;
					telegramBotUsername.innerHTML = `@${telegramBot['username']}`;
					telegramBotApiToken.innerHTML = telegramBot['api_token'];
				});
			} else {
				response.json().then(jsonResponse => {
					createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
				});
			}
		});
	}

	updateTelegramBot();
}

{
	const telegramBotCommandsCount = document.querySelector('.telegram-bot-commands-count');

	function updateTelegramBotCommands() {
		fetch(getTelegramBotCommandsUrl, {
			method: 'POST',
		}).then(response => {
			if (response.ok) {
				response.json().then(telegramBotCommands => {
					telegramBotCommandsCount.innerHTML = telegramBotCommands.length;

					document.querySelectorAll('.diagram-block').forEach(diagramBlock => diagramBlock.remove());
					document.querySelectorAll('.connector-line').forEach(diagramConnectorLine => diagramConnectorLine.remove());

					telegramBotCommands.forEach(telegramBotCommand => createDiagramBlock(telegramBotCommand));
					document.querySelectorAll('.diagram-edit-button').forEach(diagramEditButton => {
						diagramEditButton.addEventListener('click', function() {
							fetch(`/telegram-bot/${telegramBotId}/command/${this.id}/get-data/`, {
								method: 'POST',
							}).then(response => {
								if (response.ok) {
									response.json().then(telegramBotCommand => {
										editTelegramBotCommand(telegramBotCommand);
									});
								} else {
									response.json().then(jsonResponse => {
										createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level'])
									});
								}
							});
						});
					});
					document.querySelectorAll('.diagram-delete-button').forEach(diagramDeleteButton => {
						diagramDeleteButton.addEventListener('click', function() {
							const telegramBotCommandId = this.id;

							askConfirmModal(
								deleteTelegramBotCommandAskConfirmModalTitle,
								deleteTelegramBotCommandAskConfirmModalText,
								function() {
									fetch(`/telegram-bot/${telegramBotId}/command/${telegramBotCommandId}/delete/`, {
										method: 'POST',
									}).then(response => {
										if (response.ok) {
											if (telegramBotCommand.addOrEditButton.id != '0') {
												telegramBotCommandClearAll();
											}

											updateTelegramBotCommands();

											response.json().then(jsonResponse => {
												createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
											});
										}
									});
								}
							);
						});
					});
					document.querySelectorAll('.diagram-name').forEach(diagramName => {
						if (diagramName.offsetHeight > 42) {
							diagramName.classList.add('rounded-bottom');
						}
					});

					function createDiagramConnectorLines(telegramBotCommandKeyboard) {
						telegramBotCommandKeyboard['buttons'].forEach(telegramBotCommandKeyboardButton => {
							if (telegramBotCommandKeyboardButton['telegram_bot_command_id'] != null) {
								createDiagramConnectorLine(
									document.querySelector(`.diagram-connector[id="${telegramBotCommandKeyboardButton['start_diagram_connector']}"]`),
									document.querySelector(`.diagram-connector[id="${telegramBotCommandKeyboardButton['end_diagram_connector']}"]`)
								);
							}
						});
					}

					telegramBotCommands.forEach(telegramBotCommand => {
						if (telegramBotCommand['keyboard'] != null) {
							const diagramBlock = document.querySelector(`.diagram-block[id="${telegramBotCommand['id']}"]`);
							const diagramBlockImage = diagramBlock.querySelector('img');

							if (diagramBlockImage != null) {
								diagramBlockImage.addEventListener('load', function() {
									createDiagramConnectorLines(telegramBotCommand['keyboard']);
								});
							} else {
								createDiagramConnectorLines(telegramBotCommand['keyboard']);
							}
						}
					});
					document.querySelectorAll('.diagram-connector').forEach(diagramConnector => {
						diagramConnector.addEventListener('click', connectorClick);
					});

					diagramSetZoom();
				});
			} else {
				response.json().then(jsonResponse => {
					createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
				});
			}
		});

		updateTelegramBotUsers();
		if (telegramBotIsRunning && intervalUpdateUsersIsRunning == false) {
			intervalUpdateUsersIsRunning = true;

			intervalUpdateUsersId = setInterval(updateTelegramBotUsers, 3000);
		}
	}
}

{
	const telegramBotUsersCount = document.querySelector('.telegram-bot-users-count');

	function updateTelegramBotUsers() {
		if (document.hidden == false) {
			fetch(getTelegramBotUsersUrl, {
				method: 'POST',
			}).then(response => {
				if (response.ok) {
					response.json().then(telegramBotUsers => {
						telegramBotUsersCount.innerHTML = telegramBotUsers.length;

						const telegramBotUsersDiv = document.querySelector('.telegram-bot-users');
						telegramBotUsersDiv.innerHTML = '';

						if (telegramBotUsers.length == 0) {
							const telegramBotUserDiv = document.createElement('div');
							telegramBotUserDiv.setAttribute('class', 'list-group-item pb-1');
							telegramBotUserDiv.innerHTML = `<p class="text-center my-2">${telegramBotNotActivatedText}</p>`;

							telegramBotUsersDiv.append(telegramBotUserDiv);
						} else {
							telegramBotUsers.forEach(telegramBotUser => {
								const listGroupItem = document.createElement('div');
								listGroupItem.setAttribute('class', 'list-group-item pb-1');

								const telegramBotUserDiv = document.createElement('div');
								telegramBotUserDiv.setAttribute('class', 'row justify-content-between');
								telegramBotUserDiv.innerHTML = [
									'<div class="col-auto">',
									`	<p class="my-2">[${telegramBotUser['date_activated']}]: ${telegramBotUser['user_id']} - ${telegramBotUser['full_name']}</p>`,
									'</div>',
								].join('');

								const telegramBotUserButtons = document.createElement('div');
								telegramBotUserButtons.classList = 'col-auto';
								telegramBotUserButtons.id = 'telegramBotUserButtons';

								const addOrDeleteTelegramBotAllowedUserButton = document.createElement('button');
								addOrDeleteTelegramBotAllowedUserButton.classList = 'btn telegram-bot-allowed-user-button rounded-0 p-0 pe-1';
								addOrDeleteTelegramBotAllowedUserButton.id = telegramBotUser['id'];
								addOrDeleteTelegramBotAllowedUserButton.type = 'button';
								addOrDeleteTelegramBotAllowedUserButton.style.fontSize = '1.5rem';

								if (telegramBotUser['is_allowed']) {
									addOrDeleteTelegramBotAllowedUserButton.classList.add('delete');
									addOrDeleteTelegramBotAllowedUserButton.innerHTML = '<i class="bi bi-star-fill text-warning"></i>';
								} else {
									addOrDeleteTelegramBotAllowedUserButton.classList.add('add');
									addOrDeleteTelegramBotAllowedUserButton.innerHTML = '<i class="bi bi-star text-warning"></i>';
								}

								addOrDeleteTelegramBotAllowedUserButton.addEventListener('click', function() {
									if (addOrDeleteTelegramBotAllowedUserButton.classList.contains('delete')) {
										addOrDeleteTelegramBotAllowedUserButton.classList.replace('delete', 'add')
										addOrDeleteTelegramBotAllowedUserButton.innerHTML = '<i class="bi bi-star text-warning"></i>';

										fetch(`/telegram-bot/${telegramBotId}/user/${telegramBotUser['id']}/delete-allowed-user/`, {
											method: 'POST',
										}).then(response => {
											response.json().then(jsonResponse => {
												createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
											});
										});
									} else {
										addOrDeleteTelegramBotAllowedUserButton.classList.replace('add', 'delete')
										addOrDeleteTelegramBotAllowedUserButton.innerHTML = '<i class="bi bi-star-fill text-warning"></i>';

										fetch(`/telegram-bot/${telegramBotId}/user/${telegramBotUser['id']}/add-allowed-user/`, {
											method: 'POST',
										}).then(response => {
											response.json().then(jsonResponse => {
												createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
											});
										});
									}
								});

								if (telegramBotIsPrivateCheckBox.checked == false) {
									addOrDeleteTelegramBotAllowedUserButton.classList.add('d-none');
								}

								const deleteTelegramBotUserButton = document.createElement('button');
								deleteTelegramBotUserButton.classList = 'btn rounded-0 p-0';
								deleteTelegramBotUserButton.id = telegramBotUser['id'];
								deleteTelegramBotUserButton.type = 'button';
								deleteTelegramBotUserButton.style.fontSize = '1.5rem';
								deleteTelegramBotUserButton.innerHTML = '<i class="bi bi-trash text-danger"></i>';

								deleteTelegramBotUserButton.addEventListener('click', () => askConfirmModal(
									deleteTelegramBotUserAskConfirmModalTitle,
									deleteTelegramBotUserAskConfirmModalText,
									function() {
										fetch(`/telegram-bot/${telegramBotId}/user/${telegramBotUser['id']}/delete/`, {
											method: 'POST',
										}).then(response => {
											if (response.ok) {
												updateTelegramBotUsers();
											}

											response.json().then(jsonResponse => {
												createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
											});
										});
									}
								));

								telegramBotUserButtons.append(addOrDeleteTelegramBotAllowedUserButton);
								telegramBotUserButtons.append(deleteTelegramBotUserButton);
								telegramBotUserDiv.append(telegramBotUserButtons);

								listGroupItem.append(telegramBotUserDiv);
								telegramBotUsersDiv.append(listGroupItem);
							});
						}
					});
				} else {
					response.json().then(jsonResponse => {
						createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
					});
				}
			});
		}
	}

	updateTelegramBotCommands();
}

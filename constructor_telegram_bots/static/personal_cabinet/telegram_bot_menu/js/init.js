{
	const telegramBotCommandsCount = document.querySelector('#telegramBotCommandsCount');

	function updateTelegramBotCommands() {
		fetch(getTelegramBotCommandsUrl, {
			method: 'POST',
			headers: {'Authorization': `Token ${userApiToken}`},
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
								headers: {'Authorization': `Token ${userApiToken}`},
							}).then(response => {
								response.json().then(jsonResponse => {
									if (response.ok) {
										editTelegramBotCommand(jsonResponse);
									} else {
										createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
									}
								});
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
										headers: {'Authorization': `Token ${userApiToken}`},
									}).then(response => {
										if (response.ok) {
											if (telegramBotCommand.addOrEditButton.id != '0') {
												telegramBotCommandClearAll();
											}

											updateTelegramBotCommands();
										}

										response.json().then(jsonResponse => {
											createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
										});
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

					const createDiagramConnectorLines = (telegramBotCommandKeyboard) => {
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
	}

	updateTelegramBotCommands();
}
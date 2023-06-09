var telegramBotCommandKeyboardType = 'default';

var intervalUpdateUsersIsRunning = false;
var intervalUpdateUsersId;

{
	let telegramBotCommandsCountTableLine = document.querySelector('.telegram-bot-commands-count');

	function getTelegramBotCommands() {
		fetch(getTelegramBotCommandsUrl, {
			method: 'POST',
		}).then(response => {
			if (response.ok) {
				response.json().then(telegramBotCommands => {
					telegramBotCommandsCountTableLine.innerHTML = telegramBotCommands.length;

					document.querySelectorAll('.diagram-block').forEach(diagramBlock => diagramBlock.remove());
					document.querySelectorAll('.connector-line').forEach(diagramConnectorLine => diagramConnectorLine.remove());

					telegramBotCommands.forEach(telegramBotCommand => createDiagramBlock(telegramBotCommand));

					document.querySelectorAll('.diagram-name').forEach(diagramName => {
						if (diagramName.offsetHeight > 42) {
							diagramName.classList.add('rounded-bottom');
						}
					});

					function createDiagramConnectorLines(telegramBotCommandKeyboard) {
						telegramBotCommandKeyboard['buttons'].forEach(telegramBotCommandKeyboardButton => {
							if (telegramBotCommandKeyboardButton['telegram_bot_command_id'] != null) {
								let startDiagramConnector = document.querySelector(`.diagram-connector[id="${telegramBotCommandKeyboardButton['start_diagram_connector']}"]`);
								let endDiagramConnector = document.querySelector(`.diagram-connector[id="${telegramBotCommandKeyboardButton['end_diagram_connector']}"]`);

								createDiagramConnectorLine(startDiagramConnector, endDiagramConnector);
							}
						});
					}

					telegramBotCommands.forEach(telegramBotCommand => {
						if (telegramBotCommand['keyboard'] != null) {
							let diagramBlock = document.querySelector(`.diagram-block[id="${telegramBotCommand['id']}"]`);
							let diagramBlockImage = diagramBlock.querySelector('img');

							if (diagramBlockImage != null) {
								diagramBlockImage.onload = () => createDiagramConnectorLines(telegramBotCommand['keyboard']);
							} else {
								createDiagramConnectorLines(telegramBotCommand['keyboard']);
							}
						}
					});

					document.querySelectorAll('.diagram-connector').forEach(diagramConnector => diagramConnector.addEventListener('click', connectorClick));

					document.querySelectorAll('.diagram-edit-button').forEach(diagramEditButton => {
						diagramEditButton.addEventListener('click', function() {
							fetch(`/telegram-bot/${telegramBotId}/command/${this.id}/get-data/`, {
								method: 'POST',
							}).then(response => {
								if (response.ok) {
									response.json().then(telegramBotCommand => editTelegramBotCommand(telegramBotCommand));
								} else {response.text().then(responseText => createAlert(mainAlertContainer, responseText, 'danger'))}
							});
						});
					});

					document.querySelectorAll('.diagram-delete-button').forEach(diagramDeleteButton => {
						diagramDeleteButton.addEventListener('click', function() {
							let telegramBotCommandId = this.id;

							askConfirmModal(
								'Удаление команды Telegram бота',
								'Вы точно хотите удалить команду Telegram бота?',
								function() {
									fetch(`/telegram-bot/${telegramBotId}/command/${telegramBotCommandId}/delete/`, {
										method: 'POST',
									}).then(response => {
										if (response.ok) {
											response.text().then(responseText => {
												if (addOrEditTelegramBotCommandButton.id != '0') {
													telegramBotCommandAllClear();
												}

												getTelegramBotCommands();

												createAlert(mainAlertContainer, responseText, 'success');
											});
										} else {response.text().then(responseText => createAlert(mainAlertContainer, responseText, 'danger'))}
									});
								}
							);
						});
					});

					diagramSetZoom();
				});
			} else {response.text().then(responseText => createAlert(mainAlertContainer, responseText, 'danger'))}
		});

		getTelegramBotUsers();
		if (telegramBotIsRunning && intervalUpdateUsersIsRunning == false) {
			intervalUpdateUsersIsRunning = true;

			intervalUpdateUsersId = setInterval(getTelegramBotUsers, 3000);
		}
	}
}

{
	let telegramBotUsersCountTableLine = document.querySelector('.telegram-bot-users-count');

	function getTelegramBotUsers() {
		if (document.hidden == false) {
			fetch(getTelegramBotUsersUrl, {
				method: 'POST',
			}).then(response => {
				if (response.ok) {
					response.json().then(telegramBotUsers => {
						telegramBotUsersCountTableLine.innerHTML = telegramBotUsers.length;

						let telegramBotUsersDiv = document.querySelector('.telegram-bot-users');
						telegramBotUsersDiv.innerHTML = '';

						if (telegramBotUsers.length > 0) {
							telegramBotUsers.forEach(telegramBotUser => {
								let listGroupItem = document.createElement('div');
								listGroupItem.setAttribute('class', 'list-group-item pb-1');

								let telegramBotUserDiv = document.createElement('div');
								telegramBotUserDiv.setAttribute('class', 'row justify-content-between');
								telegramBotUserDiv.innerHTML = [
									'	<div class="col-auto">',
									`		<p class="my-2">[${telegramBotUser['date_activated']}]: @${telegramBotUser['username']}</p>`,
									'	</div>',
								].join('');

								let telegramBotUserButtons = document.createElement('div');
								telegramBotUserButtons.classList = 'col-auto';
								telegramBotUserButtons.id = 'telegramBotUserButtons';
								
								let addOrDeleteTelegramBotAllowedUserButton = document.createElement('button');
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
											if (response.ok) {
												response.text().then(responseText => createAlert(mainAlertContainer, responseText, 'success'));
											} else {response.text().then(responseText => createAlert(mainAlertContainer, responseText, 'danger'))}
										});
									} else {
										addOrDeleteTelegramBotAllowedUserButton.classList.replace('add', 'delete')
										addOrDeleteTelegramBotAllowedUserButton.innerHTML = '<i class="bi bi-star-fill text-warning"></i>';

										fetch(`/telegram-bot/${telegramBotId}/user/${telegramBotUser['id']}/add-allowed-user/`, {
											method: 'POST',
										}).then(response => {
											if (response.ok) {
												response.text().then(responseText => createAlert(mainAlertContainer, responseText, 'success'));
											} else {response.text().then(responseText => createAlert(mainAlertContainer, responseText, 'danger'))}
										});
									}
								});

								if (telegramBotIsPrivateCheckBox.checked == false) {
									addOrDeleteTelegramBotAllowedUserButton.classList.add('d-none');
								}

								let deleteTelegramBotUserButton = document.createElement('button');
								deleteTelegramBotUserButton.classList = 'btn rounded-0 p-0';
								deleteTelegramBotUserButton.id = telegramBotUser['id'];
								deleteTelegramBotUserButton.type = 'button';
								deleteTelegramBotUserButton.style.fontSize = '1.5rem';
								deleteTelegramBotUserButton.innerHTML = '<i class="bi bi-trash text-danger"></i>';

								deleteTelegramBotUserButton.addEventListener('click', () => askConfirmModal(
									'Удаление пользователя Telegram бота',
									'Вы точно хотите удалить пользователя Telegram бота?',
									function() {
										fetch(`/telegram-bot/${telegramBotId}/user/${telegramBotUser['id']}/delete/`, {
											method: 'POST',
										}).then(response => {
											if (response.ok) {
												getTelegramBotUsers();

												response.text().then(responseText => createAlert(mainAlertContainer, responseText, 'success'));
											} else {response.text().then(responseText => createAlert(mainAlertContainer, responseText, 'danger'))}
										});
									}
								));
								
								telegramBotUserButtons.append(addOrDeleteTelegramBotAllowedUserButton);
								telegramBotUserButtons.append(deleteTelegramBotUserButton);
								telegramBotUserDiv.append(telegramBotUserButtons);
								listGroupItem.append(telegramBotUserDiv);
								telegramBotUsersDiv.append(listGroupItem);
							});
						} else {
							let telegramBotUserDiv = document.createElement('div');
							telegramBotUserDiv.setAttribute('class', 'list-group-item pb-1');
							telegramBotUserDiv.innerHTML = `<p class="text-center my-2">Вашего Telegram бота ещё никто не активировал.</p>`;
							telegramBotUsersDiv.append(telegramBotUserDiv);
						}
					});
				} else {response.text().then(responseText => createAlert(mainAlertContainer, responseText, 'danger'))}
			});
		}
	}
}

getTelegramBotCommands();

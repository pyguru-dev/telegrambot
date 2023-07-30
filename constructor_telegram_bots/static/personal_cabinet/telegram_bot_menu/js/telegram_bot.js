{
	const telegramBotApiToken = document.querySelector('#telegramBotApiToken');
	const telegramBotUsername = document.querySelector('#telegramBotUsername');

	const updateTelegramBot = () => {
		fetch(telegramBotUrl, {
			method: 'GET',
			headers: {'Authorization': `Token ${userApiToken}`},
		}).then(response => {
			response.json().then(jsonResponse => {
				if (response.ok) {
					telegramBotUsername.href = `tg://resolve?domain=${jsonResponse['username']}`;
					telegramBotUsername.innerHTML = `@${jsonResponse['username']}`;
					telegramBotApiToken.innerHTML = jsonResponse['api_token'];
				} else {
					createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
				}
			});
		});
	}

	updateTelegramBot();

	{
		const telegramBotApiTokenEditButton = document.querySelector('#telegramBotApiTokenEditButton');
		const telegramBotApiTokenSaveButton = document.querySelector('#telegramBotApiTokenSaveButton');
		const telegramBotApiTokenCancelButton = document.querySelector('#telegramBotApiTokenCancelButton');

		const telegramBotApiTokenEditOrSaveOrCancel = () => {
			const telegramBotApiTokenInput = telegramBotApiToken.querySelector('input');

			if (telegramBotApiTokenInput == null) {
				telegramBotApiToken.innerHTML = `<input class="form-control" id="${telegramBotApiToken.innerHTML}" type="text" placeholder="${telegramBotTableLineApiTokenInputText}" value="${telegramBotApiToken.innerHTML}">`;
			} else {
				telegramBotApiToken.innerHTML = telegramBotApiTokenInput.id;
			}

			telegramBotApiTokenEditButton.classList.toggle('d-none');
			telegramBotApiTokenSaveButton.classList.toggle('d-none');
			telegramBotApiTokenCancelButton.classList.toggle('d-none');
		}

		telegramBotApiTokenEditButton.addEventListener('click', telegramBotApiTokenEditOrSaveOrCancel);
		telegramBotApiTokenSaveButton.addEventListener('click', function() {
			const telegramBotApiTokenInput = telegramBotApiToken.querySelector('input');

			fetch(telegramBotUrl, {
				method: 'PATCH',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Token ${userApiToken}`,
				},
				body: JSON.stringify({
					'api_token': telegramBotApiTokenInput.value,
					'is_private': null,
				}),
			}).then(response => {
				if (response.ok) {
					updateTelegramBot();
					telegramBotApiTokenEditOrSaveOrCancel();
				}

				response.json().then(jsonResponse => {
					createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
				});
			});
		});
		telegramBotApiTokenCancelButton.addEventListener('click', telegramBotApiTokenEditOrSaveOrCancel);
	}

	var telegramBotIsPrivateCheckBox = document.querySelector('#telegramBotIsPrivateCheckBox');

	telegramBotIsPrivateCheckBox.addEventListener('click', function() {
		fetch(telegramBotUrl, {
			method: 'PATCH',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Token ${userApiToken}`,
			},
			body: JSON.stringify({
				'api_token': null,
				'is_private': telegramBotIsPrivateCheckBox.checked,
			}),
		}).then(response => {
			if (response.ok) {
				updateTelegramBotUsers();
			}

			response.json().then(jsonResponse => {
				createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
			});
		});
	});

	{
		const telegramBotStatusDiv = document.querySelector('#telegramBotStatus');
		const telegramBotStartOrStopButton = document.querySelector('#telegramBotStartOrStopButton');

		const checkTelegramBotStatus = (wait, extraFunc) => {
			fetch (telegramBotUrl, {
				method: 'GET',
				headers: {'Authorization': `Token ${userApiToken}`},
			}).then(response => {
				response.json().then(jsonResponse => {
					if (response.ok) {
						if (!jsonResponse['is_running'] && jsonResponse['is_stopped'] && wait == 'stop') {
							telegramBotStatusDiv.classList.replace('bg-success', 'bg-danger');
							telegramBotStatusDiv.innerHTML = telegramBotCardHeaderIsNotRunningText;

							telegramBotStartOrStopButton.classList.replace('btn-danger', 'btn-success');
							telegramBotStartOrStopButton.disabled = false;
							telegramBotStartOrStopButton.innerHTML = telegramBotStartButtonText;

							if (extraFunc != null) {
								extraFunc();
							}
						} else if (jsonResponse['is_running'] && !jsonResponse['is_stopped'] && wait == 'start') {
							telegramBotStatusDiv.classList.replace('bg-danger', 'bg-success');
							telegramBotStatusDiv.innerHTML = telegramBotCardHeaderIsRunningText;

							telegramBotStartOrStopButton.classList.replace('btn-success', 'btn-danger');
							telegramBotStartOrStopButton.disabled = false;
							telegramBotStartOrStopButton.innerHTML = telegramBotStopButtonText;

							if (extraFunc != null) {
								extraFunc();
							}
						}
					} else {
						createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
					}
				});
			});
		}

		const checkTelegramBotIsStopped = () => {
			const intervalCheckTelegramBotIsStoppedId = setInterval(() => checkTelegramBotStatus('stop', function() {
				telegramBotIsRunning = false;
				clearInterval(intervalCheckTelegramBotIsStoppedId);
				createAlert(mainAlertContainer, stopTelegramBotMessage, 'success');
			}), 3000);
		}

		fetch (telegramBotUrl, {
			method: 'GET',
			headers: {'Authorization': `Token ${userApiToken}`},
		}).then(response => {
			response.json().then(jsonResponse => {
				if (response.ok) {
					if (!jsonResponse['is_running'] && !jsonResponse['is_stopped']) {
						telegramBotStartOrStopButton.disabled = true;
						telegramBotStartOrStopButton.innerHTML = [
							'<div class="spinner-border spinner-border-sm role="status">',
							'	<span class="sr-only"></span>',
							'</div>',
						].join('');

						checkTelegramBotIsStopped();
					}
				} else {
					createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
				}
			});
		});

		telegramBotStartOrStopButton.addEventListener('click', function() {
			telegramBotStartOrStopButton.disabled = true;
			telegramBotStartOrStopButton.innerHTML = [
				'<div class="spinner-border spinner-border-sm role="status">',
				'	<span class="sr-only"></span>',
				'</div>',
			].join('');

			fetch(startOrStopTelegramBotUrl, {
				method: 'POST',
				headers: {'Authorization': `Token ${userApiToken}`},
			}).then(response => {
				if (response.ok) {
					if (telegramBotIsRunning) {
						checkTelegramBotIsStopped();
					} else {
						const intervalCheckTelegramBotIsStartedId = setInterval(() => checkTelegramBotStatus('start', function() {
							telegramBotIsRunning = true;
							clearInterval(intervalCheckTelegramBotIsStartedId);
							createAlert(mainAlertContainer, startTelegramBotMessage, 'success')
						}), 3000);
					}
				} else {
					response.json().then(jsonResponse => {
						createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
					});
				}
			});
		});
	}

	document.querySelector('#telegramBotDeleteButton').addEventListener('click', () => askConfirmModal(
		deleteTelegramBotAskConfirmModalTitle,
		deleteTelegramBotAskConfirmModalText,
		function() {
			fetch(telegramBotUrl, {
				method: 'DELETE',
				headers: {'Authorization': `Token ${userApiToken}`},
			}).then(response => {
				if (response.ok) {
					setTimeout("window.location.href = '../';", 1000);
				}

				response.json().then(jsonResponse => {
					createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
				});
			});
		}
	));
}
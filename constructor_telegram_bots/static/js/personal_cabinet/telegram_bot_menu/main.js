{
	const telegramBotApiToken = document.querySelector('#telegramBotApiToken');
	const telegramBotApiTokenEditButton = document.querySelector('#telegramBotApiTokenEditButton');
	const telegramBotApiTokenSaveButton = document.querySelector('#telegramBotApiTokenSaveButton');
	const telegramBotApiTokenCancelButton = document.querySelector('#telegramBotApiTokenCancelButton');

	function telegramBotApiTokenEditOrSaveOrCancel() {
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

		fetch(editTelegramBotApiTokenUrl, {
			method: 'POST',
			headers: {'Content-Type': 'application/json'},
			body: JSON.stringify(
				{
					'api_token': telegramBotApiTokenInput.value,
				}
			),
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
	fetch(editTelegramBotPrivateUrl, {
		method: 'POST',
		body: JSON.stringify(
			{
				'is_private': telegramBotIsPrivateCheckBox.checked,
			}
		),
		headers: {'Content-Type': 'application/json'},
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
	const telegramBotStartOrStopButton = document.querySelector('#telegramBotStartOrStopButton');

	telegramBotStartOrStopButton.addEventListener('click', function() {
		telegramBotStartOrStopButton.disabled = true;
		telegramBotStartOrStopButton.innerHTML = [
			'<div class="spinner-border spinner-border-sm role="status">',
			'	<span class="sr-only"></span>',
			'</div>',
		].join('');

		fetch((telegramBotIsRunning) ? stopTelegramBotUrl : startTelegramBotUrl, {
			method: 'POST',
		}).then(response => {
			if (response.ok) {
				const telegramBotStatus = document.querySelector('#telegramBotStatus');

				if (telegramBotIsRunning) {
					function checkTelegramBotIsStopped() {
						fetch (getTelegramBotDataUrl, {
							method: 'POST'
						}).then(response => {
							if (response.ok) {
								response.json().then(telegramBot => {
									if (telegramBot['is_stopped']) {
										intervalUpdateUsersIsRunning = false;
										telegramBotIsRunning = false;

										clearInterval(intervalUpdateUsersId)
										clearInterval(intervalCheckTelegramBotIsStoppedId)

										telegramBotStatus.classList.replace('bg-success', 'bg-danger');
										telegramBotStatus.innerHTML = telegramBotCardHeaderIsNotRunningText;

										telegramBotStartOrStopButton.classList.replace('btn-danger', 'btn-success');
										telegramBotStartOrStopButton.disabled = false;
										telegramBotStartOrStopButton.innerHTML = telegramBotStartButtonText;

										createAlert(mainAlertContainer, stopTelegramBotMessage, 'success');
									} 
								});
							} else {
								response.json().then(jsonResponse => {
									createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
								});
							}
						});
					}

					const intervalCheckTelegramBotIsStoppedId = setInterval(checkTelegramBotIsStopped, 3000)
				} else {
					intervalUpdateUsersIsRunning = true;
					telegramBotIsRunning = true;

					updateTelegramBotUsers();
					intervalUpdateUsersId = setInterval(updateTelegramBotUsers, 3000);

					telegramBotStatus.classList.replace('bg-danger', 'bg-success');
					telegramBotStatus.innerHTML = telegramBotCardHeaderIsRunningText;

					telegramBotStartOrStopButton.classList.replace('btn-success', 'btn-danger');
					telegramBotStartOrStopButton.disabled = false;
					telegramBotStartOrStopButton.innerHTML = telegramBotStopButtonText;

					createAlert(mainAlertContainer, startTelegramBotMessage, 'success');
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
		fetch(deleteTelegramBotUrl, {
			method: 'POST',
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

{
	let telegramBotTableLineApiToken = document.querySelector('#telegramBotTableLineApiToken');
	let telegramBotApiTokenEditButton = document.querySelector('#telegramBotApiTokenEditButton');
	let telegramBotApiTokenSaveButton = document.querySelector('#telegramBotApiTokenSaveButton');
	let telegramBotApiTokenCancelButton = document.querySelector('#telegramBotApiTokenCancelButton');

	function telegramBotApiTokenEditOrSaveOrCancel() {
		let telegramBotTableLineApiTokenInput = telegramBotTableLineApiToken.querySelector('input');

		if (telegramBotTableLineApiTokenInput == null) {
			telegramBotTableLineApiToken.innerHTML = `<input class="form-control" id="${telegramBotTableLineApiToken.innerHTML}" type="text" placeholder="Введите API-токен Telegram бота" value="${telegramBotTableLineApiToken.innerHTML}">`;
		} else {
			telegramBotTableLineApiToken.innerHTML = telegramBotTableLineApiTokenInput.id;
		}

		telegramBotApiTokenEditButton.classList.toggle('d-none');
		telegramBotApiTokenSaveButton.classList.toggle('d-none');
		telegramBotApiTokenCancelButton.classList.toggle('d-none');
	}

	telegramBotApiTokenEditButton.addEventListener('click', telegramBotApiTokenEditOrSaveOrCancel);

	telegramBotApiTokenSaveButton.addEventListener('click', function() {
		let telegramBotTableLineApiTokenInput = telegramBotTableLineApiToken.querySelector('input');

		fetch(editTelegramBotApiTokenUrl, {
			method: 'POST',
			headers: {'Content-Type': 'application/json'},
			body: JSON.stringify({'api_token': telegramBotTableLineApiTokenInput.value}),
		}).then(response => {
			if (response.ok) {
				response.text().then(responseText => {
					updateTelegramBot();
					telegramBotApiTokenEditOrSaveOrCancel();
					createAlert(mainAlertContainer, responseText, 'success');
				});
			} else {response.text().then(responseText => createAlert(mainAlertContainer, responseText, 'danger'))}
		});
	});

	telegramBotApiTokenCancelButton.addEventListener('click', telegramBotApiTokenEditOrSaveOrCancel);
}

var telegramBotIsPrivateCheckBox = document.querySelector('#telegramBotIsPrivateCheckBox');

telegramBotIsPrivateCheckBox.addEventListener('click', function() {
	fetch(editTelegramBotPrivateUrl, {
		method: 'POST',
		headers: {'Content-Type': 'application/json'},
		body: JSON.stringify({'is_private': telegramBotIsPrivateCheckBox.checked}),
	}).then(response => {
		if (response.ok) {
			response.text().then(responseText => {
				updateTelegramBotUsers();
				createAlert(mainAlertContainer, responseText, 'success');
			});
		} else {response.text().then(responseText => createAlert(mainAlertContainer, responseText, 'danger'))}
	});
});

{
	let telegramBotStartOrStopButton = document.querySelector('#telegramBotStartOrStopButton');

	telegramBotStartOrStopButton.addEventListener('click', function() {
		telegramBotStartOrStopButton.innerHTML = [
			'<div class="spinner-border spinner-border-sm role="status">',
			'	<span class="sr-only"></span>',
			'</div>',
		].join('');
		telegramBotStartOrStopButton.disabled = true;

		fetch((telegramBotIsRunning) ? stopTelegramBotUrl : startTelegramBotUrl, {
			method: 'POST',
		}).then(response => {
			if (response.ok) {
				let cardHeader = document.querySelector('.card-header');

				if (telegramBotIsRunning) {
					let intervalCheckTelegramBotIsStoppedId;

					function checkTelegramBotIsStopped() {
						fetch (getTelegramBotData, {
							method: 'POST'
						}).then(response => {
							if (response.ok) {
								response.json().then(telegramBot => {
									if (telegramBot['is_stopped']) {
										intervalUpdateUsersIsRunning = false;
										telegramBotIsRunning = false;

										clearInterval(intervalUpdateUsersId)
										clearInterval(intervalCheckTelegramBotIsStoppedId)

										cardHeader.classList.replace('bg-success', 'bg-danger');
										cardHeader.innerHTML = 'Telegram бот выключен';

										telegramBotStartOrStopButton.disabled = false;
										telegramBotStartOrStopButton.classList.replace('btn-danger', 'btn-success');
										telegramBotStartOrStopButton.innerHTML = 'Включить Telegram бота';

										createAlert(mainAlertContainer, 'Вы успешно выключили Telegram бота.', 'success');
									} 
								});
							} else {response.text().then(responseText => createAlert(mainAlertContainer, responseText, 'danger'))}
						});
					}

					intervalCheckTelegramBotIsStoppedId = setInterval(checkTelegramBotIsStopped, 3000)
				} else {
					intervalUpdateUsersIsRunning = true;
					telegramBotIsRunning = true;

					updateTelegramBotUsers();
					intervalUpdateUsersId = setInterval(updateTelegramBotUsers, 3000);

					cardHeader.classList.replace('bg-danger', 'bg-success');
					cardHeader.innerHTML = 'Telegram бот включен';

					telegramBotStartOrStopButton.disabled = false;
					telegramBotStartOrStopButton.classList.replace('btn-success', 'btn-danger');
					telegramBotStartOrStopButton.innerHTML = 'Выключить Telegram бота';

					createAlert(mainAlertContainer, 'Вы успешно включили Telegram бота.', 'success');
				}
				
			} else {response.text().then(responseText => createAlert(mainAlertContainer, responseText, 'danger'))}
		});
	});
}

document.querySelector('#telegramBotDeleteButton').addEventListener('click', () => askConfirmModal(
	'Удаление Telegram бота',
	'Вы точно хотите удалить Telegram бота?',
	function() {
		fetch(deleteTelegramBotUrl, {
			method: 'POST',
		}).then(response => {
			if (response.ok) {
				response.text().then(responseText => {
					setTimeout("window.location.href = '../';", 1000);
					createAlert(mainAlertContainer, responseText, 'success');
				});
			} else {response.text().then(responseText => createAlert(mainAlertContainer, responseText, 'danger'))}
		});
	}
));

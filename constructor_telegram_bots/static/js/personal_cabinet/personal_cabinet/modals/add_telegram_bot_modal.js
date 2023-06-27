{
	const addTelegramBot = {
		modal: new bootstrap.Modal('#addTelegramBotModal'),

		alertContainer: document.querySelector('#addTelegramBotModalAlertContainer'),

		apiTokenInput: document.querySelector('#addTelegramBotApiTokenInput'),
		IsPrivateCheckBox: document.querySelector('#addTelegramBotIsPrivateCheckBox'),

		button: document.querySelector('#addTelegramBotModalButton'),
	}

	document.querySelector('#addTelegramBotButton').addEventListener('click', function() {
		fetch(addTelegramBotUrl, {
			method: 'POST',
			body: JSON.stringify(
				{
					'api_token': addTelegramBot.apiTokenInput.value,
					'is_private': addTelegramBot.IsPrivateCheckBox.checked,
				}
			),
			headers: {'Content-Type': 'application/json'},
		}).then(response => {
			response.json().then(jsonResponse => {
				if (response.ok) {
					updateTelegramBots();

					addTelegramBot.modal.toggle();

					createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
				} else {
					createAlert(addTelegramBot.alertContainer, jsonResponse['message'], jsonResponse['level']);
				}
			});
		});
	});

	addTelegramBot.button.addEventListener('click', function() {
		addTelegramBot.alertContainer.innerHTML = '';

		addTelegramBot.apiTokenInput.value = '';
		addTelegramBot.IsPrivateCheckBox.checked = false;

		addTelegramBot.modal.toggle();
	});
}

{
	const addTelegramBotModalBootstrap = new bootstrap.Modal('#addTelegramBotModal');

	const addTelegramBotModalAlertContainer = document.querySelector('#addTelegramBotModalAlertContainer');

	const addTelegramBotApiTokenInput = document.querySelector('#addTelegramBotApiTokenInput');
	const addTelegramBotIsPrivateCheckBox = document.querySelector('#addTelegramBotIsPrivateCheckBox');

	document.querySelector('#addTelegramBotButton').addEventListener('click', function() {
		fetch(addTelegramBotUrl, {
			method: 'POST',
			headers: {'Content-Type': 'application/json'},
			body: JSON.stringify(
				{
					'api_token': addTelegramBotApiTokenInput.value,
					'is_private': addTelegramBotIsPrivateCheckBox.checked,
				}
			),
		}).then(response => {
			response.json().then(jsonResponse => {
				if (response.ok) {
					showTelegramBots();

					addTelegramBotModalBootstrap.toggle();

					createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
				} else {
					createAlert(addTelegramBotModalAlertContainer, jsonResponse['message'], jsonResponse['level']);
				}
			});
		});
	});

	document.querySelector('#addTelegramBotModalButton').addEventListener('click', function() {
		addTelegramBotModalAlertContainer.innerHTML = '';

		addTelegramBotApiTokenInput.value = '';
		addTelegramBotIsPrivateCheckBox.checked = false;

		addTelegramBotModalBootstrap.toggle();
	});
}

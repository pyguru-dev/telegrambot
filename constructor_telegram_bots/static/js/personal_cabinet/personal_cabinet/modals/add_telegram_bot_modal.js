{
	let addTelegramBotModalBootstrap = new bootstrap.Modal('#addTelegramBotModal');

	let addTelegramBotModalAlertContainer = document.querySelector('#addTelegramBotModalAlertContainer');

	let addTelegramBotApiTokenInput = document.querySelector('#addTelegramBotApiTokenInput');
	let addTelegramBotIsPrivateCheckBox = document.querySelector('#addTelegramBotIsPrivateCheckBox');

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
				} else {createAlert(addTelegramBotModalAlertContainer, jsonResponse['message'], jsonResponse['level'])}
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

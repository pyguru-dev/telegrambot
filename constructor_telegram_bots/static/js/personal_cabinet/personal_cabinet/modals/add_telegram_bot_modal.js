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
			if (response.ok) {
				response.text().then(responseText => {
					addTelegramBotModalBootstrap.toggle();
	
					get_telegram_bots();
	
					createAlert(mainAlertContainer, responseText, 'success');
				});
			} else {response.text().then(responseText => createAlert(addTelegramBotModalAlertContainer, responseText, 'danger'))}
		});
	});

	document.querySelector('#addTelegramBotModalButton').addEventListener('click', function() {
		addTelegramBotModalAlertContainer.innerHTML = '';

		addTelegramBotApiTokenInput.value = '';
		addTelegramBotIsPrivateCheckBox.checked = false;

		addTelegramBotModalBootstrap.toggle();
	});
}

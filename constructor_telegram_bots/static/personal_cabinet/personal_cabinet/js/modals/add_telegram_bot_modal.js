{
	const addTelegramBotBootstrapModal = new bootstrap.Modal('#addTelegramBotModal');
	const addTelegramBotModalAlertContainer = document.querySelector('#addTelegramBotModalAlertContainer');
	const addTelegramBotModalApiTokenInput = document.querySelector('#addTelegramBotModalApiTokenInput');
	const addTelegramBotModalIsPrivateCheckBox = document.querySelector('#addTelegramBotModalIsPrivateCheckBox');

	document.querySelector('#addTelegramBotModalAddTelegramBotButton').addEventListener('click', function() {
		fetch(telegramBotsUrl, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Token ${userApiToken}`,
			},
			body: JSON.stringify({
				'api_token': addTelegramBotModalApiTokenInput.value,
				'is_private': addTelegramBotModalIsPrivateCheckBox.checked,
			}),
		}).then(response => {
			response.json().then(jsonResponse => {
				if (response.ok) {
					const notHaveTelegramBotDiv = document.querySelector('#notAddedTelegramBot');

					if (notHaveTelegramBotDiv != null) {
						notHaveTelegramBotDiv.remove();
					}

					addTelegramBot(jsonResponse['telegram_bot']);

					addTelegramBotBootstrapModal.toggle();

					createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
				} else {
					createAlert(addTelegramBotModalAlertContainer, jsonResponse['message'], jsonResponse['level']);
				}
			});
		});
	});

	document.querySelector('#addTelegramBotModalButton').addEventListener('click', function() {
		addTelegramBotModalAlertContainer.innerHTML = '';

		addTelegramBotModalApiTokenInput.value = '';
		addTelegramBotModalIsPrivateCheckBox.checked = false;

		addTelegramBotBootstrapModal.toggle();
	});
}
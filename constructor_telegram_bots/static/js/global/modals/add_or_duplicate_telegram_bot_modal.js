{
	let addOrDuplicateTelegramBotModalBootstrap = new bootstrap.Modal('#addOrDuplicateTelegramBotModal');

	let addOrDuplicateTelegramBotModalAlertPlaceholder = document.querySelector('#addOrDuplicateTelegramBotModalAlertPlaceholder');

	let addOrDuplicateTelegramBotApiTokenInput = document.querySelector('#addOrDuplicateTelegramBotApiTokenInput');
	let addOrDuplicateTelegramBotIsPrivateCheckBox = document.querySelector('#addOrDuplicateTelegramBotIsPrivateCheckBox');

	document.querySelector('#addOrDuplicateTelegramBotButton').addEventListener('click', function() {
		let request = new XMLHttpRequest();
		request.open('POST', (window.location.pathname == '/personal-cabinet/') ? '/telegram-bot/add/' : `/telegram-bot/${telegramBotId}/duplicate/`, true);
		request.setRequestHeader('Content-Type', 'application/json');
		request.onreadystatechange = checkRequestResponse(function() {
			if (request.status == 200) {
				addOrDuplicateTelegramBotModalBootstrap.toggle();
				
				if (window.location.pathname == '/personal-cabinet/') {
					get_telegram_bots();
				}

				myAlert(mainAlertPlaceholder, request.responseText, 'success');
			} else {
				myAlert(addOrDuplicateTelegramBotModalAlertPlaceholder, request.responseText, 'danger');
			}
		});
		request.send(JSON.stringify(
			{
				'api_token': addOrDuplicateTelegramBotApiTokenInput.value,
				'is_private': addOrDuplicateTelegramBotIsPrivateCheckBox.checked,
			}
		));
	});

	{
		document.querySelector('#addOrDuplicateTelegramBotModalButton').addEventListener('click', function() {
			addOrDuplicateTelegramBotModalAlertPlaceholder.innerHTML = '';
			addOrDuplicateTelegramBotApiTokenInput.value = '';
			addOrDuplicateTelegramBotIsPrivateCheckBox.checked = true;
	
			addOrDuplicateTelegramBotModalBootstrap.toggle();
		});
	}
}

{
	var mainAlertPlaceholder = document.querySelector('#mainAlertPlaceholder');

	var addTelegramBotModalBootstrap = new bootstrap.Modal('#addTelegramBotModal');

	var addTelegramBotModalAlertPlaceholder = document.querySelector('#addTelegramBotModalAlertPlaceholder');

	var addTelegramBotApiTokenInput = document.querySelector('#addTelegramBotApiTokenInput');

	document.querySelector('#addTelegramBotButton').addEventListener('click', function() {
		let request = new XMLHttpRequest();
		request.open('POST', '/telegram-bot/add/', true);
		request.setRequestHeader('Content-Type', 'application/json');
		request.onreadystatechange = checkRequestResponse(function() {
			if (request.status == 200) {
				addTelegramBotModalBootstrap.toggle();

				get_added_telegram_bots();
				myAlert(mainAlertPlaceholder, request.responseText, 'success');
			} else {
				myAlert(addTelegramBotModalAlertPlaceholder, request.responseText, 'danger');
			}
		});
		request.send(JSON.stringify(
			{
				'api_token': addTelegramBotApiTokenInput.value,
				'private': document.querySelector('#addTelegramBotPrivateCheckBox').checked,
			}
		));
	});
}
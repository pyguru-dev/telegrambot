{
	let mainAlertPlaceholder = document.querySelector('#mainAlertPlaceholder');

	document.querySelector('#addTelegramBotButton').addEventListener('click', function() {
		let request = new XMLHttpRequest();
		request.open('POST', '/telegram_bot/add/', true);
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
				'token': document.querySelector('#addTelegramBotTokenInput').value,
				'private': document.querySelector('#addTelegramBotPrivateCheckBox').checked,
			}
		));
	});
}
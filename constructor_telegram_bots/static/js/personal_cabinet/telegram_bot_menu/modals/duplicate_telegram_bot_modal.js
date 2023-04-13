{
	var duplicateTelegramBotModalBootstrap = new bootstrap.Modal('#duplicateTelegramBotModal');

	let duplicateTelegramBotModalAlertPlaceholder = document.querySelector('#duplicateTelegramBotModalAlertPlaceholder');

	document.querySelector('#duplicateTelegramBotButton').addEventListener('click', function() {
		let request = new XMLHttpRequest();
		request.open('POST', `/telegram_bot/${telegramBotId}/duplicate/`, true);
		request.setRequestHeader('Content-Type', 'application/json');
		request.onreadystatechange = checkRequestResponse(function() {
			if (request.status == 200) {
				duplicateTelegramBotModalBootstrap.toggle();

				myAlert(mainAlertPlaceholder, request.responseText, 'success');
			} else {
				myAlert(duplicateTelegramBotModalAlertPlaceholder, request.responseText, 'danger');
			}
		});
		request.send(JSON.stringify(
			{
				'token': document.querySelector('#duplicateTelegramBotTokenInput').value,
				'private': document.querySelector('#duplicateTelegramBotPrivateCheckBox').checked,
			}
		));
	});
}
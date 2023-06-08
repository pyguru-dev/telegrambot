var telegramBotIsPrivateCheckBox = document.querySelector('#telegramBotIsPrivateCheckBox');

telegramBotIsPrivateCheckBox.addEventListener('click', function() {
	fetch(editTelegramBotUrl, {
		method: 'POST',
		headers: {'Content-Type': 'application/json'},
		body: JSON.stringify({'is_private': this.checked,}),
	}).then(response => {
		if (response.ok) {
			response.text().then(responseText => {
				getTelegramBotUsers();

				createAlert(mainAlertContainer, responseText, 'success');
			});
		} else {response.text().then(responseText => createAlert(mainAlertContainer, responseText, 'danger'))}
	});
});

{
	let startOrStopTelegramBotButton = document.querySelector('#startOrStopTelegramBotButton');

	startOrStopTelegramBotButton.addEventListener('click', function() {
		this.innerHTML = [
			'<div class="spinner-border spinner-border-sm role="status">',
			'	<span class="sr-only"></span>',
			'</div>',
		].join('');
		this.disabled = true;

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

										startOrStopTelegramBotButton.disabled = false;
										startOrStopTelegramBotButton.classList.replace('btn-danger', 'btn-success');
										startOrStopTelegramBotButton.innerHTML = 'Включить Telegram бота';

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

					getTelegramBotUsers();
					intervalUpdateUsersId = setInterval(getTelegramBotUsers, 3000);

					cardHeader.classList.replace('bg-danger', 'bg-success');
					cardHeader.innerHTML = 'Telegram бот включен';

					startOrStopTelegramBotButton.disabled = false;
					startOrStopTelegramBotButton.classList.replace('btn-success', 'btn-danger');
					startOrStopTelegramBotButton.innerHTML = 'Выключить Telegram бота';

					createAlert(mainAlertContainer, 'Вы успешно включили Telegram бота.', 'success');
				}
				
			} else {response.text().then(responseText => createAlert(mainAlertContainer, responseText, 'danger'))}
		});
	});
}

document.querySelector('#deleteTelegramBotButton').addEventListener('click', () => askConfirmModal(
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

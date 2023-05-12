{
    var telegramBotIsPrivateCheckBox = document.querySelector('#telegramBotIsPrivateCheckBox');

    telegramBotIsPrivateCheckBox.addEventListener('click', function() {
        let request = new XMLHttpRequest();
        request.open('POST', `/telegram-bot/${telegramBotId}/edit/`, true);
        request.setRequestHeader('Content-Type', 'application/json');
        request.onreadystatechange = checkRequestResponse(function() {
            let telegramBotAllowedUserButtons = document.querySelectorAll('.telegram-bot-allowed-user-button');

            if (telegramBotIsPrivateCheckBox.checked) {
                for (let i = 0; i < telegramBotAllowedUserButtons.length; i++) {
                    telegramBotAllowedUserButtons[i].classList.remove('d-none');
                }
            } else {
                for (let i = 0; i < telegramBotAllowedUserButtons.length; i++) {
                    telegramBotAllowedUserButtons[i].classList.add('d-none');
                }
            }

            myAlert(mainAlertPlaceholder, request.responseText, 'success');
        });
        request.send(JSON.stringify(
            {
                'is_private': this.checked,
            }
        ));
    });
}

{
	let startOrStopTelegramBotButton = document.querySelector('#startOrStopTelegramBotButton');
	startOrStopTelegramBotButton.addEventListener('click', function() {
		this.disabled = true;

		let request = new XMLHttpRequest();
		request.open('POST', (telegramBotIsRunning) ? `/telegram-bot/${telegramBotId}/stop/` : `/telegram-bot/${telegramBotId}/start/`, true);
		request.onreadystatechange = checkRequestResponse(function() {
			if (request.status == 200) {
				let cardHeader = document.querySelector('.card-header');

				if (telegramBotIsRunning) {
					telegramBotIsRunning = false;

					clearInterval(setIntervalId)

					cardHeader.innerHTML = 'Telegram бот выключен';
					cardHeader.classList.replace('bg-success', 'bg-danger');

					startOrStopTelegramBotButton.innerHTML = 'Включить Telegram бота';
					startOrStopTelegramBotButton.classList.replace('btn-danger', 'btn-success');
				} else {
					telegramBotIsRunning = true;

					getTelegramBotUsers();
					setIntervalId = setInterval(getTelegramBotUsers, 1500);

					cardHeader.innerHTML = 'Telegram бот включен';
					cardHeader.classList.replace('bg-danger', 'bg-success');
					
					startOrStopTelegramBotButton.innerHTML = 'Выключить Telegram бота';
					startOrStopTelegramBotButton.classList.replace('btn-success', 'btn-danger');
				}

				startOrStopTelegramBotButton.disabled = false;

				myAlert(mainAlertPlaceholder, request.responseText, 'success');
			} else {
				myAlert(mainAlertPlaceholder, request.responseText, 'danger');
			}
		});
		request.send();
	});

	document.querySelector('#deleteTelegramBotButton').addEventListener('click', () => askConfirmModal(
		'Удаление Telegram бота',
		'Вы точно хотите удалить Telegram бота?',
		function() {
			let request = new XMLHttpRequest();
			request.open('POST', `/telegram-bot/${telegramBotId}/delete/`, true);
			request.setRequestHeader('Content-Type', 'application/json');
			request.onreadystatechange = checkRequestResponse(function() {
				if (request.status == 200) {
					setTimeout("window.location.href = '../';", 1000);

					myAlert(mainAlertPlaceholder, request.responseText, 'success');
				} else {
					myAlert(mainAlertPlaceholder, request.responseText, 'danger');
				}
			});
			request.send();
		}
	));
}
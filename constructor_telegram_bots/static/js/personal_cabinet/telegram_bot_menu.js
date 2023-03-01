const startOrStopTelegramBotButton = document.querySelector('#startOrStopTelegramBotButton')
startOrStopTelegramBotButton.addEventListener('click', function() {
	var request = new XMLHttpRequest();
	var buttomText = this.innerHTML
	var num = 0;

	if (buttomText == 'Включить Telegram бота') {
		request.open('POST', `/telegram_bot/${telegramBotId}/start/`, true);
	} else {
		request.open('POST', `/telegram_bot/${telegramBotId}/stop/`, true);
	}

	request.onreadystatechange = function() {
		num ++;

		if (num > 2) {
			if (request.status == 200) {
				const cardHeader = document.querySelector('.card-header');
				
				if (buttomText == 'Включить Telegram бота') {
					cardHeader.innerHTML = 'Бот включен';
					cardHeader.setAttribute('class', cardHeader.getAttribute('class').replace('danger', 'success'));
					
					startOrStopTelegramBotButton.innerHTML = 'Выключить Telegram бота'
					startOrStopTelegramBotButton.setAttribute('class', startOrStopTelegramBotButton.getAttribute('class').replace('success', 'danger'));
				} else {
					cardHeader.innerHTML = 'Бот выключен';
					cardHeader.setAttribute('class', cardHeader.getAttribute('class').replace('success', 'danger'));

					startOrStopTelegramBotButton.innerHTML = 'Включить Telegram бота'
					startOrStopTelegramBotButton.setAttribute('class', startOrStopTelegramBotButton.getAttribute('class').replace('danger', 'success'));
				}

				myAlert(request.responseText, 'success');
			} else {
				myAlert(request.responseText, 'danger');
			}
		}
	}
	request.send();
});

const deleteTelegramBotButton = document.querySelector('#deleteTelegramBotButton');
deleteTelegramBotButton.addEventListener('click', function() {
	var num = 0;
	
	var request = new XMLHttpRequest();
	request.open('POST', `/telegram_bot/${telegramBotId}/delete/`, true);
	request.onreadystatechange = function() {
		num ++;

		if (num > 2) {
			if (request.status == 200) {
				setTimeout("window.location.href = '../';", 1000);

				myAlert(request.responseText, 'success');
			} else {
				myAlert(request.responseText, 'danger');
			}
		}
	}
	request.send();
});

const telegramBotPrivateCheckBox = document.querySelector('#telegramBotPrivateCheckBox');
telegramBotPrivateCheckBox.addEventListener('click', function() {
	var request = new XMLHttpRequest();
	var num = 0;
	
	if (this.value == 'ON') {
		var telegramBotPrivate = false;
		this.value = 'OFF';
	} else {
		var telegramBotPrivate = true;
		this.value = 'ON';
	}

	request.open('POST', `/telegram_bot/${telegramBotId}/edit/private/`, true);
	request.setRequestHeader('Content-Type', 'application/json');
	request.onreadystatechange = function() {
		num ++;

		if (num > 2) {
			if (request.status == 200) {
				myAlert(request.responseText, 'success');
			} else {
				myAlert(request.responseText, 'danger');
			}
		}
	}
	request.send(JSON.stringify(
		{
			'telegram_bot_private': telegramBotPrivate,
		}
	));
});

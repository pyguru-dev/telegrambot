const addTelegramBotModalBootstrap = new bootstrap.Modal('#addTelegramBotModal')

get_added_telegram_bots();
function get_added_telegram_bots() {
	var request = new XMLHttpRequest();
	var num = 0;

	request.open('POST', '/user/get_added_telegram_bots/', true);
	request.setRequestHeader('Content-Type', 'application/json');
	request.onreadystatechange = function() {
		num ++;

		if (num >= 2) {
			if (request.status == 200) {
				const addedTelegramBots = document.querySelector('#addedTelegramBots');

				addedTelegramBots.innerHTML = request.responseText;
			} else {
				myAlert(request.responseText, 'danger');
			}
		}
	}
	request.send();
}

const addTelegramBotModalButton = document.querySelector('#addTelegramBotModalButton');
addTelegramBotModalButton.addEventListener('click', function() {
	addTelegramBotModalBootstrap.toggle()
});

const telegramBotPrivateCheckBox = document.querySelector('#telegramBotPrivateCheckBox');
telegramBotPrivateCheckBox.addEventListener('click', function() {
	if (this.value == 'ON') {
		this.value = 'OFF';
	} else {
		this.value = 'ON';
	}
});

const addTelegramBotButton = document.querySelector('#addTelegramBotButton');
addTelegramBotButton.addEventListener('click', function() {
	var request = new XMLHttpRequest();
	var num = 0;

	var telegramBotToken = document.querySelector('#addTelegramBotTokenInput').value;
	var telegramBotPrivate = document.querySelector('#telegramBotPrivateCheckBox').value;

	if (telegramBotPrivate == 'ON') {
		telegramBotPrivate = true;
	} else {
		telegramBotPrivate = false;
	}

	request.open('POST', '/telegram_bot/add/', true);
	request.setRequestHeader('Content-Type', 'application/json');
	request.onreadystatechange = function() {
		num ++;

		if (num > 2) {
			if (request.status == 200) {
				setTimeout('addTelegramBotModalBootstrap.toggle()', 1000);

				get_added_telegram_bots();
				myAlert(request.responseText, 'success');
			} else {
				myAlert(request.responseText, 'danger');
			}
		}
	}
	request.send(JSON.stringify(
		{
			'telegram_bot_token': telegramBotToken,
			'telegram_bot_private': telegramBotPrivate,
		}
	));
});
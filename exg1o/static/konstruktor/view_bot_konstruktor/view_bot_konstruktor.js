function hideOrShowButtonClick() {
	var inputPasswordElement = document.querySelector('.bot-token-input-control');

	if (inputPasswordElement.getAttribute('type') == 'password') {
		inputPasswordElement.setAttribute('type', 'text');

		var buttonElement = document.getElementById('hideBotToken');
		buttonElement.setAttribute('id', 'showBotToken');
	} else {
		inputPasswordElement.setAttribute('type', 'password');

		var buttonElement = document.getElementById('showBotToken');
		buttonElement.setAttribute('id', 'hideBotToken');
	}
}

function startBotButtonClick() {
	var request = new XMLHttpRequest();
	request.open('POST', 'start_bot/', true);
	request.setRequestHeader('Content-Type', 'application/json');
	request.onreadystatechange = function() {
		if (request.status == 200) {
			showSuccessMessage(request.responseText);

			var startBotButtonElement = document.querySelector('.start-bot-button-control');
			startBotButtonElement.setAttribute('class', 'stop-bot-button-control');
			startBotButtonElement.setAttribute('onclick', 'stopBotButtonClick()');
			startBotButtonElement.innerHTML = 'Остоновить бота';
		} else {
			showErrorMessage(request.responseText);
		}
	}
	request.send();
}

function stopBotButtonClick() {
	var request = new XMLHttpRequest();
	request.open('POST', 'stop_bot/', true);
	request.setRequestHeader('Content-Type', 'application/json');
	request.onreadystatechange = function() {
		if (request.status == 200) {
			showSuccessMessage(request.responseText);

			var stopBotButtonElement = document.querySelector('.stop-bot-button-control');
			stopBotButtonElement.setAttribute('class', 'start-bot-button-control');
			stopBotButtonElement.setAttribute('onclick', 'startBotButtonClick()');
			stopBotButtonElement.innerHTML = 'Запустить бота';
		} else {
			showErrorMessage(request.responseText);
		}
	}
	request.send();
}

function saveBotSettingsButtonClick() {
	var botName = document.querySelector('.bot-name-input-control').value;
	var botToken = document.querySelector('.bot-token-input-control').value;

	var request = new XMLHttpRequest();
	request.open('POST', 'save_bot_settings/', true);
	request.setRequestHeader('Content-Type', 'application/json');
	data = JSON.stringify(
		{
			'bot_name': botName,
			'bot_token': botToken
		}
	)
	request.onreadystatechange = function() {
		setInterval("window.location.href = '';", 1000)
		if (request.status == 200) {
			showSuccessMessage(request.responseText);
		} else {
			showErrorMessage(request.responseText);
		}
	}
	request.send(data);
}

function clearLogButtonClick() {
	var request = new XMLHttpRequest();
	request.open('POST', 'clear_log/', true);
	request.setRequestHeader('Content-Type', 'application/json');
	request.onreadystatechange = function() {
		setInterval("window.location.href = '';", 1000)
		if (request.status == 200) {
			showSuccessMessage(request.responseText);
		} else {
			showErrorMessage(request.responseText);
		}
	}
	request.send();
}
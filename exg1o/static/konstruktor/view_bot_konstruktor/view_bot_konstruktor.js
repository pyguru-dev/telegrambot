var intervalId;

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
	sendRequestToServer(
		request,
		'start_bot/',
		'',
		function() {
			if (request.status == 200) {
				clearInterval(intervalId);
				intervalId = setInterval(() => hideMessage(), 1000);
				showSuccessMessage(request.responseText);

				var startBotButtonElement = document.querySelector('.start-bot-button-control');
				startBotButtonElement.setAttribute('class', 'stop-bot-button-control');
				startBotButtonElement.setAttribute('onclick', 'stopBotButtonClick()');
				startBotButtonElement.innerHTML = 'Остоновить бота';
			} else {
				showErrorMessage(request.responseText);
			}
		}
	);
}

function stopBotButtonClick() {
	var request = new XMLHttpRequest();
	sendRequestToServer(
		request,
		'stop_bot/',
		'',
		function() {
			if (request.status == 200) {
				clearInterval(intervalId);
				intervalId = setInterval(() => hideMessage(), 1000);
				showSuccessMessage(request.responseText);

				var stopBotButtonElement = document.querySelector('.stop-bot-button-control');
				stopBotButtonElement.setAttribute('class', 'start-bot-button-control');
				stopBotButtonElement.setAttribute('onclick', 'startBotButtonClick()');
				stopBotButtonElement.innerHTML = 'Запустить бота';
			} else {
				showErrorMessage(request.responseText);
			}
		}
	);
}

function saveBotSettingsButtonClick() {
	var botName = document.querySelector('.bot-name-input-control').value;
	var botToken = document.querySelector('.bot-token-input-control').value;

	var request = new XMLHttpRequest();
	sendRequestToServer(
		request,
		'save_bot_settings/',
		JSON.stringify(
			{
				'bot_name': botName,
				'bot_token': botToken
			}
		),
		function() {;
			if (request.status == 200) {
				clearInterval(intervalId);
				intervalId = setInterval(() => hideMessage(), 1000);
				showSuccessMessage(request.responseText);
			} else {
				showErrorMessage(request.responseText);
			}
		}
	);
}

function clearLogButtonClick() {
	var request = new XMLHttpRequest();
	sendRequestToServer(
		request,
		'clear_log/',
		'',
		function() {
			if (request.status == 200) {
				clearInterval(intervalId);
				intervalId = setInterval(() => hideMessage(), 1000);
				showSuccessMessage(request.responseText);

				var botLogTableElement = document.querySelector('.bot-log-table');
				botLogTableElement.innerHTML = '';
			}
		}
	);
}

function updateLogButtonClick() {
	var request = new XMLHttpRequest();
	sendRequestToServer(
		request,
		'get_log/',
		'',
		function() {
			if (request.status == 200) {
				clearInterval(intervalId);
				intervalId = setInterval(() => hideMessage(), 1000);
				showSuccessMessage('Успешная обвновление логов.');

				var botLogTableElement = document.querySelector('.bot-log-table');
				botLogTableElement.innerHTML = request.responseText;
			}
		}
	);
}

function addCommandButtonClick(link) {
	var request = new XMLHttpRequest();
	sendRequestToServer(
		request,
		link,
		'',
		function() {
			if (request.status == 200) {
				window.location.href = link;
			} else {
				clearInterval(intervalId);
				intervalId = setInterval(() => hideMessage(), 1000);
				showErrorMessage(request.responseText);
			}
		}
	);
}
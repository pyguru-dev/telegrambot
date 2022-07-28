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

function checkUserWindowScreenForOtherContainer() {
	const screenWidth = window.screen.width;
	var otherContainerElement = document.querySelector('.container#other');
	var messageElementHeight = document.querySelector('.message-container').clientHeight;

	if (screenWidth >= 320 && screenWidth < 768) {
		otherContainerElement.style = 'top: ' + (860 + messageElementHeight) + 'px;';
	}
	if (screenWidth >= 768 && screenWidth < 1000) {
		otherContainerElement.style = 'top: ' + (520 + messageElementHeight) + 'px;';
	}
	if (screenWidth >= 1000 && screenWidth < 1799) {
		otherContainerElement.style = 'top: ' + (555 + messageElementHeight) + 'px;';
	}
	if (screenWidth >= 1800) {
		otherContainerElement.style = 'top: ' + (124 + messageElementHeight) + 'px;';
	}
}

function hideMessageOther() {
	const screenWidth = window.screen.width;
	var otherContainerElement = document.querySelector('.container#other');

	hideMessage();

	if (screenWidth >= 320 && screenWidth < 768) {
		otherContainerElement.style = 'top: 860px;';
	}
	if (screenWidth >= 768 && screenWidth < 1000) {
		otherContainerElement.style = 'top: 520px;';
	}
	if (screenWidth >= 1000 && screenWidth < 1799) {
		otherContainerElement.style = 'top: 555px;';
	}
	if (screenWidth >= 1800) {
		otherContainerElement.style = 'top: 124px;';
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
				intervalId = setInterval(() => hideMessageOther(), 1000);
				showSuccessMessage(request.responseText);
				checkUserWindowScreenForOtherContainer();

				var startBotButtonElement = document.querySelector('.start-bot-button-control');
				startBotButtonElement.setAttribute('class', 'stop-bot-button-control');
				startBotButtonElement.setAttribute('onclick', 'stopBotButtonClick()');
				startBotButtonElement.innerHTML = 'Остоновить бота';
			} else {
				showErrorMessage(request.responseText);
				checkUserWindowScreenForOtherContainer();
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
				intervalId = setInterval(() => hideMessageOther(), 1000);
				showSuccessMessage(request.responseText);
				checkUserWindowScreenForOtherContainer();

				var stopBotButtonElement = document.querySelector('.stop-bot-button-control');
				stopBotButtonElement.setAttribute('class', 'start-bot-button-control');
				stopBotButtonElement.setAttribute('onclick', 'startBotButtonClick()');
				stopBotButtonElement.innerHTML = 'Запустить бота';
			} else {
				showErrorMessage(request.responseText);
				checkUserWindowScreenForOtherContainer();
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
				intervalId = setInterval(() => hideMessageOther(), 1000);
				showSuccessMessage(request.responseText);
				checkUserWindowScreenForOtherContainer();
			} else {
				showErrorMessage(request.responseText);
				checkUserWindowScreenForOtherContainer();
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
				intervalId = setInterval(() => hideMessageOther(), 1000);
				showSuccessMessage(request.responseText);
				checkUserWindowScreenForOtherContainer();

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
				intervalId = setInterval(() => hideMessageOther(), 1000);
				showSuccessMessage('Успешная обвновление логов.');
				checkUserWindowScreenForOtherContainer();

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
				intervalId = setInterval(() => hideMessageOther(), 1000);
				showSuccessMessage(request.responseText);
				checkUserWindowScreenForOtherContainer();
			}
		}
	);
}
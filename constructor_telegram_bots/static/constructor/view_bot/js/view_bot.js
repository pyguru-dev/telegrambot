var intervalId_;

setInterval(function() {
		var startBotButtonElement = document.querySelector('.start-bot-button-control');
		if (startBotButtonElement == null) {
			var request = new XMLHttpRequest();
			sendRequestToServer(
				request,
				'get_bot_logs/',
				'',
				function() {
					if (request.status == 200) {
						var botLogTableElement = document.querySelector('.bot-logs-table');
						botLogTableElement.innerHTML = request.responseText;
					}
				}
			);
		}
	}, 1000)

function checkBotCommandElements() {
	var botCommandElements = document.querySelectorAll('.bot-command');
	if (botCommandElements.length >= 2) {
		const screenWidth = window.screen.width;
		if (screenWidth >= 320 && screenWidth < 1800) {
			botCommandElements[botCommandElements.length - 1].setAttribute('id', 'last');
		} else {
			if (botCommandElements.length >= 3) {
				botCommandElements[botCommandElements.length - 1].setAttribute('id', 'last');
			}
		}
	}
}
checkBotCommandElements();

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
	const messageElementHeight = document.querySelector('.message-container').clientHeight;

	if (screenWidth >= 320 && screenWidth < 1000) {
		otherContainerElement.style = 'top: ' + (563 + messageElementHeight) + 'px;';
	}
	if (screenWidth >= 1000 && screenWidth < 1799) {
		otherContainerElement.style = 'top: ' + (555 + messageElementHeight) + 'px;';
	}
	if (screenWidth >= 1800) {
		otherContainerElement.style = 'top: ' + (124 + messageElementHeight) + 'px;';
	}
}

function hideMessageOther() {
	hideMessage();

	clearInterval(intervalId_);
	intervalId_ = setInterval(function() {
		const screenWidth = window.screen.width;
		var otherContainerElement = document.querySelector('.container#other');

		if (screenWidth >= 320 && screenWidth < 1000) {
			otherContainerElement.style = 'top: 563px;';
		}
		if (screenWidth >= 1000 && screenWidth < 1799) {
			otherContainerElement.style = 'top: 555px;';
		}
		if (screenWidth >= 1800) {
			otherContainerElement.style = 'top: 124px;';
		}
	}, 1000);
}

function startBotButtonClick() {
	var request = new XMLHttpRequest();
	sendRequestToServer(
		request,
		'start_bot/',
		'',
		function() {
			if (request.status == 200) {
				showSuccessMessage(request.responseText);
				checkUserWindowScreenForOtherContainer();
				hideMessageOther();

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
				showSuccessMessage(request.responseText);
				checkUserWindowScreenForOtherContainer();
				hideMessageOther();

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
	const botName = document.querySelector('.bot-name-input-control').value;
	const botToken = document.querySelector('.bot-token-input-control').value;

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
				showSuccessMessage(request.responseText);
				checkUserWindowScreenForOtherContainer();
				hideMessageOther();
			} else {
				showErrorMessage(request.responseText);
				checkUserWindowScreenForOtherContainer();
			}
		}
	);
}

function clearBotLogsButtonClick() {
	var request = new XMLHttpRequest();
	sendRequestToServer(
		request,
		'clear_bot_logs/',
		'',
		function() {
			if (request.status == 200) {
				showSuccessMessage(request.responseText);
				checkUserWindowScreenForOtherContainer();
				hideMessageOther();

				var botLogTableElement = document.querySelector('.bot-logs-table');
				botLogTableElement.innerHTML = '';
			}
		}
	);
}

function deleteBotCommandButtonClick(bot_id) {
	var request = new XMLHttpRequest();
	sendRequestToServer(
		request,
		bot_id + '/delete_bot_command/',
		'',
		function() {
			if (request.status == 200) {
				showSuccessMessage(request.responseText);
				checkUserWindowScreenForOtherContainer();
				hideMessageOther();

				var botCommandElement = document.querySelector('.bot-command.id-' + bot_id);
				botCommandElement.remove();

				checkBotCommandElements();
			} else {
				showErrorMessage(request.responseText);
				checkUserWindowScreenForOtherContainer();
			}
		}
	);
}

function addBotCommandButtonClick(link) {
	var request = new XMLHttpRequest();
	sendRequestToServer(
		request,
		link,
		'',
		function() {
			if (request.status == 200) {
				window.location.href = link;
			} else {
				showErrorMessage(request.responseText);
				checkUserWindowScreenForOtherContainer();
			}
		}
	);
}
function checkBotElements() {
	var botElements = document.querySelectorAll('.bot');
	if (botElements.length >= 2) {
		const screenWidth = window.screen.width;
		if (screenWidth >= 320 && screenWidth < 768) {
			if (botElements.length >= 2) {
				botElements[botElements.length - 1].setAttribute('id', 'last');
			}
		} else {
			if (botElements.length >= 5) {
				botElements[botElements.length - 1].setAttribute('id', 'last');
			}
		}
	}
}
checkBotElements();

function deleteBotButtonClick(botId, botName, nickname) {
	const deleteBotAnswer = confirm('Вы точно хотите удалить бота "' + botName + '"?');
	if (deleteBotAnswer == true) {
		var request = new XMLHttpRequest();
		sendRequestToServer(
			request,
			'/constructor/' + nickname + '/delete_bot/',
			JSON.stringify(
				{
					'bot_id': botId
				}
			),
			function() {
				if (request.status == 200) {
					showSuccessMessage(request.responseText);
					if (mainConstructorPage == false) {
						checkUserWindowScreenForOtherContainer();
						hideMessageOther();
					} else {
						hideMessage();
					}

					var botElement = document.querySelector('.bot.id-' + botId);
					botElement.remove();

					checkBotElements();
				} else {
					showErrorMessage(request.responseText);
				}
			}
		);
	}
}

function addBotButtonClick(link) {
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
			}
		}
	);
}
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
					hideMessage();

					var botElement = document.querySelector('.bot.id-' + botId);
					botElement.remove();
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
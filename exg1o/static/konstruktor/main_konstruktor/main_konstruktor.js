var intervalId;

function deleteBotButtonClick(botId, botName, nickname) {
	var deleteBotAnswer = confirm('Вы точно хотите удалить бота "' + botName + '"?');
	if (deleteBotAnswer == true) {
		var request = new XMLHttpRequest();
		sendRequestToServer(
			request,
			'/konstruktor/' + nickname + '/delete_bot/',
			JSON.stringify(
				{
					'bot_id': botId
				}
			),
			function() {
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
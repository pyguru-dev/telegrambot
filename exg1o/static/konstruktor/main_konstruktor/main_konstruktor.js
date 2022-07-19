function deleteBotButtonClick(botId, botName, nickname) {
	var deleteBotAnswer = confirm('Вы точно хотите удалить бота "' + botName + '"?');
	if (deleteBotAnswer == true) {
		var request = new XMLHttpRequest();
		sendRequestToServer(
			request,
			'/account/konstruktor/' + nickname + '/delete_bot/',
			JSON.stringify(
				{
					'bot_id': botId
				}
			),
			function() {
				setInterval("window.location.href = '';", 1000)
				if (request.status == 200) {
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
			setInterval("window.location.href = '';", 1000)
			if (request.status == 200) {
				window.location.href = link;
			} else {
				showErrorMessage(request.responseText);
			}
		}
	);
}
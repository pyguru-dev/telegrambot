function editDivsForMessageElement() {
	var containerDiv = document.getElementById('mainContainer');
	var addBotButtonElement = document.getElementById('addBotButton');

	containerDiv.style = 'height: 445px;';
	addBotButtonElement.style = "top: 283px;";
}

function deleteBotButtonClick(botId, botName, nickname) {
	var deleteBotAnswer = confirm('Вы точно хотите удалить бота "' + botName + '"?');
	if (deleteBotAnswer == true) {
		var request = new XMLHttpRequest();
			request.open('POST', '/account/konstruktor/' + nickname + '/delete_bot/', true);
			request.setRequestHeader('Content-Type', 'application/json');
			var data = JSON.stringify(
				{
					'bot_id': botId
				}
			);
			request.onreadystatechange = function() {
				setInterval("window.location.href = '';", 1500)
				if (request.status == 200) {
					showSuccessMessage(request.responseText)
				} else {
					showErrorMessage(request.responseText);
				}
			}
			request.send(data);
	}
}
function editDivsForMessageElement() {
	var containerDiv = document.getElementById('mainContainer');
	var addBotButtonElement = document.getElementById('addBotButton');

	containerDiv.style = 'height: 445px;';
	addBotButtonElement.style = "top: 283px;";
}

function showSuccessMessage(successMessage) {
	var messageElement = document.getElementById('message');

	editDivsForMessageElement();
	messageElement.style = 'color: #27c54a;';
	messageElement.innerHTML = successMessage;
}

function showErrorMessage(errorMessage) {
	var messageElement = document.getElementById('message');

	editDivsForMessageElement();
	messageElement.style = 'color: #ff006a;';
	messageElement.innerHTML = errorMessage;
}

function deleteBotButtonClick(botName, nickname) {
	var deleteBotAnswer = confirm('Вы точно хотите удалить бота "' + botName + '"?');
	if (deleteBotAnswer == true) {
		var request = new XMLHttpRequest();
			request.open('POST', '/account/konstruktor/' + nickname + '/delete_bot/', true);
			request.setRequestHeader('Content-Type', 'application/json');
			var data = JSON.stringify(
				{
					'bot_name': botName
				}
			);
			request.onreadystatechange = function() {
				if (request.status == 200) {
					setInterval("window.location.href = '';", 1500)
					showSuccessMessage('Вы успешно удалили бота.')
				} else {
					setInterval("window.location.href = '';", 1500)
					showErrorMessage(request.responseText);
				}
			}
			request.send(data);
	}
}
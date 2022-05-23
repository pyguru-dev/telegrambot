function hideOrShowButtonClick() {
	var inputPasswordElement = document.getElementById('inputBotToken');

	if (inputPasswordElement.getAttribute('type') == 'password') {
		inputPasswordElement.setAttribute('type', 'text');

		var buttonElement = document.getElementById('hidePassword');
		buttonElement.setAttribute('id', 'showPassword');
	} else {
		inputPasswordElement.setAttribute('type', 'password');

		var buttonElement = document.getElementById('showPassword');
		buttonElement.setAttribute('id', 'hidePassword');
	}
}

function showErrorMessage(errorMessage) {
	var errorMessageElememt = document.getElementById('errorMessage');
	var containerDiv = document.getElementById('container');
	var buttonsDiv = document.getElementById('buttons');

	containerDiv.style = 'height: 280px;';
	buttonsDiv.style = "top: 200px;";
	errorMessageElememt.innerHTML = errorMessage;
}

function addBotButtonClick() {
	var bot_name = document.querySelector('.bot-name-input-control').value;
	var bot_token = document.querySelector('.bot-token-input-control').value;

	if (bot_name && bot_token != '') {
		if (bot_name.length <= 22) {
			var request = new XMLHttpRequest();
			request.open('POST', '../add_bot_/', true);
			request.setRequestHeader('Content-Type', 'application/json');
			var data = JSON.stringify(
				{
					'bot_name': bot_name,
					'bot_token': bot_token
				}
			);
			request.onreadystatechange = function() {
				if (request.status == 200) {
					window.location.href = '../';
				} else {
					showErrorMessage(request.responseText);
				}
			}
			request.send(data);
		}
	} else {
		showErrorMessage('Заполните форму добавление бота!')
	}
}
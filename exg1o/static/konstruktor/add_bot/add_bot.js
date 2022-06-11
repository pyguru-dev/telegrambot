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

function addBotButtonClick() {
	var botName = document.querySelector('.bot-name-input-control').value;
	var botToken = document.querySelector('.bot-token-input-control').value;

	if (botName && botToken != '') {
		if (botName.length <= 255) {
			var request = new XMLHttpRequest();
			request.open('POST', '../add_bot_/', true);
			request.setRequestHeader('Content-Type', 'application/json');
			var data = JSON.stringify(
				{
					'bot_name': botName,
					'bot_token': botToken
				}
			);
			request.onreadystatechange = function() {
				if (request.status == 200) {
					setInterval("window.location.href = '../';", 1200)
					showSuccessMessage(request.responseText);
				} else {
					showErrorMessage(request.responseText);
				}
			}
			request.send(data);
		} else {
			showErrorMessage('Имя бота должно содержать не более 255 символов!')
		}
	} else {
		showErrorMessage('Заполните форму добавление бота!')
	}
}
const inputElements = [
	document.querySelector('.bot-name-input-control'),
	document.querySelector('.bot-token-input-control')
]

for (let i = 0; i <= inputElements.length; i++) {
	inputElements[i].addEventListener('keyup', function(event) {
		if (event.keyCode == 13) {
			document.querySelector('.add-bot-button-control').click();
		}
	})
}

function hideOrShowButtonClick() {
	var inputPasswordElement = document.querySelector('.bot-token-input-control');

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
	const botName = document.querySelector('.bot-name-input-control').value;
	const botToken = document.querySelector('.bot-token-input-control').value;

	if (botName && botToken != '') {
		if (botName.length <= 255) {
			var request = new XMLHttpRequest();
			sendRequestToServer(
				request,
				'../add_bot_/',
				JSON.stringify(
					{
						'bot_name': botName,
						'bot_token': botToken
					}
				),
				function() {
					if (request.status == 200) {
						showSuccessMessage(request.responseText);
						setInterval("window.location.href = '../';", 1000);
					} else {
						showErrorMessage(request.responseText);
					}
				}
			);
		} else {
			showErrorMessage('Имя бота должно содержать не более 255 символов!');
		}
	} else {
		showErrorMessage('Заполните форму добавление бота!');
	}
}
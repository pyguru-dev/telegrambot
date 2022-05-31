function hideOrShowButtonClick() {
	var inputPasswordElement = document.getElementById('inputBotToken');

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
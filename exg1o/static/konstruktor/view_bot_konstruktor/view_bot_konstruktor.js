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

function startBotButtonClick() {
	var request = new XMLHttpRequest();
	request.open("POST", 'start_bot/', true);
	request.setRequestHeader("Content-Type", "application/json");
	request.onreadystatechange = function() {
		if (request.status == 200) {
			console.log('OK!')
		}
	}
	request.send();
}
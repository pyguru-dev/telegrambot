var intervalId;

function checkUserWindowScreen() {
	const screenWidth = window.screen.width;
	var containerElement = document.querySelector('.container');
	var messageElementHeight = document.querySelector('.message-container').clientHeight;

	if (screenWidth >= 320 && screenWidth < 768) {
		if (userAuth) {
			containerElement.style = 'top: ' + (235 + messageElementHeight) + 'px;';
		} else {
			containerElement.style = 'top: ' + (185 + messageElementHeight) + 'px;';
		}
	}
	if (screenWidth >= 768 && screenWidth < 1000) {
			containerElement.style = 'top: ' + (99 + messageElementHeight) + 'px;';
		}
	if (screenWidth >= 1000) {
		containerElement.style = 'top: ' + (124 + messageElementHeight) + 'px;';
	}
}

function showSuccessMessage(successMessage) {
	var messageContainerElement = document.querySelector('.message-container');
	var messageElement = document.querySelector('.message');

	messageContainerElement.style = 'background-color: #27C54A;';
	messageElement.innerHTML = successMessage;

	checkUserWindowScreen();
}

function showErrorMessage(errorMessage) {
	var messageContainerElement = document.querySelector('.message-container');
	var messageElement = document.querySelector('.message');

	messageContainerElement.style = 'background-color: #EF3A3F;';
	messageElement.innerHTML = errorMessage;

	checkUserWindowScreen();
}

function hideMessage() {
	clearInterval(intervalId);
	intervalId = setInterval(function() {
		const screenWidth = window.screen.width;
		var containerElement = document.querySelector('.container');

		if (screenWidth >= 320 && screenWidth < 768) {
			if (userAuth) {
				containerElement.style = 'top: 235px;';
			} else {
				containerElement.style = 'top: 185px;';
			}
		}
		if (screenWidth >= 768 && screenWidth < 1000) {
			containerElement.style = 'top: 99px;';
		}
		if (screenWidth >= 1000) {
			containerElement.style = 'top: 124px;';
		}

		var messageContainerElement = document.querySelector('.message-container');
		var messageElement = document.querySelector('.message');

		messageContainerElement.style = '';
		messageElement.innerHTML = '';
	}, 1000);
}
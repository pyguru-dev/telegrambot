function checkUserWindowScreen() {
	const screenWidth = window.screen.width;
	var containerElement = document.querySelector('.container');
	var messageElementHeight = document.querySelector('.message-container').clientHeight;

	if (userAuth) {
		if (screenWidth >= 320 && screenWidth < 768) {
			containerElement.style = 'top: ' + (249 + messageElementHeight) + 'px;';
		}
	} else {
		if (screenWidth >= 320 && screenWidth < 768) {
			containerElement.style = 'top: ' + (199 + messageElementHeight) + 'px;';
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

function showWarningMessage(warningMessage) {
	var messageContainerElement = document.querySelector('.message-container');
	var messageElement = document.querySelector('.message');

	messageContainerElement.style = 'background-color: #F0AE24;';
	messageElement.innerHTML = warningMessage;

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
	const screenWidth = window.screen.width;
	var containerElement = document.querySelector('.container');

	if (screenWidth >= 320 && screenWidth < 768) {
		containerElement.style = 'top: 249px;';
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
}
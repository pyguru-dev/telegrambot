function showSuccessMessage(successMessage) {
	var messageContainerElement = document.getElementById('messageContainer');
	var messageElement = document.getElementById('message');

	messageContainerElement.style = 'background-color: #27C54A;';
	messageElement.innerHTML = successMessage;
}

function showWarningMessage(warningMessage) {
	var messageContainerElement = document.getElementById('messageContainer');
	var messageElement = document.getElementById('message');

	messageContainerElement.style = 'background-color: #F0AE24;';
	messageElement.innerHTML = warningMessage;
}

function showErrorMessage(errorMessage) {
	var messageContainerElement = document.getElementById('messageContainer');
	var messageElement = document.getElementById('message');

	messageContainerElement.style = 'background-color: #EF3A3F;';
	messageElement.innerHTML = errorMessage;
}
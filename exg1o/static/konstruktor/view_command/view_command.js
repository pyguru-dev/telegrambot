function editDivsForMessageElement() {
	var containerDiv = document.getElementById('mainContainer');
	var buttonsDiv = document.getElementById('buttons');

	containerDiv.style = 'height: 506px;';
	buttonsDiv.style = "top: 354px;";
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
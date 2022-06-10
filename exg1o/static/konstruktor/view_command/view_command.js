function editDivsForMessageElement() {
	var containerDiv = document.getElementById('container');
	var buttonsDiv = document.getElementById('buttons');

	containerDiv.style = 'height: 574px;';
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

function saveOrDeleteCommandRequest(request_type) {
	var commandName = document.querySelector('.command-name-input-control').value;
	var command = document.querySelector('.command-input-control').value;
	var commandAnswer = document.querySelector('.command-answer-input-control').value;

	if (commandName && command && commandAnswer != '') {
		if (commandName.length <= 29) {
			var request = new XMLHttpRequest();
			if (request_type == 'save_command') {
				request.open('POST', 'save_command/', true);
			} else {
				request.open('POST', 'delete_command/', true);
			}
			request.setRequestHeader('Content-Type', 'application/json');
			var data = JSON.stringify(
				{
					'command_name': commandName,
					'command': command,
					'command_answer': commandAnswer
				}
			);
			request.onreadystatechange = function() {
				if (request.status == 200) {
					setInterval("window.location.href = '../../';", 1500)
					if (request_type == 'save_command') {
						showSuccessMessage('Вы успешно сохранили команду.')
					} else {
						showSuccessMessage('Вы успешно удалили команду.')
					}
				} else {
					showErrorMessage(request.responseText);
				}
			}
			request.send(data);
		} else {
			showErrorMessage('Имя команды должно содержать не более 29 символов!')
		}
	} else {
		showErrorMessage('Заполните форму добавление команды!')
	}
}

function saveCommandButtonClick() {
	saveOrDeleteCommandRequest('save_command');
}

function deleteCommandButtonClick() {
	saveOrDeleteCommandRequest('delete_command');
}
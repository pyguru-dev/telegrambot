function showErrorMessage(errorMessage) {
	var errorMessageElement = document.getElementById('errorMessage');
	var containerDiv = document.getElementById('container');
	var buttonsDiv = document.getElementById('buttons');

	containerDiv.style = 'height: 506px;';
	buttonsDiv.style = "top: 354px;";
	errorMessageElement.innerHTML = errorMessage;
}

function addCommandButtonClick() {
	var commandName = document.querySelector('.command-name-input-control').value;
	var command = document.querySelector('.command-input-control').value;
	var commandAnswer = document.querySelector('.command-answer-input-control').value;

	if (commandName && command && commandAnswer != '') {
		if (commandName.length <= 29) {
			var request = new XMLHttpRequest();
			request.open('POST', '../add_command_/', true);
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
					window.location.href = '../';
				} else {
					showErrorMessage(request.responseText);
				}
			}
			request.send(data);
		} else {
			showErrorMessage('Имя команды должно содержать не более 256 символов!')
		}
	} else {
		showErrorMessage('Заполните форму добавление команды!')
	}
}
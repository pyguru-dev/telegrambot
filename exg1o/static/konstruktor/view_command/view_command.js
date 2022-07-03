function saveOrDeleteCommandRequest(request_type) {
	var command = document.querySelector('.command-input-control').value;
	var commandAnswer = document.querySelector('.command-answer-input-control').value;

	if (command && commandAnswer != '') {
		if (command.length <= 255) {
			var request = new XMLHttpRequest();
			if (request_type == 'save_command') {
				request.open('POST', 'save_command/', true);
			} else {
				request.open('POST', 'delete_command/', true);
			}
			request.setRequestHeader('Content-Type', 'application/json');
			var data = JSON.stringify(
				{
					'command': command,
					'command_answer': commandAnswer
				}
			);
			request.onreadystatechange = function() {
				if (request.status == 200) {
					setInterval("window.location.href = '../../';", 1000)
					showSuccessMessage(request.responseText)
				} else {
					showErrorMessage(request.responseText);
				}
			}
			request.send(data);
		} else {
			showErrorMessage('Команда должна содержать не более 255 символов!')
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
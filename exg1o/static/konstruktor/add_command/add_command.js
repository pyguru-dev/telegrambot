const inputElements = [
	document.querySelector('.command-input-control')
]

function addCommandButtonClick() {
	var command = document.querySelector('.command-input-control').value;
	var commandAnswer = document.querySelector('.command-answer-input-control').value;

	if (command && commandAnswer != '') {
		if (command.length <= 255) {
			var request = new XMLHttpRequest();
			sendRequestToServer(
				request,
				'../add_command_/',
				JSON.stringify(
					{
						'command': command,
						'command_answer': commandAnswer
					}
				),
				function() {
					if (request.status == 200) {
						setInterval("window.location.href = '../';", 1000);
						showSuccessMessage(request.responseText);
					} else {
						showErrorMessage(request.responseText);
					}
				}
			);
		} else {
			showErrorMessage('Команда должна содержать не более 255 символов!');
		}
	} else {
		showErrorMessage('Заполните форму добавление команды!');
	}
}
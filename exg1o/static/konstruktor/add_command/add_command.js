function showErrorMessage(errorMessage) {
	var errorMessageElement = document.getElementById('errorMessage');
	var containerDiv = document.getElementById('container');
	var buttonsDiv = document.getElementById('buttons');

	containerDiv.style = 'height: 310px;';
	buttonsDiv.style = "top: 158px;";
	errorMessageElement.innerHTML = errorMessage;
}

function addCommandButtonClick() {
	var commandName = document.querySelector('.command-name-input-control').value;

	if (commandName != '') {
		if (commandName.length <= 11) {
			var request = new XMLHttpRequest();
			request.open('POST', '../add_command_/', true);
			request.setRequestHeader('Content-Type', 'application/json');
			var data = JSON.stringify(
				{
					'command_name': commandName
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
			showErrorMessage('Имя команды должно содержать не менее (хуй знает) символов!')
		}
	} else {
		showErrorMessage('Заполните форму добавление команды!')
	}
}
function hideOrShowButtonClick() {
	var inputPasswordElement = document.getElementById('inputPassword');

	if (inputPasswordElement.getAttribute('type') == 'password') {
		inputPasswordElement.setAttribute('type', 'text');

		var buttonElement = document.getElementById('hidePassword');
		buttonElement.setAttribute('id', 'showPassword');
	} else {
		inputPasswordElement.setAttribute('type', 'password');

		var buttonElement = document.getElementById('showPassword');
		buttonElement.setAttribute('id', 'hidePassword');
	}
}

function showErrorMessage(errorMessage) {
	var errorMessageElement = document.getElementById('errorMessage')
	var containerDiv = document.getElementById('container');
	var buttonsDiv = document.getElementById('buttons');

	if (screen.width < 786) {
		containerDiv.style = 'height: 259px;';
		buttonsDiv.style = 'top: 168px;';
	}
	if (screen.width >= 768 && screen.width < 1000) {
		containerDiv.style = 'height: 294px;';
		buttonsDiv.style = 'top: 220px;';
	}
	if (screen.width > 1000) {
		containerDiv.style = 'height: 345px;';
		buttonsDiv.style = 'top: 261px;';
	}
	errorMessageElement.innerHTML = errorMessage;
}

function authorizationButtonClick() {
	var login = document.querySelector('.login-input-control').value;
	var password = document.querySelector('.password-input-control').value;

	if (login | password != '') {
		if (password.length > 8) {
			var request = new XMLHttpRequest();
			request.open("POST", 'authorize_in_account/', true);
			request.setRequestHeader("Content-Type", "application/json");
			var data = JSON.stringify(
				{
					"login": login,
					"password": password
				}
			);
			request.onreadystatechange = function() {
				if (request.status == 200) {
					window.location.href = '/account/view/' + login + '/';
				} else {
					showErrorMessage(request.responseText);
				}
			}
			request.send(data);
		} else {
			showErrorMessage('Пароль должен содержать не менее 8 символов!');
		}
	} else {
		showErrorMessage('Заполните форму авторизации!');
	}
}
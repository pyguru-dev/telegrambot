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
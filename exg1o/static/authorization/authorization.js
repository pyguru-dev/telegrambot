const inputElements = [
	document.querySelector('.login-input-control'),
	document.querySelector('.password-input-control')
]

for (let i = 0; i <= inputElements.length; i++) {
	inputElements[i].addEventListener('keyup', function(event) {
		if (event.keyCode == 13) {
			document.querySelector('.authorization-button-control').click();
		}
	})
}

function hideOrShowButtonClick() {
	var inputPasswordElement = document.querySelector('.password-input-control');

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
		if (password.length >= 8) {
			if (password.length <= 255) {
				var request = new XMLHttpRequest();
				sendRequestToServer(
					request,
					'authorize_in_account/',
					JSON.stringify(
						{
							"login": login,
							"password": password
						}
					),
					function() {
						if (request.status == 200) {
							setInterval("window.location.href = '/account/view/" + login + "/';", 1000)
							showSuccessMessage(request.responseText);
						} else {
							showErrorMessage(request.responseText);
						}
					}
				)
			} else {
				showErrorMessage('Пароль должен содержать не более 255 символов!');
			}
		} else {
			showErrorMessage('Пароль должен содержать не менее 8 символов!');
		}
	} else {
		showErrorMessage('Заполните форму авторизации!');
	}
}
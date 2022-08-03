const inputElements = [
	document.querySelector('.login-input-control'),
	document.querySelector('.email-input-control'),
	document.querySelector('.password-input-control'),
	document.querySelector('.again-password-input-control')
]

for (let i = 0; i <= inputElements.length; i++) {
	inputElements[i].addEventListener('keyup', function(event) {
		if (event.keyCode == 13) {
			document.querySelector('.registration-button-control').click();
		}
	})
}

function hideOrShowButtonClick(elemet) {
	var inputPasswordElement = document.querySelector(elemet);

	if (inputPasswordElement.getAttribute('type') == 'password') {
		inputPasswordElement.setAttribute('type', 'text');

		if (elemet == '.password-input-control') {
			var buttonElement = document.getElementById('hidePassword');
			buttonElement.setAttribute('id', 'showPassword');
		} else {
			var buttonElement = document.getElementById('hideAgainPassword');
			buttonElement.setAttribute('id', 'showAgainPassword');
		}
	} else {
		inputPasswordElement.setAttribute('type', 'password');

		if (elemet == '.password-input-control') {
			var buttonElement = document.getElementById('showPassword');
			buttonElement.setAttribute('id', 'hidePassword');
		} else {
			var buttonElement = document.getElementById('showAgainPassword');
			buttonElement.setAttribute('id', 'hideAgainPassword');
		}
	}
}

function registrationButtonClick() {
	const login = document.querySelector('.login-input-control').value;
	const email = document.querySelector('.email-input-control').value;
	const password_1 = document.querySelector('.password-input-control').value;
	const password_2 = document.querySelector('.again-password-input-control').value;

	if (login && email && password_1 && password_2 != '') {
		if (password_1 == password_2) {
			if (password_1.length >= 8) {
				if (password_1.length <= 255) {
					var request = new XMLHttpRequest();
					sendRequestToServer(
						request,
						'register_account/',
							JSON.stringify(
							{
								'login': login,
								'email': email,
								'password': password_1
							}
						),
						function() {
							if (request.status == 200) {
								setInterval("window.location.href = '/authorization';", 1000);
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
			showErrorMessage('Пароли не совпадают!');
		}
	} else {
		showErrorMessage('Заполните форму регистрации!');
	}
}
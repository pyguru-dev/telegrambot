function hideOrShowButtonClick(elemet) {
	var inputPasswordElement = document.getElementById(elemet);

	if (inputPasswordElement.getAttribute('type') == 'password') {
		inputPasswordElement.setAttribute('type', 'text');

		if (elemet == 'inputPassword') {
			var buttonElement = document.getElementById('hidePassword');
			buttonElement.setAttribute('id', 'showPassword');
		} else {
			var buttonElement = document.getElementById('hideAgainPassword');
			buttonElement.setAttribute('id', 'showAgainPassword');
		}
	} else {
		inputPasswordElement.setAttribute('type', 'password');

		if (elemet == 'inputPassword') {
			var buttonElement = document.getElementById('showPassword');
			buttonElement.setAttribute('id', 'hidePassword');
		} else {
			var buttonElement = document.getElementById('showAgainPassword');
			buttonElement.setAttribute('id', 'hideAgainPassword');
		}
	}
}

function showErrorMessage(errorMessage) {
	var errorMessageElement = document.getElementById('errorMessage');
	var containerDiv = document.getElementById('container');
	var buttonsDiv = document.getElementById('buttons');

	if (screen.width < 786) {
		containerDiv.style = 'height: 351px;';
		buttonsDiv.style = 'top: 260px;';
	}
	if (screen.width >= 768 && screen.width < 1000) {
		containerDiv.style = 'height: 399px;';
		buttonsDiv.style = 'top: 325px;';
	}
	if (screen.width > 1000) {
		containerDiv.style = 'height: 451px;';
		buttonsDiv.style = 'top: 367px;';
	}
	errorMessageElement.innerHTML = errorMessage;
}

function registrationButtonClick() {
	var login = document.querySelector('.login-input-control').value;
	var email = document.querySelector('.email-input-control').value;
	var password_1 = document.querySelector('.password-input-control').value;
	var password_2 = document.querySelector('.again-password-input-control').value;

	if (login && email && password_1 && password_2 != '') {
		if (password_1 == password_2) {
			if (password_1.length >= 8 && password_1.length <= 128) {
				var request = new XMLHttpRequest();
				request.open('POST', 'register_account/', true);
				request.setRequestHeader('Content-Type', 'application/json');
				var data = JSON.stringify(
					{
						'login': login,
						'email': email,
						'password': password_1
					}
				);
				request.onreadystatechange = function() {
					if (request.status == 200) {
						window.location.href = '../authorization';
					} else {
						showErrorMessage(request.responseText);
					}
				}
				request.send(data);
			} else {
				showErrorMessage('Пароль должен содержать не менее 8 до 128 символов!');
			}
		} else {
			showErrorMessage('Пароли не совпадают!');
		}
	} else {
		showErrorMessage('Заполните форму регистрации!');
	}
}
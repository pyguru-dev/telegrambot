function hideOrShowButtonClick(elemet) {
	var inputPasswordElement = document.getElementById(elemet);

	if (inputPasswordElement.getAttribute('type') == 'password') {
		inputPasswordElement.setAttribute('type', 'text');

		if (elemet == 'inputPassword') {
			var buttonElement = document.getElementById('hidePassword');
			buttonElement.setAttribute('id', 'showPassword')
		} else {
			var buttonElement = document.getElementById('hideAgainPassword');
			buttonElement.setAttribute('id', 'showAgainPassword')		
		}
		buttonElement.setAttribute('class', 'show-password-button-control')
	} else {
		inputPasswordElement.setAttribute('type', 'password');

		if (elemet == 'inputPassword') {
			var buttonElement = document.getElementById('showPassword');
			buttonElement.setAttribute('id', 'hidePassword')	
		} else {
			var buttonElement = document.getElementById('showAgainPassword');
			buttonElement.setAttribute('id', 'hideAgainPassword')	
		}
		buttonElement.setAttribute('class', 'hide-password-button-control')
	}
}


function showErrorMessage(errorMessage) {
	var errorMessageElememt = document.getElementById('errorMessage')
	var buttonsDiv = document.getElementById('buttons')

	buttonsDiv.style = "top: 370px;";
	errorMessageElememt.innerHTML = errorMessage;
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
function hideOrShowButtonClick() {
	var inputPasswordElement = document.getElementById('inputPassword');

	if (inputPasswordElement.getAttribute('type') == 'password') {
		inputPasswordElement.setAttribute('type', 'text');

		var buttonElement = document.getElementById('hidePassword');
		buttonElement.setAttribute('id', 'showPassword')
		buttonElement.setAttribute('class', 'show-password-button-control')
	} else {
		inputPasswordElement.setAttribute('type', 'password');

		var buttonElement = document.getElementById('showPassword');
		buttonElement.setAttribute('id', 'hidePassword')
		buttonElement.setAttribute('class', 'hide-password-button-control')
	}
}

function authorizationButtonClick() {
	var login = document.querySelector('.login-input-control').value;
	var password = document.querySelector('.password-input-control').value;
	if (login | password != '') {
		var request = new XMLHttpRequest();
		request.open("POST", 'authorize_in_account/', true);
		request.setRequestHeader("Content-Type", "application/json");
		var data = JSON.stringify({ "Login": login, "Password": password});
		request.send(data)
	} else {
		document.getElementById('errorMessage').innerHTML = 'Неверный "Login" или "Password"!';
	}
}
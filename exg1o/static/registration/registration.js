function registrationButtonClick() {
	var login = document.querySelector('.login-input-control').value;
	var email = document.querySelector('.email-input-control').value;
	var password_1 = document.querySelector('.password-input-control').value;
	var password_2 = document.querySelector('.again-password-input-control').value;
	if (login && email && password_1 && password_2 != '') {
		if (password_1 == password_2) {
			if (password_1.length >= 8) {
			var request = new XMLHttpRequest();
			request.open('POST', 'register_account/', true);
			request.setRequestHeader('Content-Type', 'application/json');
			var data = JSON.stringify(
				{
					'Login': login,
					'Email': email,
					'Password': password_1
				}
			);
			request.send(data);
			request.onreadystatechange = function() {
				if (request.readyState == 4 && request.status == 200) {
					window.location.href = '../authorization';
				} else {
					document.getElementById('errorMessage').innerHTML = request.responseText;
				}
			}
			} else {
				document.getElementById('errorMessage').innerHTML = 'Пароль должен содержать не менее 8 символов!';
			}
		} else {
			document.getElementById('errorMessage').innerHTML = 'Пароли не совпадают!';
		}
	} else {
		document.getElementById('errorMessage').innerHTML = 'Заполните форму регистрации!';
	}
}
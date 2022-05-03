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
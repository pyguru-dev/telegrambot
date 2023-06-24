document.querySelector('#loginButton').addEventListener('click', function() {
	fetch(loginUrl, {
		method: 'POST',
		body: JSON.stringify(
			{
				'username': document.querySelector('#loginUsernameInput').value,
				'password': document.querySelector('#loginPasswordInput').value,
			}
		),
		headers: {'Content-Type': 'application/json'},
	}).then(response => {
		response.json().then(jsonResponse => {
			if (response.ok) {
				setTimeout("window.location.href = '';", 1500);
			}

			createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
		});
	});
});

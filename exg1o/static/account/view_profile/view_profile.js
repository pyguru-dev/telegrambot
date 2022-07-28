var updateUserIconInputElement = document.querySelector('.update-user-icon-input-control');
updateUserIconInputElement.onchange = e => {
	file = e.target.files[0];

	if (file.type == 'image/png' || file.type == 'image/jpeg') {
		var request = new XMLHttpRequest();
		sendRequestToServer(
			request,
			'update_user_icon/',
			file,
			function() {
				if (request.status == 200) {
					setInterval("window.location.href = '';", 1000);
					showSuccessMessage(request.responseText);
				}
			}
		)
	} else {
		showErrorMessage('Вы выбрали не фото!');
	}
}
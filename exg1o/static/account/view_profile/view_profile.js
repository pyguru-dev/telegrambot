var updateUserIconInputElement = document.querySelector('.update-user-icon-input-control');
updateUserIconInputElement.onchange = e => {
	file = e.target.files[0];

	if (file.type == 'image/png' || file.type == 'image/jpeg') {
		if (file.size <= 1000000) {
		var request = new XMLHttpRequest();
			sendRequestToServer(
				request,
				'update_user_icon/',
				file,
				function() {
					if (request.status == 200) {
						showSuccessMessage(request.responseText);
						hideMessage();

						var userIconElement = document.querySelector('.user-icon');
						userIconElement.src = URL.createObjectURL(file);
					}
				}
			)
		} else {
			showErrorMessage('Картинка весит больше 1-ого мегабайта!');
		}
	} else {
		showErrorMessage('Вы выбрали не картинку!');
	}
}
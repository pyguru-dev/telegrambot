var updateUserIconInputElement = document.querySelector('.update-user-icon-input-control');
updateUserIconInputElement.onchange = e => {
	file = e.target.files[0];

	let reader = new FileReader();
	reader.readAsDataURL(file)
	reader.onload = function() {
		var request = new XMLHttpRequest();
		sendRequestToServer(
			request,
			'update_user_icon/',
			reader.result,
			function() {
				if (request.status == 200) {
					setInterval("window.location.href = '';", 1000)
					showSuccessMessage(request.responseText);
				} else {
					showErrorMessage(request.responseText);
				}
			}
		)
	}
}
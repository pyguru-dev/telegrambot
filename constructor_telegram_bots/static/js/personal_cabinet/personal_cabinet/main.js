{
	var mainAlertPlaceholder = document.querySelector('#mainAlertPlaceholder');

	document.querySelector('#addTelegramBotModalButton').addEventListener('click', function() {
		addTelegramBotModalAlertPlaceholder.innerHTML = '';
		addTelegramBotTokenInput.value = '';

		addTelegramBotModalBootstrap.toggle();
	});
}
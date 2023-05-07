{
	document.querySelector('#addTelegramBotModalButton').addEventListener('click', function() {
		addTelegramBotModalAlertPlaceholder.innerHTML = '';
		addTelegramBotApiTokenInput.value = '';

		addTelegramBotModalBootstrap.toggle();
	});
}
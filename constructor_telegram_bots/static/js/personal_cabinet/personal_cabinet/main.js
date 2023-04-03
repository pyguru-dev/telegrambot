{
	var addTelegramBotModalBootstrap = new bootstrap.Modal('#addTelegramBotModal');
	var addTelegramBotModalAlertPlaceholder = document.querySelector('#addTelegramBotModalAlertPlaceholder');
	let addTelegramBotTokenInput = document.querySelector('#addTelegramBotTokenInput');

	document.querySelector('#addTelegramBotModalButton').addEventListener('click', function() {
		addTelegramBotModalAlertPlaceholder.innerHTML = '';
		addTelegramBotTokenInput.value = '';

		addTelegramBotModalBootstrap.toggle();
	});
}
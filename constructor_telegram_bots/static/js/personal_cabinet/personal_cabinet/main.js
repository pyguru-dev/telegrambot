{
	var addTelegramBotModalBootstrap = new bootstrap.Modal('#addTelegramBotModal');
	let addTelegramBotTokenInput = document.querySelector('#addTelegramBotTokenInput');

	document.querySelector('#addTelegramBotModalButton').addEventListener('click', function() {
		addTelegramBotTokenInput.value = '';

		addTelegramBotModalBootstrap.toggle();
	});
}
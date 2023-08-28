{
	const loginViaTelegramModalDiv = document.querySelector('#loginViaTelegramModal');
	const loginViaTelegramBootstrapModal = new bootstrap.Modal(loginViaTelegramModalDiv);

	new QRCode(loginViaTelegramModalDiv.querySelector('.qrcode'), `tg://resolve?domain=${constructorTelegramBotUsername}&start=login`);
	document.querySelectorAll('.btn-login-via-telegram').forEach(button => button.addEventListener('click', () => loginViaTelegramBootstrapModal.toggle()));
}
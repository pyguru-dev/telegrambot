{
	const loginViaTelegramModalDiv = document.querySelector('#loginViaTelegramModal');
	const loginViaTelegramBootstrapModal = new bootstrap.Modal(loginViaTelegramModalDiv)
	const loginViaTelegramModalQrcodeDiv = loginViaTelegramModalDiv.querySelector('.qrcode');

	new QRCode(loginViaTelegramModalQrcodeDiv, `tg://resolve?domain=${constructorTelegramBotUsername}&start=login`);
	document.querySelectorAll('.btn-login-via-telegram').forEach(button => button.addEventListener('click', () => loginViaTelegramBootstrapModal.toggle()));
}
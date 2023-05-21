{
	document.querySelector('#logoutButton').addEventListener('click', () => askConfirmModal(
		'Выход из аккаунта',
		'Вы точно хотите выйти из аккаунта?',
		function() {
			window.location.href = userLogOutUrl;
		}
	));
}
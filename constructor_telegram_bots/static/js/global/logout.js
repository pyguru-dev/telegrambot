document.querySelector('#logoutButton').addEventListener('click', () => askConfirmModal(
	logoutAskConfirmModalTitle,
	logoutAskConfirmModalText,
	function() {window.location.href = userLogoutUrl}
));

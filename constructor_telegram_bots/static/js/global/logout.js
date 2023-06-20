document.querySelector('#userLogoutButton').addEventListener('click', () => askConfirmModal(
	userLogoutAskConfirmModalTitle,
	userLogoutAskConfirmModalText,
	function() {window.location.href = userLogoutUrl}
));

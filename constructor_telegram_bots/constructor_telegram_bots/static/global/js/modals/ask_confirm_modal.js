{
	const askConfirmBootstrapModal = new bootstrap.Modal('#askConfirmModal');
	const askConfirmModalTitle = document.querySelector('#askConfirmModalTitle');
	const askConfirmModalText = document.querySelector('#askConfirmModalText');
	const askConfirmModalYesButton = document.querySelector('#askConfirmModalYesButton');

	function askConfirmModal(title, text, func) {
		askConfirmModalTitle.innerHTML = title;
		askConfirmModalText.innerHTML = text;

		if (askConfirmModalYesButton.onclick) {
			askConfirmModalYesButton.removeEventListener('click', askConfirmModalYesButton.onclick);
		}

		askConfirmModalYesButton.onclick = function() {
			askConfirmBootstrapModal.toggle();
			func();
		}

		askConfirmBootstrapModal.toggle();
	}
}
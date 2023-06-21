{
	var askConfirmModalBootstrap = new bootstrap.Modal('#askConfirmModal');

	const askConfirmModalLabel = document.querySelector('#askConfirmModalLabel');
	const askConfirmText = document.querySelector('#askConfirmText');

	const askConfirmYesButton = document.querySelector('#askConfirmYesButton');

	function askConfirmModal(title, text, func) {
		askConfirmModalLabel.innerHTML = title;
		askConfirmText.innerHTML = text;

		askConfirmYesButton.addEventListener('click', function() {
			askConfirmModalBootstrap.toggle();
			
			func();
		});

		askConfirmModalBootstrap.toggle();
	}
}

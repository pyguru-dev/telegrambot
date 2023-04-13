{
	var askConfirmModalBootstrap = new bootstrap.Modal('#askConfirmModal');

	let askConfirmModalLabel = document.querySelector('#askConfirmModalLabel');
	let askConfirmText = document.querySelector('#askConfirmText');

	let askConfirmYesButton = document.querySelector('#askConfirmYesButton');

	function askConfirmModal(title, text, func) {
		askConfirmModalLabel.innerHTML = title;
		askConfirmText.innerHTML = text;

		askConfirmYesButton.onclick = function() {
			askConfirmModalBootstrap.toggle();

			func();
		}

		askConfirmModalBootstrap.toggle();
	}
}

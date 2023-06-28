{
	const askConfirm = {
		modal: new bootstrap.Modal('#askConfirmModal'),

		title: document.querySelector('#askConfirmModalLabel'),
		text: document.querySelector('#askConfirmText'),

		button: document.querySelector('#askConfirmYesButton'),
	}

	function askConfirmModal(title, text, func) {
		askConfirm.title.innerHTML = title;
		askConfirm.text.innerHTML = text;

		askConfirm.button.addEventListener('click', function() {
			askConfirm.modal.toggle();
			func();
		});

		askConfirm.modal.toggle();
	}
}

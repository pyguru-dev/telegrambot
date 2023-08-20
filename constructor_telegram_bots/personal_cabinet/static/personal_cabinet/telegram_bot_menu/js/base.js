document.querySelectorAll('.btn-update').forEach(updateButton => {
	updateButton.addEventListener('click', function() {
		if (updateButton.getAttribute('aria-updating') == 'false') {
			updateButton.setAttribute('aria-updating', 'true');
			setTimeout(() => updateButton.setAttribute('aria-updating', 'false'), 900);
		}
	})
});
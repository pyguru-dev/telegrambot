{
	const mainToastContainerDiv = document.querySelector('#mainToastContainer');
	const toastIcons = {
		'success': '<i class="bi bi-check-circle-fill me-2"></i>',
		'primary': '<i class="bi bi-info-circle-fill me-2"></i>',
		'danger': '<i class="bi bi-exclamation-triangle-fill me-2"></i>',
	}

	function createToast(message, type) {
		const toastDiv = document.createElement('div');
		toastDiv.className = `toast bg-light border fade`;
		toastDiv.role = 'alert';
		toastDiv.setAttribute('aria-live', 'assertive');
		toastDiv.setAttribute('aria-atomic', 'true');
		toastDiv.setAttribute('data-bs-autohide', 'true');
		toastDiv.setAttribute('data-bs-delay', '6000');
		toastDiv.innerHTML = [
			`<div class="toast-body text-${type}">`,
			'	<div class="d-flex align-items-center">',
					toastIcons[type],
			`		<strong class="text-break me-auto">${message}</strong>`,
			'		<button class="btn-close ms-2" type="button" data-bs-dismiss="toast" aria-label="Close"></button>',
			'	</div>',
			'</div>',
		].join('');
		mainToastContainerDiv.appendChild(toastDiv);

		const bootstrapToast = new bootstrap.Toast(toastDiv);
		bootstrapToast.show();
	}
}
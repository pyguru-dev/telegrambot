{
	const mainContainer = document.querySelector('main .container');
	const mainContainerClass = mainContainer.getAttribute('class');

	var mainAlertContainer = document.querySelector('#mainAlertContainer');

	const bootstrapBreakpoints = ['', 'sm-', 'md-', 'lg-', 'xl-', 'xxl-'];

	const alertIcons = {
		'primary': '<i class="bi bi-info-circle-fill me-2"></i>',
		'success': '<i class="bi bi-check-circle-fill me-2"></i>',
		'danger': '<i class="bi bi-exclamation-triangle-fill me-2"></i>',
		'warning': '<i class="bi bi-exclamation-triangle-fill me-2"></i>',
	}

	let alertId = 0;

	function createAlert(alertContainer, message, type) {
		const alertDiv = document.createElement('div');
		alertDiv.className = `alert alert-${type} d-flex align-items-center alert-dismissible fade `;
		alertDiv.id = alertId;
		alertDiv.role = 'alert';
		alertDiv.innerHTML = [
			alertIcons[type],
			`<p class="mb-0">${message}</p>`,
			'<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
		].join('');

		if (alertContainer == mainAlertContainer) {
			for (let bootstrapBreakpoint = 0; bootstrapBreakpoint < bootstrapBreakpoints.length; bootstrapBreakpoint++) {
				for (let size = 1; size <= 5; size++) {
					if (mainContainer.classList.contains(`my-${bootstrapBreakpoints[bootstrapBreakpoint]}${size}`)) {
						mainContainer.classList.remove(`my-${bootstrapBreakpoints[bootstrapBreakpoint]}${size}`);
						mainContainer.classList.add(`mb-${bootstrapBreakpoints[bootstrapBreakpoint]}${size}`);
					} else if (mainContainer.classList.contains(`mt-${bootstrapBreakpoints[bootstrapBreakpoint]}${size}`)) {
						mainContainer.classList.remove(`mt-${bootstrapBreakpoints[bootstrapBreakpoint]}${size}`);
					}
				}
			}

			alertDiv.className += 'my-2';
		} else {
			alertDiv.className += 'mb-2';
		}

		alertContainer.append(alertDiv);

		setTimeout((alertDiv) => {
			alertDiv.classList.add('show');
			
			setTimeout((alertDiv) => {
				alertDiv.classList.remove('show');
				
				setTimeout((alertDiv) => {
					alertDiv.remove();

					if (alertDiv.id == alertId - 1) {
						mainContainer.setAttribute('class', mainContainerClass);
					}
				}, 300, alertDiv);
			}, 5000, alertDiv);
		}, 250, alertDiv);

		alertId ++;
	}
}
{
	let mainContainer = document.querySelector('main .container');
	let mainContainerClass = mainContainer.getAttribute('class');

	var mainAlertContainer = document.querySelector('#mainAlertContainer');

	let breakpoints = ['', 'sm-', 'md-', 'lg-', 'xl-', 'xxl-']

	let alertId = 0;

	function removeAlert(alertDiv) {
		alertDiv.remove();

		if (alertDiv.id == alertId - 1) {
			mainContainer.setAttribute('class', mainContainerClass);
		}
	}

	function closeAlert(alertDiv) {
		alertDiv.classList.remove('show');

		setTimeout(removeAlert, 300, alertDiv)
	}

	function showAlert(alertDiv) {
		alertDiv.classList.add('show');

		setTimeout(closeAlert, 5000, alertDiv)
	}

	function createAlert(alertContainer, message, type) {
		let alertDiv = document.createElement('div');
		alertDiv.className = `alert alert-${type} fade `;
		alertDiv.id = alertId;
		alertDiv.role = 'alert';
		alertDiv.innerHTML = `<p class="text-center mb-0">${message}</p>`;

		if (alertContainer == mainAlertContainer) {
			for (let breakpoint = 0; breakpoint < breakpoints.length; breakpoint++) {
				for (let size = 1; size <= 5; size++) {
					if (mainContainer.classList.contains(`my-${breakpoints[breakpoint]}${size}`)) {
						mainContainer.classList.remove(`my-${breakpoints[breakpoint]}${size}`);
						mainContainer.classList.add(`mb-${breakpoints[breakpoint]}${size}`);
					} else if (mainContainer.classList.contains(`mt-${breakpoints[breakpoint]}${size}`)) {
						mainContainer.classList.remove(`mt-${breakpoints[breakpoint]}${size}`);
					}
				}
			}

			alertDiv.className += 'my-2';
		} else {
			alertDiv.className += 'mb-2';
		}

		alertContainer.append(alertDiv);

		setTimeout(showAlert, 200, alertDiv);

		alertId ++;
	}
}
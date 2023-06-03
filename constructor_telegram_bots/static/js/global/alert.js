{
	let mainContainer = document.querySelector('main .container');
	let mainContainerClass = mainContainer.getAttribute('class');

	var mainAlertPlaceholder = document.querySelector('#mainAlertPlaceholder');

	let breakpoints = ['', 'sm-', 'md-', 'lg-', 'xl-', 'xxl-']

	let myAlertId = 0;

	function myAlert(alertPlaceholder, message, type) {
		let wrapper = document.createElement('div');
		wrapper.className = `alert alert-${type} fade `;
		wrapper.id = myAlertId;
		wrapper.role = 'alert';
		wrapper.innerHTML = `<p class="text-center mb-0">${message}</p>`;

		if (alertPlaceholder == mainAlertPlaceholder) {
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

			wrapper.className += 'my-2';
		} else {
			wrapper.className += 'mb-2';
		}

		alertPlaceholder.append(wrapper);

		function showMyAlert(__myAlert) {
			__myAlert.classList.add('show');

			setTimeout(closeMyAlert, 5000, __myAlert)
		}

		function closeMyAlert(__myAlert) {
			__myAlert.classList.remove('show');

			function removeMyAlert(___myAlert) {
				___myAlert.remove();

				if (__myAlert.id == myAlertId - 1) {
					mainContainer.setAttribute('class', mainContainerClass);
				}
			}

			setTimeout(removeMyAlert, 300, __myAlert)
		}

		let _myAlert = document.querySelector(`.alert[id="${myAlertId}"]`);
		setTimeout(showMyAlert, 200, _myAlert);

		myAlertId ++;
	}
}
{
	let mainContainer = document.querySelector('main').querySelector('.container');
	let mainContainerClass= mainContainer.getAttribute('class');

	let alertId = 0;

	function myAlert(alertPlaceholder, message, type) {
		for (let a = 0; a <= 5; a++) {
			mainContainer.classList.remove(`mt-${a}`);
		}

		breakpoints = ['sm', 'md', 'lg', 'xl', 'xxl']

		for (let a = 0; a <= 5; a++) {
			for (let b = 0; b < breakpoints.length; b++) {
				mainContainer.classList.remove(`mt-${breakpoints[b]}-${a}`);
			}
		}
		
		let wrapper = document.createElement('div');
		wrapper.innerHTML = [
			`<div class="alert alert-${type} alert-dismissible fade p-3 my-2" id="${alertId}" role="alert">`,
			`   <p class="text-center mb-0">${message}</p>`,
			'</div>',
		].join('');
		alertPlaceholder.append(wrapper);

		function showMyAlert(__myAlert) {
			__myAlert.classList.add('show');

			setTimeout(closeMyAlert, 5000, __myAlert)
		}

		function closeMyAlert(__myAlert) {
			__myAlert.classList.remove('show');

			function removeMyAlert(___myAlert) {
				___myAlert.remove();

				if (__myAlert.id == alertId - 1) {
					mainContainer.setAttribute('class', mainContainerClass);
				}
			}

			setTimeout(removeMyAlert, 300, __myAlert)
		}

		let _myAlert = document.querySelector(`.alert[id="${alertId}"]`);
		setTimeout(showMyAlert, 200, _myAlert);

		alertId ++;
	}
}
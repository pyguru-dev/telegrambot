{
	let alertId = 0;

	function myAlert(alertPlaceholder, message, type) {
		let wrapper = document.createElement('div');
		wrapper.innerHTML = [
			`<div class="alert alert-${type} alert-dismissible fade mb-2" id="${alertId}" role="alert">`,
			`   <div class="text-center">${message}</div>`,
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
			}

			setTimeout(removeMyAlert, 300, __myAlert)
		}

		let _myAlert = document.querySelector(`.alert[id="${alertId}"]`);
		setTimeout(showMyAlert, 200, _myAlert);

		alertId ++;
	}
}
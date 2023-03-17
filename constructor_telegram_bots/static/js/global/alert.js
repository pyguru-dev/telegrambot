function myAlert(alertPlaceholder, message, type) {
	let wrapper = document.createElement('div');
	wrapper.innerHTML = [
		`<div class="alert alert-${type} alert-dismissible mb-2" role="alert">`,
		`   <div>${message}</div>`,
		'   <button class="btn-close" type="button" data-bs-dismiss="alert" aria-label="Close"></button>',
		'</div>',
	].join('');
	alertPlaceholder.append(wrapper);
}
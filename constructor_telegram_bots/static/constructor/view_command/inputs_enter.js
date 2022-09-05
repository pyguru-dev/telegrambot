for (let i = 0; i <= inputElements.length; i++) {
	inputElements[i].addEventListener('keyup', function(event) {
		if (event.keyCode == 13) {
			document.querySelector('.save-command-button-control').click();
		}
	})
}
for (let i = 0; i <= inputElements.length; i++) {
	inputElements[i].addEventListener('keyup', function(event) {
		if (event.keyCode == 13) {
			document.querySelector('.add-command-button-control').click();
		}
	})
}
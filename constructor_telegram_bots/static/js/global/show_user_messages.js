function showUserMessages() {
	fetch(getUserMessagesUrl, {
		method: 'POST'
	}).then(response => {
		if (response.ok) {
			response.json().then(messages => {
				messages.forEach(message => {
					createAlert(mainAlertContainer, message['text'], message['type']);
				});
			});
		}
	});
}

setInterval(showUserMessages, 2500);
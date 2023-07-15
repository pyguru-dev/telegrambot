var intervalUpdateUsersIsRunning = false;
var intervalUpdateUsersId;

{
	const telegramBotUsersCountDiv = document.querySelector('#telegramBotUsersCount');
	const telegramBotUsersDiv = document.querySelector('#telegramBotUsers');

	const checkTelegramBotUsersСount = () => {
		if (telegramBotUsersDiv.querySelectorAll('.telegram-bot-user').length == 0) {
			const telegramBotNotActivatedDiv = document.createElement('div');
			telegramBotNotActivatedDiv.setAttribute('class', 'list-group-item telegram-bot-not-activated px-3 py-2');
			telegramBotNotActivatedDiv.innerHTML = `<p class="text-center my-2">${telegramBotNotActivatedText}</p>`;
			telegramBotUsersDiv.append(telegramBotNotActivatedDiv);
		} else {
			const telegramBotNotActivatedDiv = telegramBotUsersDiv.querySelector('.telegram-bot-not-activated');

			if (telegramBotNotActivatedDiv != null) {
				telegramBotNotActivatedDiv.remove();
			}
		}
	}

	const addTelegramBotUser = (telegramBotUser) => {
		const telegramBotUserDiv = document.createElement('div');
		telegramBotUserDiv.classList = 'list-group-item telegram-bot-user p-3';
		telegramBotUserDiv.id = telegramBotUser['id'];
		telegramBotUserDiv.innerHTML = [
			'<div class="d-flex justify-content-between align-items-center">',
			`	[${telegramBotUser['date_activated']}]: ${telegramBotUser['user_id']} - ${telegramBotUser['full_name']}`,
			'	<div class="btn-group" role="group">',
			'		<button class="btn btn-warning add-allowed px-2 py-1 d-none">',
			'			<i class="bi bi-star d-flex justify-content-center text-light" style="font-size: 20px;"></i>',
			'		</button>',
			'		<button class="btn btn-warning delete-allowed px-2 py-1 d-none">',
			'			<i class="bi bi-star-fill d-flex justify-content-center text-light" style="font-size: 20px;"></i>',
			'		</button>',
			'		<button class="btn btn-danger delete px-2 py-1">',
			'			<i class="bi bi-trash d-flex justify-content-center" style="font-size: 20px;"></i>',
			'		</button>',
			'	</div>',
			'</div>',
		].join('');
		telegramBotUsersDiv.append(telegramBotUserDiv);

		const telegramBotUserAddAllowedButton = telegramBotUserDiv.querySelector('.add-allowed');
		const telegramBotUserDeleteAllowedButton = telegramBotUserDiv.querySelector('.delete-allowed');
		const telegramBotUserDeleteButton = telegramBotUserDiv.querySelector('.delete');

		if (telegramBotIsPrivateCheckBox.checked) {
			if (telegramBotUser['is_allowed']) {
				telegramBotUserDeleteAllowedButton.classList.add('rounded-start');
				telegramBotUserDeleteAllowedButton.classList.remove('d-none');
			} else {
				telegramBotUserAddAllowedButton.classList.remove('d-none');
			}
		} else {
			telegramBotUserDeleteButton.classList.add('rounded');
		}

		telegramBotUserAddAllowedButton.addEventListener('click', function() {
			fetch(`/telegram-bot/${telegramBotId}/user/${telegramBotUser['id']}/add-allowed-user/`, {
				method: 'POST',
				headers: {'Authorization': `Token ${userApiToken}`},
			}).then(response => {
				if (response.ok) {
					updateTelegramBotUsers();
				}

				response.json().then(jsonResponse => {
					createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
				});
			});
		});

		telegramBotUserDeleteAllowedButton.addEventListener('click', function() {
			fetch(`/telegram-bot/${telegramBotId}/user/${telegramBotUser['id']}/delete-allowed-user/`, {
				method: 'POST',
				headers: {'Authorization': `Token ${userApiToken}`},
			}).then(response => {
				if (response.ok) {
					updateTelegramBotUsers();
				}

				response.json().then(jsonResponse => {
					createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
				});
			});
		});

		telegramBotUserDeleteButton.addEventListener('click', () => askConfirmModal(
			deleteTelegramBotUserAskConfirmModalTitle,
			deleteTelegramBotUserAskConfirmModalText,
			function() {
				fetch(`/telegram-bot/${telegramBotId}/user/${telegramBotUser['id']}/delete/`, {
					method: 'POST',
					headers: {'Authorization': `Token ${userApiToken}`},
				}).then(response => {
					if (response.ok) {
						telegramBotUserDiv.remove();
						checkTelegramBotUsersСount();
					}

					response.json().then(jsonResponse => {
						createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
					});
				});
			}
		));
	}

	function updateTelegramBotUsers() {
		fetch(getTelegramBotUsersUrl, {
			method: 'POST',
			headers: {'Authorization': `Token ${userApiToken}`},
		}).then(response => {
			response.json().then(jsonResponse => {
				if (response.ok) {
					telegramBotUsersCountDiv.innerHTML = jsonResponse.length;
					telegramBotUsersDiv.innerHTML = '';

					jsonResponse.forEach(telegramBotUser => addTelegramBotUser(telegramBotUser))
					checkTelegramBotUsersСount();
				} else {
					createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
				}
			});
		});
	}

	updateTelegramBotUsers();
	if (telegramBotIsRunning && intervalUpdateUsersIsRunning == false) {
		intervalUpdateUsersIsRunning = true;
		intervalUpdateUsersId = setInterval(updateTelegramBotUsers, 3000);
	}
}
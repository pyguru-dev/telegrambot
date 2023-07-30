{
	const telegramBotUsersCountDiv = document.querySelector('#telegramBotUsersCount');
	const telegramBotUsersDiv = document.querySelector('#telegramBotUsers');

	const checkTelegramBotUsersСount = () => {
		if (telegramBotUsersDiv.querySelectorAll('.telegram-bot-user').length == 0) {
			const telegramBotNotActivatedDiv = document.createElement('div');
			telegramBotNotActivatedDiv.setAttribute('class', 'list-group-item telegram-bot-not-activated p-3');
			telegramBotNotActivatedDiv.innerHTML = `<p class="text-center m-0">${telegramBotNotActivatedText}</p>`;
			telegramBotUsersDiv.append(telegramBotNotActivatedDiv);
		} else {
			const telegramBotNotActivatedDiv = telegramBotUsersDiv.querySelector('.telegram-bot-not-activated');

			if (telegramBotNotActivatedDiv != null) {
				telegramBotNotActivatedDiv.remove();
			}
		}
	}

	function updateTelegramBotUsers() {
		fetch(telegramBotUsersUrl, {
			method: 'GET',
			headers: {'Authorization': `Token ${userApiToken}`},
		}).then(response => {
			response.json().then(jsonResponse => {
				if (response.ok) {
					telegramBotUsersCountDiv.innerHTML = jsonResponse.length;
					telegramBotUsersDiv.innerHTML = '';

					jsonResponse.forEach(telegramBotUser => {
						const telegramBotUserDiv = document.createElement('div');
						telegramBotUserDiv.classList = 'list-group-item telegram-bot-user p-3';
						telegramBotUserDiv.id = telegramBotUser['id'];
						telegramBotUserDiv.innerHTML = [
							'<div class="d-flex justify-content-between align-items-center">',
							`	<p class="m-0">[<span class="text-success-emphasis">${telegramBotUser['date_activated']}</span>]: <span class="text-primary">${telegramBotUser['user_id']}</span> - ${telegramBotUser['full_name']}</p>`,
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
							fetch(`/telegram-bots/${telegramBotId}/users/${telegramBotUser['id']}/allowed-user/`, {
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
							fetch(`/telegram-bots/${telegramBotId}/users/${telegramBotUser['id']}/allowed-user/`, {
								method: 'DELETE',
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
								fetch(`/telegram-bots/${telegramBotId}/users/${telegramBotUser['id']}/`, {
									method: 'DELETE',
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
					});

					checkTelegramBotUsersСount();
				} else {
					createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
				}
			});
		});
	}

	updateTelegramBotUsers();

	const telegramBotUsersСollapseButton = document.querySelector('#telegramBotUsersСollapseButton');
	const updateTelegramBotUsersButton = document.querySelector('#updateTelegramBotUsersButton');
	const telegramBotUsersBootstrapСollapse = new bootstrap.Collapse('#telegramBotUsersСollapse');

	telegramBotUsersСollapseButton.addEventListener('click', function() {
		updateTelegramBotUsersButton.classList.toggle('disabled');
		telegramBotUsersBootstrapСollapse.toggle();

		if (telegramBotUsersСollapseButton.querySelector('i').classList.contains('bi-arrow-up')) {
			telegramBotUsersСollapseButton.innerHTML = '<i class="bi bi-arrow-down d-flex" style="font-size: 20px;"></i>';
		} else {
			telegramBotUsersСollapseButton.innerHTML = '<i class="bi bi-arrow-up d-flex" style="font-size: 20px;"></i>';
		}
	});
	updateTelegramBotUsersButton.addEventListener('click', () => updateTelegramBotUsers());
}
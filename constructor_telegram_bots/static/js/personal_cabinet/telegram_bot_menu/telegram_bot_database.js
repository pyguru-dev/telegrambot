{
	const databaseRecords = document.querySelector('#databaseRecords');

	function updateDatabaseRecords() {
		fetch(getTelegramBotDatabeseRecordsUrl, {
			method: 'POST',
			headers: {'Authorization': `Token ${userApiToken}`},
		}).then(response => {
			response.json().then(jsonResponse => {
				if (response.ok) {
					jsonResponse.forEach(databaseRecord => {
						const databaseRecordDiv = document.createElement('div')
						databaseRecordDiv.className = 'list-group-item px-3 py-2';
						databaseRecordDiv.innerHTML = [
							'<div class="d-flex justify-content-between align-items-center">',
								JSON.stringify(databaseRecord),
							'	<button class="btn p-0">',
							`		<i class="bi bi-trash text-danger delete" id="${databaseRecord['_id']}" style="font-size: 1.5rem;"></i>`,
							'	</button>',
							'</div>',
						].join('');

						databaseRecordDiv.querySelector(`.delete`).addEventListener('click', function() {
							fetch(`/telegram-bot/${telegramBotId}/database/record/${this.id}/delete/`, {
								method: 'POST',
								headers: {'Authorization': `Token ${userApiToken}`},
							}).then(response => {response.json().then(jsonResponse => createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']))});
						});

						databaseRecords.append(databaseRecordDiv)
					});
				} else {
					createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
				}
			});
		});
	}

	updateDatabaseRecords();
}
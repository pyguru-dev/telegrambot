{
	const telegramBotDatabaseRecordsDiv = document.querySelector('#telegramBotDatabaseRecords');

	const checkTelegramBotDatabaseRecordsСount = () => {
		if (telegramBotDatabaseRecordsDiv.querySelectorAll('.database-record').length == 0) {
			const telegramBotDatabaseNotHaveRecordDiv = document.createElement('div');
			telegramBotDatabaseNotHaveRecordDiv.className = 'list-group-item database-not-have-record px-3 py-2';
			telegramBotDatabaseNotHaveRecordDiv.innerHTML = `<p class="text-center my-2">${telegramBotDatabaseNotHaveDataText}</p>`;
			telegramBotDatabaseRecordsDiv.append(telegramBotDatabaseNotHaveRecordDiv);
		} else {
			const telegramBotDatabaseNotHaveRecordDiv = telegramBotDatabaseRecordsDiv.querySelector('.database-not-have-record');

			if (telegramBotDatabaseNotHaveRecordDiv != null) {
				telegramBotDatabaseNotHaveRecordDiv.remove();
			}
		}
	}

	const addTelegramBotDatabaseRecord = (telegramBotDatabaseRecord) => {
		const telegramBotDatabaseRecordDiv = document.createElement('div');
		telegramBotDatabaseRecordDiv.className = 'list-group-item database-record p-3';
		telegramBotDatabaseRecordDiv.innerHTML = [
			'<div class="d-flex justify-content-between align-items-center">',
			'	<div class="border border-2 border-dark-subtle rounded w-100 p-2">',
			'		<div class="editor">',
			'			<div class="spinner-border text-secondary ms-2 mt-2" role="status">',
			'				<span class="visually-hidden"></span>',
			'			</div>',
			'		</div>',
			'	</div>',
			'	<div class="d-flex buttons justify-content-between align-items-center ms-3">',
			'		<div class="btn-group confirm-and-cancel me-2 d-none" role="group">',
			`			<button class="btn btn-success confirm px-2 py-1" id="${telegramBotDatabaseRecord['_id']}">`,
			'				<i class="bi bi-check-lg d-flex justify-content-center" style="font-size: 20px"></i>',
			'			</button>',
			`			<button class="btn btn-danger cancel px-2 py-1">`,
			'				<i class="bi bi-x-lg d-flex justify-content-center" style="font-size: 20px; -webkit-text-stroke: 1px;"></i>',
			'			</button>',
			'		</div>',
			`		<button class="btn btn-danger delete px-2 py-1 disabled" id="${telegramBotDatabaseRecord['_id']}">`,
			'			<div class="spinner-border spinner-border-sm" role="status">',
			'				<span class="visually-hidden"></span>',
			'			</div>',
			'		</button>',
			'	</div>',
			'</div>',
		].join('');
		telegramBotDatabaseRecordsDiv.append(telegramBotDatabaseRecordDiv);

		checkTelegramBotDatabaseRecordsСount();

		const telegramBotDatabaseRecordEditorDiv = telegramBotDatabaseRecordDiv.querySelector('.editor');
		const telegramBotDatabaseRecordConfirmAndCancelButtonsGroup = telegramBotDatabaseRecordDiv.querySelector('.confirm-and-cancel');
		const telegramBotDatabaseRecordConfirmButton = telegramBotDatabaseRecordDiv.querySelector('.confirm');
		const telegramBotDatabaseRecordCancelButton = telegramBotDatabaseRecordDiv.querySelector('.cancel');
		const telegramBotDatabaseRecordDeleteButton = telegramBotDatabaseRecordDiv.querySelector('.delete');

		require(['vs/editor/editor.main'], function() {
			telegramBotDatabaseRecordEditorDiv.querySelector('.spinner-border').remove();

			telegramBotDatabaseRecordDeleteButton.classList.remove('disabled');
			telegramBotDatabaseRecordDeleteButton.innerHTML = '<i class="bi bi-trash d-flex justify-content-center" style="font-size: 20px;"></i>';

			let telegramBotDatabaseRecordData = JSON.stringify(telegramBotDatabaseRecord, null, '\t');

			const telegramBotDatabaseRecordMonacoEditor = monaco.editor.create(telegramBotDatabaseRecordEditorDiv, {
				value: telegramBotDatabaseRecordData,
				language: 'json',
				lineNumbers: "off",
				folding: false,
				lineDecorationsWidth: 0,
				minimap: {enabled: false},
				overviewRulerLanes: 0,
				scrollBeyondLastLine: false,
				scrollbar: {
					vertical: 'hidden',
					horizontal: 'hidden',
				},
				renderLineHighlight: 'none',
			});

			const updateTelegramBotDatabaseRecordMonacoEditorHeight = () => {
				telegramBotDatabaseRecordMonacoEditor.layout({height: telegramBotDatabaseRecordMonacoEditor.getContentHeight()});
				telegramBotDatabaseRecordMonacoEditor.layout();
			}
			updateTelegramBotDatabaseRecordMonacoEditorHeight();
			telegramBotDatabaseRecordMonacoEditor.onDidChangeModelContent(event => {
				telegramBotDatabaseRecordConfirmAndCancelButtonsGroup.classList.remove('d-none');
				updateTelegramBotDatabaseRecordMonacoEditorHeight();
			});

			telegramBotDatabaseRecordConfirmButton.addEventListener('click', function() {
				fetch(`/telegram-bot/${telegramBotId}/database/records/${this.id}/`, {
					method: 'PATCH',
					headers: {
						'Content-Type': 'application/json',
						'Authorization': `Token ${userApiToken}`,
					},
					body: JSON.stringify({'updated_record': JSON.parse(telegramBotDatabaseRecordMonacoEditor.getModel().getValue())}),
				}).then(response => {
					response.json().then(jsonResponse => {
						if (response.ok) {
							telegramBotDatabaseRecordData = JSON.stringify(jsonResponse['record'], null, '\t');
							telegramBotDatabaseRecordMonacoEditor.setValue(telegramBotDatabaseRecordData);
							telegramBotDatabaseRecordConfirmAndCancelButtonsGroup.classList.add('d-none');
						}

						createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
					});
				});
			});
			telegramBotDatabaseRecordCancelButton.addEventListener('click', function() {
				telegramBotDatabaseRecordMonacoEditor.setValue(telegramBotDatabaseRecordData);
				telegramBotDatabaseRecordConfirmAndCancelButtonsGroup.classList.add('d-none');
			});
			telegramBotDatabaseRecordDeleteButton.addEventListener('click', function() {
				const telegramBotDatabaseRecordId = this.id;

				askConfirmModal(
					deleteTelegramBotDatabaseRecordAskConfirmModalTitle,
					deleteTelegramBotDatabaseRecordAskConfirmModalText,
					function() {
						fetch(`/telegram-bot/${telegramBotId}/database/records/${telegramBotDatabaseRecordId}/`, {
							method: 'DELETE',
							headers: {'Authorization': `Token ${userApiToken}`},
						}).then(response => {
							if (response.ok) {
								telegramBotDatabaseRecordDiv.remove();
								checkTelegramBotDatabaseRecordsСount();
							}

							response.json().then(jsonResponse => createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']));
						});
					}
				);
			});
		});
	}

	{
		const updateTelegramBotDatabaseRecords = () => {
			fetch(telegramBotDatabeseRecordsUrl, {
				method: 'GET',
				headers: {'Authorization': `Token ${userApiToken}`},
			}).then(response => {
				response.json().then(jsonResponse => {
					if (response.ok) {
						telegramBotDatabaseRecordsDiv.innerHTML = '';

						if (jsonResponse.length > 0) {
							jsonResponse.forEach(telegramBotDatabaseRecord => addTelegramBotDatabaseRecord(telegramBotDatabaseRecord));
						} else {
							checkTelegramBotDatabaseRecordsСount();
						}
					} else {
						createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level'])
					};
				});
			});
		}

		const telegramBotDatabaseRecordsСollapseButton = document.querySelector('#telegramBotDatabaseRecordsСollapseButton');
		const updateTelegramBotDatabaseRecordsButton = document.querySelector('#updateTelegramBotDatabaseRecordsButton');
		const telegramBotDatabaseRecordsBootstrapСollapse = new bootstrap.Collapse('#telegramBotDatabaseRecordsСollapse');
		const addTelegramBotDatabaseRecordButton = document.querySelector('#addTelegramBotDatabaseRecordButton');

		telegramBotDatabaseRecordsСollapseButton.addEventListener('click', function() {
			updateTelegramBotDatabaseRecordsButton.classList.toggle('disabled');
			telegramBotDatabaseRecordsBootstrapСollapse.toggle();
			addTelegramBotDatabaseRecordButton.classList.toggle('disabled');

			if (telegramBotDatabaseRecordsСollapseButton.querySelector('i').classList.contains('bi-arrow-up')) {
				telegramBotDatabaseRecordsСollapseButton.innerHTML = '<i class="bi bi-arrow-down d-flex" style="font-size: 20px;"></i>';
			} else {
				telegramBotDatabaseRecordsСollapseButton.innerHTML = '<i class="bi bi-arrow-up d-flex" style="font-size: 20px;"></i>';
			}
		});
		updateTelegramBotDatabaseRecordsButton.addEventListener('click', () => updateTelegramBotDatabaseRecords());
		addTelegramBotDatabaseRecordButton.addEventListener('click', function() {
			const telegramBotDatabaseRecordDiv = document.createElement('div');
			telegramBotDatabaseRecordDiv.className = 'list-group-item database-record p-3';
			telegramBotDatabaseRecordDiv.innerHTML = [
				'<div class="d-flex justify-content-between align-items-center">',
				'	<div class="border border-2 border-success-subtle rounded w-100 p-2">',
				'		<div class="editor">',
				'			<div class="spinner-border text-secondary ms-2 mt-2" role="status">',
				'				<span class="visually-hidden"></span>',
				'			</div>',
				'		</div>',
				'	</div>',
				'	<div class="d-flex justify-content-between align-items-center ms-3">',
				'	<div class="btn-group" role="group">',
				`		<button class="btn btn-success confirm px-2 py-1 disabled">`,
				'			<div class="spinner-border spinner-border-sm" role="status">',
				'				<span class="visually-hidden"></span>',
				'			</div>',
				'		</button>',
				`		<button class="btn btn-danger cancel px-2 py-1 disabled">`,
				'			<div class="spinner-border spinner-border-sm" role="status">',
				'				<span class="visually-hidden"></span>',
				'			</div>',
				'		</button>',
				'	</div>',
				'</div>',
			].join('');
			telegramBotDatabaseRecordsDiv.append(telegramBotDatabaseRecordDiv);

			checkTelegramBotDatabaseRecordsСount();

			const telegramBotDatabaseRecordEditorDiv = telegramBotDatabaseRecordDiv.querySelector('.editor');
			const telegramBotDatabaseRecordConfirmButton = telegramBotDatabaseRecordDiv.querySelector('.confirm');
			const telegramBotDatabaseRecordCancelButton = telegramBotDatabaseRecordDiv.querySelector('.cancel');

			require(['vs/editor/editor.main'], function() {
				telegramBotDatabaseRecordEditorDiv.querySelector('.spinner-border').remove();

				telegramBotDatabaseRecordConfirmButton.classList.remove('disabled');
				telegramBotDatabaseRecordConfirmButton.innerHTML = '<i class="bi bi-check-lg d-flex justify-content-center" style="font-size: 20px"></i>';

				telegramBotDatabaseRecordCancelButton.classList.remove('disabled');
				telegramBotDatabaseRecordCancelButton.innerHTML = '<i class="bi bi-x-lg d-flex justify-content-center" style="font-size: 20px; -webkit-text-stroke: 1px;"></i>';

				const telegramBotDatabaseRecordMonacoEditor = monaco.editor.create(telegramBotDatabaseRecordEditorDiv, {
					value: JSON.stringify({'key': 'value'}, null, '\t'),
					language: 'json',
					lineNumbers: "off",
					folding: false,
					lineDecorationsWidth: 0,
					minimap: {enabled: false},
					overviewRulerLanes: 0,
					scrollBeyondLastLine: false,
					scrollbar: {
						vertical: 'hidden',
						horizontal: 'hidden',
					},
					renderLineHighlight: 'none',
				});

				const updateTelegramBotDatabaseRecordMonacoEditorHeight = () => {
					telegramBotDatabaseRecordMonacoEditor.layout({height: telegramBotDatabaseRecordMonacoEditor.getContentHeight()});
					telegramBotDatabaseRecordMonacoEditor.layout();
				}
				updateTelegramBotDatabaseRecordMonacoEditorHeight();
				telegramBotDatabaseRecordMonacoEditor.onDidChangeModelContent(event => updateTelegramBotDatabaseRecordMonacoEditorHeight());

				telegramBotDatabaseRecordConfirmButton.addEventListener('click', function() {
					fetch(telegramBotDatabeseRecordsUrl, {
						method: 'POST',
						headers: {
							'Content-Type': 'application/json',
							'Authorization': `Token ${userApiToken}`,
						},
						body: JSON.stringify({'record': JSON.parse(telegramBotDatabaseRecordMonacoEditor.getModel().getValue())}),
					}).then(response => {
						response.json().then(jsonResponse => {
							if (response.ok) {
								telegramBotDatabaseRecordDiv.remove();
								addTelegramBotDatabaseRecord(jsonResponse['record']);
							}

							createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
						});
					});
				});
				telegramBotDatabaseRecordCancelButton.addEventListener('click', function() {
					telegramBotDatabaseRecordDiv.remove();
					checkTelegramBotDatabaseRecordsСount();
				});
			});
		});

		updateTelegramBotDatabaseRecords();
	}
}
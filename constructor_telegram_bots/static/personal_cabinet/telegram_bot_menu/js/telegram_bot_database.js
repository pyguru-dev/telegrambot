{
	let databaseRecordsDiv;

	const checkDatabaseRecordsСount = () => {
		if (databaseRecordsDiv.querySelectorAll('.database-record').length == 0) {
			const databaseNotHaveRecordDiv = document.createElement('div');
			databaseNotHaveRecordDiv.className = 'list-group-item database-not-have-record px-3 py-2';
			databaseNotHaveRecordDiv.innerHTML = `<p class="text-center my-2">${telegramBotDatabaseNotHaveDataText}</p>`;
			databaseRecordsDiv.append(databaseNotHaveRecordDiv);
		} else {
			const databaseNotHaveRecordDiv = databaseRecordsDiv.querySelector('.database-not-have-record');
			if (databaseNotHaveRecordDiv != null) {databaseNotHaveRecordDiv.remove()}
		}
	}

	const addDatabaseRecord = (databaseRecord) => {
		const databaseRecordDiv = document.createElement('div');
		databaseRecordDiv.className = 'list-group-item database-record p-3';
		databaseRecordDiv.innerHTML = [
			'<div class="d-flex justify-content-between align-items-center">',
			'	<div class="editor border border-2 border-dark-subtle rounded w-100 p-2">',
			'		<div class="spinner-border text-secondary ms-2 mt-2" role="status">',
			'			<span class="visually-hidden"></span>',
			'		</div>',
			'	</div>',
			'	<div class="d-flex buttons justify-content-between align-items-center mx-3">',
			'		<div class="btn-group confirm-and-cancel me-2 d-none" role="group">',
			`			<button class="btn btn-success confirm px-2 py-0" id="${databaseRecord['_id']}">`,
			'				<i class="bi bi-check-lg" style="font-size: 20px"></i>',
			'			</button>',
			`			<button class="btn btn-danger cancel px-2 py-0">`,
			'				<i class="bi bi-x-lg" style="font-size: 20px; -webkit-text-stroke: 1px;"></i>',
			'			</button>',
			'		</div>',
			`		<button class="btn btn-danger delete px-2 py-1 disabled" id="${databaseRecord['_id']}">`,
			'			<div class="spinner-border spinner-border-sm" role="status">',
			'				<span class="visually-hidden"></span>',
			'			</div>',
			'		</button>',
			'	</div>',
			'</div>',
		].join('');
		databaseRecordsDiv.append(databaseRecordDiv);

		checkDatabaseRecordsСount();

		const databaseRecordEditorDiv = databaseRecordDiv.querySelector('.editor');
		const databaseRecordConfirmAndCancelButtonsGroup = databaseRecordDiv.querySelector('.confirm-and-cancel');
		const databaseRecordConfirmButton = databaseRecordDiv.querySelector('.confirm');
		const databaseRecordCancelButton = databaseRecordDiv.querySelector('.cancel');
		const databaseRecordDeleteButton = databaseRecordDiv.querySelector('.delete');

		require(['vs/editor/editor.main'], function() {
			databaseRecordEditorDiv.querySelector('.spinner-border').remove();

			databaseRecordDeleteButton.classList.replace('py-1', 'py-0');
			databaseRecordDeleteButton.classList.remove('disabled');
			databaseRecordDeleteButton.innerHTML = '<i class="bi bi-trash" style="font-size: 20px;"></i>';

			const databaseRecordMonacoEditor = monaco.editor.create(databaseRecordEditorDiv, {
				value: JSON.stringify(databaseRecord, null, '\t'),
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

			const updateDatabaseRecordMonacoEditorHeight = () => {
				databaseRecordMonacoEditor.layout({height: databaseRecordMonacoEditor.getContentHeight() - 16});
				databaseRecordMonacoEditor.layout();
			}

			updateDatabaseRecordMonacoEditorHeight();

			databaseRecordMonacoEditor.onDidChangeModelContent(event => {
				databaseRecordConfirmAndCancelButtonsGroup.classList.remove('d-none');
				updateDatabaseRecordMonacoEditorHeight();
			});

			databaseRecordConfirmButton.addEventListener('click', function() {
				fetch(`/telegram-bot/${telegramBotId}/database/records/${this.id}/`, {
					method: 'PATCH',
					headers: {
						'Content-Type': 'application/json',
						'Authorization': `Token ${userApiToken}`,
					},
					body: JSON.stringify({'updated_record': JSON.parse(databaseRecordMonacoEditor.getModel().getValue())}),
				}).then(response => {
					response.json().then(jsonResponse => {
						if (response.ok) {
							databaseRecordMonacoEditor.setValue(JSON.stringify(jsonResponse['record'], null, '\t'));
							databaseRecordDiv.querySelector('.buttons').classList.replace('mx-3', 'ms-3');
							databaseRecordConfirmAndCancelButtonsGroup.classList.add('d-none');
						}

						createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
					});
				});
			});

			databaseRecordCancelButton.addEventListener('click', function() {
				databaseRecordMonacoEditor.setValue(JSON.stringify(databaseRecord, null, '\t'));
				databaseRecordConfirmAndCancelButtonsGroup.classList.add('d-none');
			});

			databaseRecordDeleteButton.addEventListener('click', function() {
				const databaseRecordId = this.id;

				askConfirmModal(
					deleteTelegramBotDatabaseRecordAskConfirmModalTitle,
					deleteTelegramBotDatabaseRecordAskConfirmModalText,
					function() {
						fetch(`/telegram-bot/${telegramBotId}/database/records/${databaseRecordId}/`, {
							method: 'DELETE',
							headers: {'Authorization': `Token ${userApiToken}`},
						}).then(response => {
							if (response.ok) {
								databaseRecordDiv.remove();
								checkDatabaseRecordsСount();
							}

							response.json().then(jsonResponse => {createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level'])});
						});
					}
				);
			});
		});
	}
	{
		const updateDatabaseRecords = () => {
			fetch(telegramBotDatabeseRecordsUrl, {
				method: 'GET',
				headers: {'Authorization': `Token ${userApiToken}`},
			}).then(response => {
				response.json().then(jsonResponse => {
					if (response.ok) {
						databaseRecordsDiv.innerHTML = '';
						(jsonResponse.length > 0) ? jsonResponse.forEach(databaseRecord => addDatabaseRecord(databaseRecord)) : checkDatabaseRecordsСount();
					} else {createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level'])}
				});
			});
		}

		const showDatabaseRecordsButton = document.querySelector('#showDatabaseRecords');

		showDatabaseRecordsButton.addEventListener('click', function() {
			require.config({paths: {'vs': monacoEditorMinVsFolderUrl}});

			databaseRecordsDiv = document.createElement('div');
			databaseRecordsDiv.classList = 'card-body';
			databaseRecordsDiv.innerHTML = '<div class="list-group" id="databaseRecords"></div>';
			showDatabaseRecordsButton.parentElement.insertAdjacentElement('beforebegin', databaseRecordsDiv);

			databaseRecordsDiv = databaseRecordsDiv.querySelector('#databaseRecords');

			const addDatabaseRecordButton = document.createElement('button');
			addDatabaseRecordButton.id = 'addDatabaseRecord';
			addDatabaseRecordButton.classList = 'btn btn-light rounded-top-0 w-100 px-3';
			addDatabaseRecordButton.type = 'button';
			addDatabaseRecordButton.style.height = '42px';
			addDatabaseRecordButton.innerHTML = telegramBotDatabaseAddRecordButtonText;
			showDatabaseRecordsButton.insertAdjacentElement('beforebegin', addDatabaseRecordButton);

			addDatabaseRecordButton.addEventListener('click', function() {
				const databaseRecordDiv = document.createElement('div');
				databaseRecordDiv.className = 'list-group-item database-record p-3';
				databaseRecordDiv.innerHTML = [
					'<div class="d-flex justify-content-between align-items-center">',
					'	<div class="editor border border-2 border-success-subtle rounded w-100 p-2">',
					'		<div class="spinner-border text-secondary ms-2 mt-2" role="status">',
					'			<span class="visually-hidden"></span>',
					'		</div>',
					'	</div>',
					'	<div class="d-flex justify-content-between align-items-center mx-3">',
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
				databaseRecordsDiv.append(databaseRecordDiv);

				checkDatabaseRecordsСount();

				const databaseRecordEditorDiv = databaseRecordDiv.querySelector('.editor');
				const databaseRecordConfirmButton = databaseRecordDiv.querySelector('.confirm');
				const databaseRecordCancelButton = databaseRecordDiv.querySelector('.cancel');

				require(['vs/editor/editor.main'], function() {
					databaseRecordEditorDiv.querySelector('.spinner-border').remove();

					databaseRecordConfirmButton.classList.replace('py-1', 'py-0');
					databaseRecordConfirmButton.classList.remove('disabled');
					databaseRecordConfirmButton.innerHTML = '<i class="bi bi-check-lg" style="font-size: 20px"></i>';

					databaseRecordCancelButton.classList.replace('py-1', 'py-0');
					databaseRecordCancelButton.classList.remove('disabled');
					databaseRecordCancelButton.innerHTML = '<i class="bi bi-x-lg" style="font-size: 20px; -webkit-text-stroke: 1px;"></i>';

					const databaseRecordMonacoEditor = monaco.editor.create(databaseRecordEditorDiv, {
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
					});

					const updateDatabaseRecordMonacoEditorHeight = () => {
						databaseRecordMonacoEditor.layout({height: databaseRecordMonacoEditor.getContentHeight() - 16});
						databaseRecordMonacoEditor.layout();
					}

					updateDatabaseRecordMonacoEditorHeight();

					databaseRecordMonacoEditor.onDidChangeModelContent(event => updateDatabaseRecordMonacoEditorHeight());

					databaseRecordConfirmButton.addEventListener('click', function() {
						fetch(telegramBotDatabeseRecordsUrl, {
							method: 'POST',
							headers: {
								'Content-Type': 'application/json',
								'Authorization': `Token ${userApiToken}`,
							},
							body: JSON.stringify({'record': JSON.parse(databaseRecordMonacoEditor.getModel().getValue())}),
						}).then(response => {
							response.json().then(jsonResponse => {
								if (response.ok) {
									databaseRecordDiv.remove();
									addDatabaseRecord(jsonResponse['record']);
								}

								createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
							});
						});
					});

					databaseRecordCancelButton.addEventListener('click', function() {
						databaseRecordDiv.remove();
						checkDatabaseRecordsСount();
					});
				});
			});

			showDatabaseRecordsButton.parentElement.classList.remove('border-0');
			showDatabaseRecordsButton.remove();

			updateDatabaseRecords();
		});
	}
}
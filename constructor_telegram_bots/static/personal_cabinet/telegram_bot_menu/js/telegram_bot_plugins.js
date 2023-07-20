{
	const telegramBotPluginsDiv = document.querySelector('#telegramBotPlugins');

	const checkTelegramBotPluginsСount = () => {
		if (telegramBotPluginsDiv.querySelectorAll('.telegram-bot-plugin').length == 0) {
			const telegramBotNotHavePluginsDiv = document.createElement('div');
			telegramBotNotHavePluginsDiv.className = 'list-group-item px-3 py-2';
			telegramBotNotHavePluginsDiv.id = 'telegramBotNotHavePlugins';
			telegramBotNotHavePluginsDiv.innerHTML = `<p class="text-center my-2">${telegramBotNotHavePluginText}</p>`;
			telegramBotPluginsDiv.append(telegramBotNotHavePluginsDiv);
		} else {
			const telegramBotNotHavePluginsDiv = telegramBotPluginsDiv.querySelector('#telegramBotNotHavePlugins');

			if (telegramBotNotHavePluginsDiv != null) {
				telegramBotNotHavePluginsDiv.remove();
			}
		}
	}

	const addTelegramBotPlugin = (telegramBotPlugin) => {
		const telegramBotPluginDiv = document.createElement('div');
		telegramBotPluginDiv.classList = 'list-group-item telegram-bot-plugin p-3 pt-2';
		telegramBotPluginDiv.innerHTML = [
			`<h5>${telegramBotPluginNameText} ${telegramBotPlugin['name']}</h5>`,
			'<div class="d-flex justify-content-between align-items-center">',
			'	<div class="border border-2 border-dark-subtle rounded w-100 pe-2 py-2">',
			'		<div class="editor">',
			'			<div class="spinner-border text-secondary ms-2 mt-2" role="status">',
			'				<span class="visually-hidden"></span>',
			'			</div>',
			'		</div>',
			'	</div>',
			'	<div class="d-flex buttons align-items-center ms-3">',
			'		<div class="d-flex me-3">',
			'			<span class="me-1">Проверен:</span>',
			`			<i class="bi bi-${(telegramBotPlugin['is_checked']) ? 'check' : 'x'}-circle-fill text-${(telegramBotPlugin['is_checked']) ? 'success' : 'danger'} d-flex align-items-center is_checked" style="margin-top: 2px"></i>`,
			'		</div>',
			'		<div class="btn-group confirm-and-cancel me-2 d-none" role="group">',
			`			<button class="btn btn-success confirm px-2 py-1" id="${telegramBotPlugin['id']}">`,
			'				<i class="bi bi-check-lg d-flex justify-content-center" style="font-size: 20px"></i>',
			'			</button>',
			'			<button class="btn btn-danger cancel px-2 py-1">',
			'				<i class="bi bi-x-lg d-flex justify-content-center" style="font-size: 20px;"></i>',
			'			</button>',
			'		</div>',
			`		<button class="btn btn-danger delete px-2 py-1 disabled" id="${telegramBotPlugin['id']}">`,
			'			<div class="spinner-border spinner-border-sm" role="status">',
			'				<span class="visually-hidden"></span>',
			'			</div>',
			'		</button>',
			'	</div>',
			'</div>',
		].join('');
		telegramBotPluginsDiv.append(telegramBotPluginDiv);

		checkTelegramBotPluginsСount();

		const telegramBotPluginEditorDiv = telegramBotPluginDiv.querySelector('.editor');
		const telegramBotPluginIsCheckedIcon = telegramBotPluginDiv.querySelector('.is_checked');
		const telegramBotPluginConfirmAndCancelButtonsGroup = telegramBotPluginDiv.querySelector('.confirm-and-cancel');
		const telegramBotPluginConfirmButton = telegramBotPluginDiv.querySelector('.confirm');
		const telegramBotPluginCancelButton = telegramBotPluginDiv.querySelector('.cancel');
		const telegramBotPluginDeleteButton = telegramBotPluginDiv.querySelector('.delete');

		require(['vs/editor/editor.main'], function() {
			telegramBotPluginEditorDiv.querySelector('.spinner-border').remove();

			telegramBotPluginDeleteButton.classList.remove('disabled');
			telegramBotPluginDeleteButton.innerHTML = '<i class="bi bi-trash d-flex justify-content-center" style="font-size: 20px;"></i>';

			let telegramBotPluginCode = telegramBotPlugin['code'];

			const telegramBotPluginMonacoEditor = monaco.editor.create(telegramBotPluginEditorDiv, {
				value: telegramBotPluginCode,
				language: 'python',
				folding: false,
				lineDecorationsWidth: 0,
				minimap: {enabled: false},
				overviewRulerLanes: 0,
				scrollBeyondLastLine: false,
				scrollbar: {vertical: 'hidden'},
				renderLineHighlight: 'none',
			});

			updateMonacoEditorHeight(telegramBotPluginMonacoEditor);
			telegramBotPluginMonacoEditor.onDidChangeModelContent(() => {
				telegramBotPluginConfirmAndCancelButtonsGroup.classList.remove('d-none');
				updateMonacoEditorHeight(telegramBotPluginMonacoEditor);
			});

			const telegramBotPluginConfirmOrCancelButtonClick = () => {
				telegramBotPluginMonacoEditor.setValue(telegramBotPluginCode);
				telegramBotPluginConfirmAndCancelButtonsGroup.classList.add('d-none');
				updateMonacoEditorHeight(telegramBotPluginMonacoEditor);
			}

			telegramBotPluginConfirmButton.addEventListener('click', function() {
				fetch(`/plugins/${this.id}/`, {
					method: 'PATCH',
					headers: {
						'Content-Type': 'application/json',
						'Authorization': `Token ${userApiToken}`,
					},
					body: JSON.stringify({'code': telegramBotPluginMonacoEditor.getModel().getValue()}),
				}).then(response => {
					response.json().then(jsonResponse => {
						if (response.ok) {
							telegramBotPluginIsCheckedIcon.classList.remove('bi-check-circle-fill', 'text-success');
							telegramBotPluginIsCheckedIcon.classList.add('bi-x-circle-fill', 'text-danger');
							telegramBotPluginCode = jsonResponse['plugin']['code'];

							telegramBotPluginConfirmOrCancelButtonClick(telegramBotPluginCode);
						}

						createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
					});
				});
			});
			telegramBotPluginCancelButton.addEventListener('click', () => telegramBotPluginConfirmOrCancelButtonClick(telegramBotPluginCode));
			telegramBotPluginDeleteButton.addEventListener('click', function() {
				const telegramBotPluginId = this.id;

				askConfirmModal(
					deleteTelegramBotPluginAskConfirmModalTitle,
					deleteTelegramBotPluginAskConfirmModalText,
					function() {
						fetch(`/plugins/${telegramBotPluginId}/`, {
							method: 'DELETE',
							headers: {'Authorization': `Token ${userApiToken}`},
						}).then(response => {
							if (response.ok) {
								telegramBotPluginDiv.remove();
								checkTelegramBotPluginsСount();
							}

							response.json().then(jsonResponse => {
								createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
							});
						});
					}
				);
			});
		});
	}

	const updateTelegramBotPlugins = () => {
		fetch(telegramBotPluginsUrl, {
			method: 'GET',
			headers: {'Authorization': `Token ${userApiToken}`},
		}).then(response => {
			response.json().then(jsonResponse => {
				if (response.ok) {
					telegramBotPluginsDiv.innerHTML = '';

					if (jsonResponse.length > 0) {
						jsonResponse.forEach(telegramBotPlugin => addTelegramBotPlugin(telegramBotPlugin));
					} else {
						checkTelegramBotPluginsСount();
					}
				} else {
					createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
				}
			});
		});
	}

	updateTelegramBotPlugins();

	const telegramBotPluginsСollapseButton = document.querySelector('#telegramBotPluginsСollapseButton');
	const updateTelegramBotPluginsButton = document.querySelector('#updateTelegramBotPluginsButton');
	const telegramBotPluginsBootstrapСollapse = new bootstrap.Collapse('#telegramBotPluginsСollapse');
	const addTelegramBotPluginButton = document.querySelector('#addTelegramBotPluginButton');

	telegramBotPluginsСollapseButton.addEventListener('click', function() {
		updateTelegramBotPluginsButton.classList.toggle('disabled');
		telegramBotPluginsBootstrapСollapse.toggle();
		addTelegramBotPluginButton.classList.toggle('disabled');

		if (telegramBotPluginsСollapseButton.querySelector('i').classList.contains('bi-arrow-up')) {
			telegramBotPluginsСollapseButton.innerHTML = '<i class="bi bi-arrow-down d-flex" style="font-size: 20px;"></i>';
		} else {
			telegramBotPluginsСollapseButton.innerHTML = '<i class="bi bi-arrow-up d-flex" style="font-size: 20px;"></i>';
		}
	});
	updateTelegramBotPluginsButton.addEventListener('click', () => updateTelegramBotPlugins());
	addTelegramBotPluginButton.addEventListener('click', function() {
		const telegramBotPluginDiv = document.createElement('div');
		telegramBotPluginDiv.classList = 'list-group-item telegram-bot-plugin p-3';
		telegramBotPluginDiv.innerHTML = [
			'<div class="d-flex justify-content-between align-items-center">',
			'	<div class="w-100">',
			`		<input class="form-control name mb-2" type="text" placeholder="${telegramBotPluginNameInputPlaceholderText}">`,
			'		<div class="border border-2 border-success-subtle rounded pe-2 py-2">',
			'			<div class="editor">',
			'				<div class="spinner-border text-secondary ms-2 mt-2" role="status">',
			'					<span class="visually-hidden"></span>',
			'				</div>',
			'			</div>',
			'		</div>',
			'	</div>',
			'	<div class="btn-group ms-3" role="group">',
			'		<button class="btn btn-success confirm px-2 py-1 disabled">',
			'			<div class="spinner-border spinner-border-sm role="status">',
			'				<span class="visually-hidden"></span>',
			'			</div>',
			'		</button>',
			'		<button class="btn btn-danger cancel px-2 py-1 disabled">',
			'			<div class="spinner-border spinner-border-sm" role="status">',
			'				<span class="visually-hidden"></span>',
			'			</div>',
			'		</button>',
			'	</div>',
			'</div>',
		].join('');
		telegramBotPluginsDiv.append(telegramBotPluginDiv);

		checkTelegramBotPluginsСount();

		const telegramBotPluginNameInput = telegramBotPluginDiv.querySelector('.name');
		const telegramBotPluginEditorDiv = telegramBotPluginDiv.querySelector('.editor');
		const telegramBotPluginConfirmButton = telegramBotPluginDiv.querySelector('.confirm');
		const telegramBotPluginCancelButton = telegramBotPluginDiv.querySelector('.cancel');

		require(['vs/editor/editor.main'], function() {
			telegramBotPluginEditorDiv.querySelector('.spinner-border').remove();

			telegramBotPluginConfirmButton.classList.remove('disabled');
			telegramBotPluginConfirmButton.innerHTML = '<i class="bi bi-check-lg d-flex justify-content-center" style="font-size: 20px"></i>';

			telegramBotPluginCancelButton.classList.remove('disabled');
			telegramBotPluginCancelButton.innerHTML = '<i class="bi bi-x-lg d-flex justify-content-center" style="font-size: 20px;"></i>';

			const telegramBotPluginMonacoEditor = monaco.editor.create(telegramBotPluginEditorDiv, {
				value: `# ${telegramBotPluginCodePlaceholderText}`,
				language: 'python',
				folding: false,
				lineDecorationsWidth: 0,
				minimap: {enabled: false},
				overviewRulerLanes: 0,
				scrollBeyondLastLine: false,
				scrollbar: {vertical: 'hidden'},
				renderLineHighlight: 'none',
			});

			updateMonacoEditorHeight(telegramBotPluginMonacoEditor);
			telegramBotPluginMonacoEditor.onDidChangeModelContent(() => updateMonacoEditorHeight(telegramBotPluginMonacoEditor));

			telegramBotPluginConfirmButton.addEventListener('click', function() {
				fetch(telegramBotPluginsUrl, {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'Authorization': `Token ${userApiToken}`,
					},
					body: JSON.stringify({
						'name': telegramBotPluginNameInput.value,
						'code': telegramBotPluginMonacoEditor.getModel().getValue(),
					}),
				}).then(response => {
					response.json().then(jsonResponse => {
						if (response.ok) {
							telegramBotPluginDiv.remove();
							addTelegramBotPlugin(jsonResponse['plugin']);
						}

						createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level']);
					});
				});
			});
			telegramBotPluginCancelButton.addEventListener('click', function() {
				telegramBotPluginDiv.remove();
				checkTelegramBotPluginsСount();
			});
		});
	});
}
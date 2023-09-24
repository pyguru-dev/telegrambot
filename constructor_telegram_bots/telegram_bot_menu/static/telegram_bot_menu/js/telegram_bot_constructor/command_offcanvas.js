const copyToBuffer = (value) => {
	navigator.clipboard.writeText(`{{ ${value} }}`);
	createToast(telegramBotCommandOffcanvasSuccessfullyCopyToBufferText, 'success');
}

{
	class Addition {
		constructor(additionDiv) {
			this.additionDiv = additionDiv;
			this.additionButton = document.querySelector(`[addition-target="#${this.additionDiv.id}"]`);
			this.additionButtonClickShowExtraFunc = null;
			this.additionButtonClickHideExtraFunc = null;
			this.isShow = false;

			this.additionButton.addEventListener('click', () => this.toggle());
		}
		toggle() {
			(this.additionDiv.classList.contains('d-none')) ? this.show() : this.hide();
		}
		show() {
			this.isShow = true;

			this.additionDiv.classList.remove('d-none');
			this.additionButton.classList.replace('btn-dark', 'btn-secondary');

			if (this.additionButtonClickShowExtraFunc) this.additionButtonClickShowExtraFunc();
		}
		hide() {
			this.isShow = false;

			this.additionDiv.classList.add('d-none');
			this.additionButton.classList.replace('btn-secondary', 'btn-dark');

			if (this.additionButtonClickHideExtraFunc) this.additionButtonClickHideExtraFunc();
		}
	}

	class Name {
		constructor() {
			this.input = document.querySelector('#telegramBotCommandOffcanvasNameInput');
		}
		get() {
			return this.input.value;
		}
		set(telegramBotCommand) {
			this.input.value = telegramBotCommand.name;
		}
		reset() {
			this.input.value = null;
		}
	}

	class Command extends Addition {
		constructor() {
			super(document.querySelector('#telegramBotCommandOffcanvasCommandAddition'));

			this.textInput = document.querySelector('#telegramBotCommandOffcanvasCommandTextInput');
			this.descriptionInput = document.querySelector('#telegramBotCommandOffcanvasCommandDescriptionInput');
			this.showInMenuButton = document.querySelector('#telegramBotCommandOffcanvasCommandShowInMenuButton');
			this.notShowInMenuButton = document.querySelector('#telegramBotCommandOffcanvasCommandNotShowInMenuButton');
			this.isShowInMenu = false;

			this.showInMenuButton.addEventListener('click', () => this.showDescriptionInput());
			this.notShowInMenuButton.addEventListener('click', () => this.hideDescriptionInput());
		}
		showDescriptionInput(description=null) {
			this.descriptionInput.classList.remove('d-none');
			this.descriptionInput.value = description;
			this.showInMenuButton.classList.add('d-none');
			this.notShowInMenuButton.classList.remove('d-none');
			this.isShowInMenu = true;
		}
		hideDescriptionInput() {
			this.descriptionInput.classList.add('d-none');
			this.descriptionInput.value = null;
			this.showInMenuButton.classList.remove('d-none');
			this.notShowInMenuButton.classList.add('d-none');
			this.isShowInMenu = false;
		}
		get() {
			if (this.isShow) {
				return {
					text: this.textInput.value,
					is_show_in_menu: this.isShowInMenu,
					description: (this.isShowInMenu) ? this.descriptionInput.value : null,
				}
			}
			return null;
		}
		set(telegramBotCommand) {
			if (telegramBotCommand.command) {
				this.show();
				this.textInput.value = telegramBotCommand.command.text;
				if (telegramBotCommand.command.is_show_in_menu) this.showDescriptionInput(telegramBotCommand.command.description);
			}
		}
		reset() {
			this.hide();
			this.textInput.value = null;
			this.hideDescriptionInput();
		}
	}

	class Image extends Addition {
		constructor() {
			super(document.querySelector('#telegramBotCommandOffcanvasImageAddition'));

			this.previewImg = document.querySelector('#telegramBotCommandOffcanvasImagePreview');
			this.input = document.querySelector('#telegramBotCommandOffcanvasImageInput');
			this.file = null;

			this.input.addEventListener('change', (event) => {
				this.file = event.target.files[0];
				const imageReader = new FileReader();

				imageReader.readAsDataURL(this.file);
				imageReader.addEventListener('load', () => {
					this.previewImg.classList.remove('d-none');
					this.previewImg.src = imageReader.result;
				});
			});
		}
		get() {
			if (this.isShow && !this.previewImg.classList.contains('d-none')) {
				return (this.file) ? this.file : 'not_edited';
			}
			return null;
		}
		set(telegramBotCommand) {
			if (telegramBotCommand.image) {
				this.show();
				this.previewImg.classList.remove('d-none');
				this.previewImg.src = telegramBotCommand.image;
			}
		}
		reset() {
			this.hide();
			this.previewImg.classList.add('d-none');
			this.previewImg.removeAttribute('src');
			this.input.value = null;
			this.file = null;
		}
	}

	class MessageText {
		constructor() {
			this.div = document.querySelector('#telegramBotCommandOffcanvasMessageText');
			this.messageTextModesRadios = document.querySelectorAll('[name="telegramBotCommandOffcanvasMessageTextModes"]');
			this.monacoEditor = null;
			this.mode = null;

			this.messageTextModesRadios.forEach(messageTextModeRadio => messageTextModeRadio.addEventListener('click', () => this.setMode(messageTextModeRadio.value)));
		}
		createMonacoEditor(language) {
			this.div.innerHTML = [
				'<div class="border rounded" id="telegramBotCommandOffcanvasMessageTextEditor" style="padding: 7px 12px;">',
				'	<div>',
				'		<div class="spinner-border text-secondary ms-2 mt-2" role="status">',
				'			<span class="visually-hidden"></span>',
				'		</div>',
				'	</div>',
				'</div>',
			].join('');

			require(['vs/editor/editor.main'], () => {
				const messageTextEditorDiv = document.querySelector('#telegramBotCommandOffcanvasMessageTextEditor');
				messageTextEditorDiv.querySelector('.spinner-border').remove();

				this.monacoEditor = monaco.editor.create(messageTextEditorDiv.querySelector('div'), {
					value: (language === 'markdown') ? `__${telegramBotCommandOffcanvasMessageTextPlaceholderText}__` : `<b>${telegramBotCommandOffcanvasMessageTextPlaceholderText}</b>`,
					language: language,
					lineNumbers: 'off',
					folding: false,
					lineDecorationsWidth: 0,
					minimap: {enabled: false},
					overviewRulerLanes: 0,
					scrollBeyondLastLine: false,
					scrollbar: {horizontal: 'hidden'},
					renderLineHighlight: 'none',
					wordWrap: 'on',
					fontSize: '16px',
					fontWeight: '400',
					fontFamily: 'inherit',
				});
				this.monacoEditor.layout({height: 144});
				this.monacoEditor.layout();
			});
		}
		setMode(mode) {
			if (mode !== this.mode) {
				this.mode = mode;

				this.messageTextModesRadios.forEach(messageTextModeRadio => messageTextModeRadio.checked = (messageTextModeRadio.value === this.mode));

				if (this.mode === 'default') {
					this.div.innerHTML = `<textarea class="form-control" placeholder="${telegramBotCommandOffcanvasMessageTextPlaceholderText}" style="height: 160px; resize: none;"></textarea>`;
				} else {
					this.createMonacoEditor(mode);
				}
			}
		}
		get() {
			return {
				mode: this.mode,
				text: (this.mode === 'default') ? this.div.querySelector('textarea').value : this.monacoEditor.getModel().getValue(),
			}
		}
		set(telegramBotCommand) {
			this.setMode(telegramBotCommand.message_text.mode);

			if (this.mode === 'default') {
				this.div.querySelector('textarea').value = telegramBotCommand.message_text.text;
			} else {
				const setMessageText = () => {
					if (this.monacoEditor) {
						this.monacoEditor.setValue(telegramBotCommand.message_text.text);
						return true
					}
					return false
				}

				const isSuccess = setMessageText();

				if (!isSuccess) {
					const intervalId = setInterval(() => {
						const isSuccess = setMessageText();
						if (isSuccess) clearInterval(intervalId);
					}, 1000);
				}

			}
		}
		reset() {
			this.monacoEditor = null;
			this.mode = null;
			this.setMode('default');
		}
	}

	class Keyboard extends Addition {
		constructor() {
			super(document.querySelector('#telegramBotCommandOffcanvasKeyboardAddition'));

			this.modesRadios = document.querySelectorAll('[name="telegramBotCommandOffcanvasKeyboardModes"]');
			this.buttonsRowsDiv = document.querySelector('#telegramBotCommandOffcanvasKeyboardButtonsRows');
			this.selectedKeyboardButtonRowButton = null;
			this.buttonsDiv = document.querySelector('#telegramBotCommandOffcanvasKeyboardButtons');
			this.mode = null;

			this.modesRadios.forEach(keyboardModeRadio => keyboardModeRadio.addEventListener('click', () => this.setMode(keyboardModeRadio.value)));
			document.querySelector('#telegramBotCommandOffcanvasKeyboardAddButton').addEventListener('click', () => this.createButton());

		}
		insertRowButton(keyboardButtonDiv, keyboardButtonNameInput, keyboardButtonRowButton_) {
			const keyboardButtonRowButton = keyboardButtonRowButton_.cloneNode(true);
			keyboardButtonRowButton.classList.replace('btn-dark', 'btn-secondary');
			keyboardButtonRowButton.style.width = '35px';
			keyboardButtonDiv.appendChild(keyboardButtonRowButton);
			keyboardButtonDiv.insertBefore(keyboardButtonRowButton, keyboardButtonNameInput);

			keyboardButtonRowButton.addEventListener('click', () => keyboardButtonRowButton.remove());
		}
		createRowButton() {
			const keyboardButtonsCount = this.buttonsDiv.querySelectorAll('.keyboard-button').length + 1;
			const keyboardButtonRowButtonWidth = (this.buttonsRowsDiv.clientWidth - (8 + 4 * 7)) / 8;

			const keyboardButtonRowButton = document.createElement('button');
			keyboardButtonRowButton.classList = 'btn btn-sm btn-dark btn-row';
			keyboardButtonRowButton.setAttribute('row-num', keyboardButtonsCount);
			keyboardButtonRowButton.style.width = `${keyboardButtonRowButtonWidth}px`;
			keyboardButtonRowButton.innerHTML = keyboardButtonsCount;
			this.buttonsRowsDiv.appendChild(keyboardButtonRowButton);

			keyboardButtonRowButton.addEventListener('click', () => {
				this.buttonsRowsDiv.querySelectorAll('button').forEach(keyboardButtonRowButton => keyboardButtonRowButton.classList.replace('btn-secondary', 'btn-dark'));

				if (this.selectedKeyboardButtonRowButton !== keyboardButtonRowButton) {
					this.selectedKeyboardButtonRowButton = keyboardButtonRowButton;
					keyboardButtonRowButton.classList.replace('btn-dark', 'btn-secondary');
				} else {
					this.selectedKeyboardButtonRowButton = null;
				}
			});
		}
		addLinkButtonClick(keyboardButtonDiv, keyboardButtonAddLinkButton, value=null) {
			const keyboardButtonLinkInput = document.createElement('input');
			keyboardButtonLinkInput.classList = 'form-control form-control-sm border border-dark link-input text-center';
			keyboardButtonLinkInput.type = 'text';
			keyboardButtonLinkInput.placeholder = telegramBotCommandOffcanvasKeyboardButtonUrlInputPlaceholderText;
			keyboardButtonLinkInput.style.boxShadow = 'none';
			if (value) keyboardButtonLinkInput.value = value;
			keyboardButtonDiv.replaceChild(keyboardButtonLinkInput, keyboardButtonAddLinkButton);
			keyboardButtonLinkInput.focus();
		}
		createAddLinkButton(keyboardButtonDiv) {
			const keyboardButtonAddLinkButton = document.createElement('button');
			keyboardButtonAddLinkButton.classList = 'btn btn-sm btn-primary btn-add-link';
			keyboardButtonAddLinkButton.type = 'button';
			keyboardButtonAddLinkButton.innerHTML = '<i class="bi bi-link-45deg" style="-webkit-text-stroke: 0.25px;"></i>';
			keyboardButtonDiv.appendChild(keyboardButtonAddLinkButton);
			keyboardButtonDiv.insertBefore(keyboardButtonAddLinkButton, keyboardButtonDiv.querySelector('.btn-delete'));

			keyboardButtonAddLinkButton.addEventListener('click', () => this.addLinkButtonClick(keyboardButtonDiv, keyboardButtonAddLinkButton));
		}
		createButton(telegramBotCommandKeyboardButton=null) {
			this.createRowButton();

			const keyboardButtonDiv = document.createElement('div');
			if (telegramBotCommandKeyboardButton) keyboardButtonDiv.id = telegramBotCommandKeyboardButton.id;
			keyboardButtonDiv.classList = 'input-group keyboard-button';
			keyboardButtonDiv.innerHTML = [
				'<button class="btn btn-sm btn-dark btn-move-up" type="button"><i class="bi bi-arrow-up" style="-webkit-text-stroke: 1px;"></i></button>',
				'<button class="btn btn-sm btn-dark btn-move-down" type="button"><i class="bi bi-arrow-down" style="-webkit-text-stroke: 1px;"></i></button>',
				`<input class="form-control form-control-sm border border-dark name-input text-center" type="text" placeholder="${telegramBotCommandOffcanvasKeyboardButtonNameInputPlaceholderText}" style="box-shadow: none;">`,
				'<button class="btn btn-sm btn-danger btn-delete" type="button"><i class="bi bi-x-lg" style="-webkit-text-stroke: 1.25px;"></i></button>',
			].join('');
			this.buttonsDiv.appendChild(keyboardButtonDiv);

			const keyboardButtonNameInput = keyboardButtonDiv.querySelector('.name-input');

			keyboardButtonNameInput.addEventListener('mouseover', () => keyboardButtonNameInput.style.cursor = (this.selectedKeyboardButtonRowButton) ? 'copy' : null);
			keyboardButtonNameInput.addEventListener('click', () => {
				if (this.selectedKeyboardButtonRowButton) {
					const oldKeyboardButtonRowButton = keyboardButtonDiv.querySelector('.btn-row');
					if (oldKeyboardButtonRowButton) oldKeyboardButtonRowButton.remove();

					this.insertRowButton(keyboardButtonDiv, keyboardButtonNameInput, this.selectedKeyboardButtonRowButton);

					this.selectedKeyboardButtonRowButton = null;
					this.buttonsRowsDiv.querySelectorAll('button').forEach(keyboardButtonRowButton => keyboardButtonRowButton.classList.replace('btn-secondary', 'btn-dark'));
				}
			});

			(telegramBotCommandKeyboardButton) ? keyboardButtonNameInput.value = telegramBotCommandKeyboardButton.text : keyboardButtonNameInput.focus();

			keyboardButtonDiv.querySelector('.btn-move-up').addEventListener('click', () => {
				const previousKeyboardButtonDiv = keyboardButtonDiv.previousElementSibling;
				if (previousKeyboardButtonDiv) this.buttonsDiv.insertBefore(keyboardButtonDiv, previousKeyboardButtonDiv);
			});
			keyboardButtonDiv.querySelector('.btn-move-down').addEventListener('click', () => {
				const nextKeyboardButtonDiv = keyboardButtonDiv.nextElementSibling;
				if (nextKeyboardButtonDiv) this.buttonsDiv.insertBefore(nextKeyboardButtonDiv, keyboardButtonDiv);
			});

			if (this.mode === 'inline' || this.mode === 'payment') this.createAddLinkButton(keyboardButtonDiv);

			keyboardButtonDiv.querySelector('.btn-delete').addEventListener('click', () => {
				const keyboardButtonsRowsButtons = this.buttonsRowsDiv.querySelectorAll('.btn-row');
				const lastKeyboardButtonRowButton = keyboardButtonsRowsButtons[keyboardButtonsRowsButtons.length - 1];

				this.buttonsDiv.querySelectorAll('.keyboard-button').forEach(keyboardButton => {
					const keyboardButtonRowButton = keyboardButton.querySelector('.btn-row');
					if (keyboardButtonRowButton && lastKeyboardButtonRowButton.getAttribute('row-num') === keyboardButtonRowButton.getAttribute('row-num')) keyboardButtonRowButton.remove();
				})

				lastKeyboardButtonRowButton.remove();
				keyboardButtonDiv.remove();
			});
		}
		setMode(mode) {
			if (mode !== this.mode) {
				this.modesRadios.forEach(keyboardModeRadio => {
					if (keyboardModeRadio.value === mode) keyboardModeRadio.checked = true;
				});

				if (this.mode === 'default' && (mode === 'inline' || mode === 'payment')) {
					this.buttonsDiv.querySelectorAll('.keyboard-button').forEach(keyboardButtonDiv => this.createAddLinkButton(keyboardButtonDiv));
				} else if ((this.mode === 'inline' || this.mode === 'payment') && mode === 'default') {
					this.buttonsDiv.querySelectorAll('.keyboard-button').forEach(keyboardButtonDiv => {
						const keyboardButtonAddLinkButton = keyboardButtonDiv.querySelector('.btn-add-link');
						const keyboardButtonLinkInput = keyboardButtonDiv.querySelector('.link-input');

						if (keyboardButtonAddLinkButton) keyboardButtonAddLinkButton.remove();
						if (keyboardButtonLinkInput) keyboardButtonLinkInput.remove();
					});
				}

				this.mode = mode;
			}
		}
		get() {
			if (this.isShow) {
				const keyboardButtons = [];

				this.buttonsDiv.querySelectorAll('.keyboard-button').forEach(keyboardButtonDiv => {
					const keyboardButtonRowButton = keyboardButtonDiv.querySelector('.btn-row');
					const keyboardButtonLinkInput = keyboardButtonDiv.querySelector('.link-input');

					keyboardButtons.push({
						id: (keyboardButtonDiv.id) ? parseInt(keyboardButtonDiv.id) : null,
						row: (keyboardButtonRowButton) ? parseInt(keyboardButtonRowButton.getAttribute('row-num')) : null,
						text: keyboardButtonDiv.querySelector('.name-input').value,
						url: (keyboardButtonLinkInput) ? keyboardButtonLinkInput.value : null,
					});
				});

				return {
					mode: this.mode,
					buttons: keyboardButtons,
				}
			}
			return null;
		}
		set(telegramBotCommand) {
			if (telegramBotCommand.keyboard) {
				this.show();
				this.setMode(telegramBotCommand.keyboard.mode);
				telegramBotCommand.keyboard.buttons.forEach(telegramBotCommandKeyboardButton => this.createButton(telegramBotCommandKeyboardButton));
				telegramBotCommand.keyboard.buttons.forEach(telegramBotCommandKeyboardButton => {
					const keyboardButtonDiv = document.querySelector(`.keyboard-button[id="${telegramBotCommandKeyboardButton.id}"]`);

					if (telegramBotCommandKeyboardButton.row) {
						const keyboardButtonNameInput = keyboardButtonDiv.querySelector('.name-input');
						const keyboardButtonRowButton = this.buttonsRowsDiv.querySelector(`button[row-num="${telegramBotCommandKeyboardButton.row}"]`);

						this.insertRowButton(keyboardButtonDiv, keyboardButtonNameInput, keyboardButtonRowButton);
					}

					if (telegramBotCommandKeyboardButton.url) {
						const keyboardButtonAddLinkButton = keyboardButtonDiv.querySelector('.btn-add-link');

						this.addLinkButtonClick(keyboardButtonDiv, keyboardButtonAddLinkButton, telegramBotCommandKeyboardButton.url);
					}
				});
			}
		}
		reset() {
			this.hide();
			this.buttonsRowsDiv.innerHTML = '';
			this.selectedKeyboardButtonRowButton = null;
			this.buttonsDiv.innerHTML = '';
			this.mode = null;
			this.setMode('default');
		}
	}

	class ApiRequest extends Addition {
		constructor() {
			super(document.querySelector('#telegramBotCommandOffcanvasApiRequestAddition'));

			this.urlInput = document.querySelector('#telegramBotCommandOffcanvasApiRequestUrlInput');
			this.headersEditorDiv = document.querySelector('#telegramBotCommandOffcanvasApiRequestHeadersEditor');
			this.headersMonacoEditor = null;
			this.showHeadersEditorDivButton = document.querySelector('#telegramBotCommandOffcanvasApiRequestShowHeadersEditorButton');
			this.hideHeadersEditorDivButton = document.querySelector('#telegramBotCommandOffcanvasApiRequestHideHeadersEditorButton');
			this.dataEditorDiv = document.querySelector('#telegramBotCommandOffcanvasApiRequestDataEditor');
			this.dataMonacoEditor = null;
			this.showDataEditorDivButton = document.querySelector('#telegramBotCommandOffcanvasApiRequestShowDataEditorButton');
			this.hideDataEditorDivButton = document.querySelector('#telegramBotCommandOffcanvasApiRequestHideDataEditorButton');
			this.method = null;

			this.showHeadersEditorDivButton.addEventListener('click', () => this.showEditorDiv(
				this.headersEditorDiv,
				'headersMonacoEditor',
				this.showHeadersEditorDivButton,
				this.hideHeadersEditorDivButton
			));
			this.hideHeadersEditorDivButton.addEventListener('click', () => this.hideEditorDiv(
				this.headersEditorDiv,
				'headersMonacoEditor',
				this.showHeadersEditorDivButton,
				this.hideHeadersEditorDivButton
			));
			this.showDataEditorDivButton.addEventListener('click', () => this.showEditorDiv(
				this.dataEditorDiv,
				'dataMonacoEditor',
				this.showDataEditorDivButton,
				this.hideDataEditorDivButton
			));
			this.hideDataEditorDivButton.addEventListener('click', () => this.hideEditorDiv(
				this.dataEditorDiv,
				'dataMonacoEditor',
				this.showDataEditorDivButton,
				this.hideDataEditorDivButton
			));
			document.querySelectorAll('[name="telegramBotCommandOffcanvasApiRequestMethods"]').forEach(apiRequestMethodRadio => apiRequestMethodRadio.addEventListener('click', () => this.setMethod(apiRequestMethodRadio.value)));
		}
		setMethod(method) {
			if (method !== this.method) {
				this.method = method;

				document.querySelectorAll('[name="telegramBotCommandOffcanvasApiRequestMethods"]').forEach(apiRequestMethodRadio => {
					if (this.method === apiRequestMethodRadio.value) apiRequestMethodRadio.checked = true;
				});
			}
		}
		showEditorDiv(editorDiv, monacoEditorVariableName, showButton, hideButton, value=null) {
			editorDiv.classList.remove('d-none');
			showButton.classList.add('d-none');
			hideButton.classList.remove('d-none');
			this.createMonacoEditor(editorDiv, monacoEditorVariableName, value);
		}
		hideEditorDiv(editorDiv, monacoEditorVariableName, showButton, hideButton) {
			editorDiv.classList.add('d-none');
			editorDiv.innerHTML = '';
			this[monacoEditorVariableName] = null;
			showButton.classList.remove('d-none');
			hideButton.classList.add('d-none');
		}
		createMonacoEditor(editorDiv, monacoEditorVariableName, value=null) {
			editorDiv.innerHTML = [
				'<div>',
				'	<div class="spinner-border text-secondary ms-2 mt-2" role="status">',
				'		<span class="visually-hidden"></span>',
				'	</div>',
				'</div>',
			].join('');

			require(['vs/editor/editor.main'], () => {
				editorDiv.querySelector('.spinner-border').remove();

				this[monacoEditorVariableName] = monaco.editor.create(editorDiv.querySelector('div'), {
					value: (value) ? value : JSON.stringify({'key': 'value'}, null, '\t'),
					language: 'json',
					lineNumbers: 'off',
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
				updateMonacoEditorHeight(this[monacoEditorVariableName]);
				this[monacoEditorVariableName].onDidChangeModelContent(() => updateMonacoEditorHeight(this[monacoEditorVariableName]));
			});
		}
		get() {
			if (this.isShow) {
				return {
					url: this.urlInput.value,
					method: this.method,
					headers: (this.headersMonacoEditor) ? this.headersMonacoEditor.getModel().getValue() : null,
					data: (this.dataMonacoEditor) ? this.dataMonacoEditor.getModel().getValue() : null,
				}
			}
			return null;
		}
		set(telegramBotCommand) {
			if (telegramBotCommand.api_request) {
				this.show();
				this.urlInput.value = telegramBotCommand.api_request.url;
				this.setMethod(telegramBotCommand.api_request.method);

				if (telegramBotCommand.api_request.headers) {
					this.showEditorDiv(
						this.headersEditorDiv,
						'headersMonacoEditor',
						this.showHeadersEditorDivButton,
						this.hideHeadersEditorDivButton,
						telegramBotCommand.api_request.headers,
					);
				}

				if (telegramBotCommand.api_request.data) {
					this.showEditorDiv(
						this.dataEditorDiv,
						'dataMonacoEditor',
						this.showDataEditorDivButton,
						this.hideDataEditorDivButton,
						telegramBotCommand.api_request.data,
					);
				}
			}
		}
		reset() {
			this.hide();
			this.urlInput.value = '';
			this.hideEditorDiv(
				this.headersEditorDiv,
				'headersMonacoEditor',
				this.showHeadersEditorDivButton,
				this.hideHeadersEditorDivButton
			);
			this.hideEditorDiv(
				this.dataEditorDiv,
				'dataMonacoEditor',
				this.showDataEditorDivButton,
				this.hideDataEditorDivButton
			);
			this.method = null;
			this.setMethod('get');
		}
	}

	class DatabaseRecord extends Addition {
		constructor() {
			super(document.querySelector('#telegramBotCommandOffcanvasDatabaseRecordAddition'));
			this.additionButtonClickShowExtraFunc = this.createMonacoEditor;

			this.editorDiv = document.querySelector('#telegramBotCommandOffcanvasDatabaseRecordEditor');
			this.monacoEditor = null;
		}
		createMonacoEditor(value=null) {
			this.editorDiv.innerHTML = [
				'<div>',
				'	<div class="spinner-border text-secondary ms-2 mt-2" role="status">',
				'		<span class="visually-hidden"></span>',
				'	</div>',
				'</div>',
			].join('');

			require(['vs/editor/editor.main'], () => {
				this.editorDiv.querySelector('.spinner-border').remove();

				this.monacoEditor = monaco.editor.create(this.editorDiv.querySelector('div'), {
					value: (value) ? value : JSON.stringify({'key': 'value'}, null, '\t'),
					language: 'json',
					lineNumbers: 'off',
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
				updateMonacoEditorHeight(this.monacoEditor);
				this.monacoEditor.onDidChangeModelContent(() => updateMonacoEditorHeight(this.monacoEditor));
			});
		}
		get() {
			return (this.isShow) ? this.monacoEditor.getModel().getValue() : null;
		}
		set(telegramBotCommand) {
			if (telegramBotCommand.database_record) {
				this.isShow = true;

				this.additionDiv.classList.remove('d-none');
				this.additionButton.classList.replace('btn-dark', 'btn-secondary');

				this.createMonacoEditor(telegramBotCommand.database_record);
			}
		}
		reset() {
			this.hide();
			this.editorDiv.innerHTML = '';
			this.monacoEditor = null;
		}
	}

	class TelegramBotCommandOffcanvas {
		constructor() {
			this.bootstrap = new bootstrap.Offcanvas('#telegramBotCommandOffcanvas');
			this.title = document.querySelector('#telegramBotCommandOffcanvasLabel');

			this.name = new Name();
			this.command = new Command();
			this.image = new Image();
			this.messageText = new MessageText();
			this.keyboard = new Keyboard();
			this.apiRequest = new ApiRequest();
			this.databaseRecord = new DatabaseRecord();

			this.addCommandButton = document.querySelector('#telegramBotCommandOffcanvasAddCommandButton');
			this.saveCommandButton = document.querySelector('#telegramBotCommandOffcanvasSaveCommandButton');

			document.querySelector('#telegramBotCommandOffcanvasButton').addEventListener('click', () => this.show('add', null));
			this.addCommandButton.addEventListener('click', () => this.sendData('POST', telegramBotCommandsUrl));
			this.saveCommandButton.addEventListener('click', () => {
				const telegramBotCommandId = this.saveCommandButton.getAttribute('telegram-bot-command-id');
				this.sendData('PATCH', `/telegram-bots/${telegramBotId}/commands/${telegramBotCommandId}/`);
			});
		}
		show(mode, telegramBotCommand) {
			this.reset();

			if (mode === 'add') {
				this.title.innerHTML = telegramBotCommandOffcanvasAddCommandTitleText;

				this.addCommandButton.classList.remove('d-none');
				this.saveCommandButton.classList.add('d-none');
			} else {
				this.title.innerHTML = telegramBotCommandOffcanvasEditCommandTitleText;

				this.addCommandButton.classList.add('d-none');
				this.saveCommandButton.classList.remove('d-none');
				this.saveCommandButton.setAttribute('telegram-bot-command-id', telegramBotCommand.id);

				this.name.set(telegramBotCommand);
				this.command.set(telegramBotCommand);
				this.image.set(telegramBotCommand);
				this.messageText.set(telegramBotCommand);
				this.keyboard.set(telegramBotCommand);
				this.apiRequest.set(telegramBotCommand);
				this.databaseRecord.set(telegramBotCommand);
			}

			this.bootstrap.toggle();
		}
		sendData(method, url) {
			const self = this;

			const formData = new FormData();
			formData.append('image', this.image.get());
			formData.append('data', JSON.stringify({
				'name': this.name.get(),
				'command': this.command.get(),
				'message_text': this.messageText.get(),
				'keyboard': this.keyboard.get(),
				'api_request': this.apiRequest.get(),
				'database_record': this.databaseRecord.get(),
			}));

			fetch(url, {
				method: method,
				headers: {'Authorization': `Token ${userApiToken}`},
				body: formData,
			}).then(response => {
				if (response.ok) {
					self.bootstrap.toggle();
					updateDiagramBlocks();
					self.reset();
				}

				response.json().then(jsonResponse => createToast(jsonResponse.message, jsonResponse.level));
			});
		}
		reset() {
			this.name.reset();
			this.command.reset();
			this.image.reset();
			this.messageText.reset();
			this.keyboard.reset();
			this.apiRequest.reset();
			this.databaseRecord.reset();
		}
	}

	var telegramBotCommandOffcanvas = new TelegramBotCommandOffcanvas();
}

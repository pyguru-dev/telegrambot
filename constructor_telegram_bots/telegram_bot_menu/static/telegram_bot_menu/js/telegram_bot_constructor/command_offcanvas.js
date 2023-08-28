const copyToBuffer = (value) => {
	navigator.clipboard.writeText(`{{ ${value} }}`);
	createToast(telegramBotCommandOffcanvasSuccessfullyCopyToBufferText, 'success');
}

{
	class Name {
		constructor() {
			this.input = document.querySelector('#telegramBotCommandOffcanvasNameInput');
		}
		reset() {
			this.input.value = null;
		}
	}

	class Command {
		constructor() {
			this.input = document.querySelector('#telegramBotCommandOffcanvasCommandInput');
			this.showInMenuCheckBox = document.querySelector('#telegramBotCommandOffcanvasCommandShowInMenuCheckbox');
		}
		reset() {
			this.input.value = null;
			this.showInMenuCheckBox.checked = false;
		}
	}

	class Image {
		constructor() {
			const self = this;

			this.previewImg = document.querySelector('#telegramBotCommandOffcanvasImagePreview');
			this.input = document.querySelector('#telegramBotCommandOffcanvasImageInput');
			this.file = null;

			this.input.addEventListener('change', function(event) {
				self.file = event.target.files[0];
				const imageReader = new FileReader();

				imageReader.addEventListener('load', function() {
					self.previewImg.classList.remove('d-none');
					self.previewImg.src = imageReader.result;
				});
				imageReader.readAsDataURL(self.file);
			});
		}
		reset() {
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
			const self = this;

			this.div.innerHTML = [
				'<div class="border rounded" id="telegramBotCommandOffcanvasMessageTextEditor" style="padding: 7px 12px;">',
				'	<div>',
				'		<div class="spinner-border text-secondary ms-2 mt-2" role="status">',
				'			<span class="visually-hidden"></span>',
				'		</div>',
				'	</div>',
				'</div>',
			].join('');

			require(['vs/editor/editor.main'], function() {
				const messageTextEditorDiv = document.querySelector('#telegramBotCommandOffcanvasMessageTextEditor');
				messageTextEditorDiv.querySelector('.spinner-border').remove();

				self.monacoEditor = monaco.editor.create(messageTextEditorDiv.querySelector('div'), {
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
				self.monacoEditor.layout({height: 144});
				self.monacoEditor.layout();
			});
		}
		setMode(mode) {
			if (mode !== this.mode) {
				this.mode = mode;

				this.messageTextModesRadios.forEach(messageTextModeRadio => {
					if (messageTextModeRadio.value === this.mode) {
						messageTextModeRadio.checked = true;
					}
				});

				if (this.mode === 'default') {
					this.div.innerHTML = `<textarea class="form-control" placeholder="${telegramBotCommandOffcanvasMessageTextPlaceholderText}" style="height: 160px; resize: none;"></textarea>`;
				} else {
					this.createMonacoEditor(mode);
				}
			}
		}
		reset() {
			this.monacoEditor = null;
			this.mode = null;
			this.setMode('default');
		}
	}

	class Keyboard {
		constructor() {
			this.modesRadios = document.querySelectorAll('[name="telegramBotCommandOffcanvasKeyboardModes"]');
			this.buttonsRowsDiv = document.querySelector('#telegramBotCommandOffcanvasKeyboardButtonsRows');
			this.selectedKeyboardButtonRowButton = null;
			this.buttonsDiv = document.querySelector('#telegramBotCommandOffcanvasKeyboardButtons');
			this.mode = null;

			this.modesRadios.forEach(keyboardModeRadio => keyboardModeRadio.addEventListener('click', () => this.setMode(keyboardModeRadio.value)));
			document.querySelector('#telegramBotCommandOffcanvasKeyboardAddButton').addEventListener('click', () => this.createButton());
		}
		createButtonAddLinkButton(keyboardButtonDiv) {
			const keyboardButtonAddLinkButton = document.createElement('button');
			keyboardButtonAddLinkButton.classList = 'btn btn-sm btn-primary btn-add-link';
			keyboardButtonAddLinkButton.type = 'button';
			keyboardButtonAddLinkButton.innerHTML = '<i class="bi bi-link-45deg" style="-webkit-text-stroke: 0.25px;"></i>';
			keyboardButtonDiv.appendChild(keyboardButtonAddLinkButton);
			keyboardButtonDiv.insertBefore(keyboardButtonAddLinkButton, keyboardButtonDiv.querySelector('.btn-delete'));

			keyboardButtonAddLinkButton.addEventListener('click', function() {
				const keyboardButtonLinkInput = document.createElement('input');
				keyboardButtonLinkInput.classList = 'form-control form-control-sm border border-dark link-input text-center';
				keyboardButtonLinkInput.type = 'text';
				keyboardButtonLinkInput.placeholder = telegramBotCommandOffcanvasKeyboardButtonUrlInputPlaceholderText;
				keyboardButtonLinkInput.style.boxShadow = 'none';
				keyboardButtonDiv.replaceChild(keyboardButtonLinkInput, keyboardButtonAddLinkButton);
				keyboardButtonLinkInput.focus();
			});
		}
		createButton() {
			const self = this;

			const keyboardButtonsCount = this.buttonsDiv.querySelectorAll('.keyboard-button').length + 1;
			const keyboardButtonRowButtonWidth = (this.buttonsRowsDiv.clientWidth - (8 + 4 * 7)) / 8;

			const keyboardButtonRowButton = document.createElement('button');
			keyboardButtonRowButton.className = 'btn btn-sm btn-dark btn-row';
			keyboardButtonRowButton.style.width = `${keyboardButtonRowButtonWidth}px`;
			keyboardButtonRowButton.innerHTML = keyboardButtonsCount;
			this.buttonsRowsDiv.appendChild(keyboardButtonRowButton);

			keyboardButtonRowButton.addEventListener('click', function() {
				self.buttonsRowsDiv.querySelectorAll('button').forEach(
					keyboardButtonRowButton => keyboardButtonRowButton.classList.replace('btn-secondary', 'btn-dark')
				);

				if (self.selectedKeyboardButtonRowButton !== keyboardButtonRowButton.innerHTML) {
					self.selectedKeyboardButtonRowButton = keyboardButtonRowButton;

					if (keyboardButtonRowButton.classList.contains('btn-dark')) {
						keyboardButtonRowButton.classList.replace('btn-dark', 'btn-secondary');
					} else {
						keyboardButtonRowButton.classList.replace('btn-secondary', 'btn-dark');
					}
				} else {
					self.selectedKeyboardButtonRowButton = null;
				}
			});

			const keyboardButtonDiv = document.createElement('div');
			keyboardButtonDiv.classList = 'input-group keyboard-button';
			keyboardButtonDiv.innerHTML = [
				'<button class="btn btn-sm btn-dark btn-move-up" type="button"><i class="bi bi-arrow-up" style="-webkit-text-stroke: 1px;"></i></button>',
				'<button class="btn btn-sm btn-dark btn-move-down" type="button"><i class="bi bi-arrow-down" style="-webkit-text-stroke: 1px;"></i></button>',
				`<input class="form-control form-control-sm border border-dark name-input text-center" type="text" placeholder="${telegramBotCommandOffcanvasKeyboardButtonNameInputPlaceholderText}" style="box-shadow: none;">`,
				'<button class="btn btn-sm btn-danger btn-delete" type="button"><i class="bi bi-x-lg" style="-webkit-text-stroke: 1.25px;"></i></button>',
			].join('');
			this.buttonsDiv.appendChild(keyboardButtonDiv);

			const keyboardButtonNameInput = keyboardButtonDiv.querySelector('.name-input');

			keyboardButtonNameInput.addEventListener('mouseover', () => keyboardButtonNameInput.style.cursor = (self.selectedKeyboardButtonRowButton) ? 'copy' : null);
			keyboardButtonNameInput.addEventListener('click', function() {
				if (self.selectedKeyboardButtonRowButton) {
					const oldKeyboardButtonRowButton = keyboardButtonDiv.querySelector('.btn-row');
					if (oldKeyboardButtonRowButton) oldKeyboardButtonRowButton.remove();

					const keyboardButtonRowButton = self.selectedKeyboardButtonRowButton.cloneNode(true);
					keyboardButtonRowButton.style.width = '35px';
					keyboardButtonDiv.appendChild(keyboardButtonRowButton);
					keyboardButtonDiv.insertBefore(keyboardButtonRowButton, keyboardButtonNameInput);

					self.selectedKeyboardButtonRowButton = null;
					self.buttonsRowsDiv.querySelectorAll('button').forEach(
						keyboardButtonRowButton => keyboardButtonRowButton.classList.replace('btn-secondary', 'btn-dark')
					);
				}
			});
			keyboardButtonNameInput.focus();

			keyboardButtonDiv.querySelector('.btn-move-up').addEventListener('click', function() {
				const previousKeyboardButtonDiv = keyboardButtonDiv.previousElementSibling;

				if (previousKeyboardButtonDiv) {
					self.buttonsDiv.insertBefore(keyboardButtonDiv, previousKeyboardButtonDiv);
				}
			});
			keyboardButtonDiv.querySelector('.btn-move-down').addEventListener('click', function() {
				const nextKeyboardButtonDiv = keyboardButtonDiv.nextElementSibling;

				if (nextKeyboardButtonDiv) {
					self.buttonsDiv.insertBefore(nextKeyboardButtonDiv, keyboardButtonDiv);
				}
			});

			if (this.mode === 'inline' || this.mode === 'payment') {
				this.createButtonAddLinkButton(keyboardButtonDiv);
			}

			keyboardButtonDiv.querySelector('.btn-delete').addEventListener('click', () => keyboardButtonDiv.remove());
		}
		setMode(mode) {
			if (mode !== this.mode) {
				this.modesRadios.forEach(keyboardModeRadio => {
					if (keyboardModeRadio.value === mode) {
						keyboardModeRadio.checked = true;
					}
				});

				if (this.mode === 'default' && (mode === 'inline' || mode === 'payment')) {
					this.buttonsDiv.querySelectorAll('.keyboard-button').forEach(keyboardButtonDiv => this.createButtonAddLinkButton(keyboardButtonDiv));
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
		reset() {
			this.buttonsRowsDiv.innerHTML = '';
			this.selectedKeyboardButtonRowButton = null;
			this.buttonsDiv.innerHTML = '';
			this.mode = null;
			this.setMode('default');
		}
	}

	class ApiRequest {
		constructor() {
			this.urlInput = document.querySelector('#telegramBotCommandOffcanvasApiRequestUrlInput');
			this.editorDiv = document.querySelector('#telegramBotCommandOffcanvasApiRequestDataEditor');
			this.monacoEditor = null;
			this.method = null;

			document.querySelectorAll('[name="telegramBotCommandOffcanvasApiRequestMethods"]').forEach(apiRequestMethodRadio => this.setMethod(apiRequestMethodRadio.value));
		}
		createMonacoEditor() {
			const self = this;

			this.editorDiv.innerHTML = [
				'<div>',
				'	<div class="spinner-border text-secondary ms-2 mt-2" role="status">',
				'		<span class="visually-hidden"></span>',
				'	</div>',
				'</div>',
			].join('');

			require(['vs/editor/editor.main'], function() {
				self.editorDiv.querySelector('.spinner-border').remove();

				self.monacoEditor = monaco.editor.create(self.editorDiv.querySelector('div'), {
					value: JSON.stringify({'key': 'value'}, null, '\t'),
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
				updateMonacoEditorHeight(self.monacoEditor);
				self.monacoEditor.onDidChangeModelContent(() => updateMonacoEditorHeight(self.monacoEditor));
			});
		}
		setMethod(method) {
			if (method !== this.method) {
				this.method = method;

				document.querySelectorAll('[name="telegramBotCommandOffcanvasApiRequestMethods"]').forEach(apiRequestMethodRadio => {
					if (this.method === apiRequestMethodRadio.value) {
						apiRequestMethodRadio.checked = true;
					}
				});
			}
		}
		reset() {
			this.urlInput.value = '';
			this.editorDiv.innerHTML = '';
			this.monacoEditor = null;
			this.method = null;
			this.setMethod('GET');
		}
	}

	class DatabaseRecord {
		constructor() {
			this.editorDiv = document.querySelector('#telegramBotCommandOffcanvasDatabaseRecordEditor');
			this.monacoEditor = null;
		}
		createMonacoEditor() {
			const self = this;

			this.editorDiv.innerHTML = [
				'<div>',
				'	<div class="spinner-border text-secondary ms-2 mt-2" role="status">',
				'		<span class="visually-hidden"></span>',
				'	</div>',
				'</div>',
			].join('');

			require(['vs/editor/editor.main'], function() {
				self.editorDiv.querySelector('.spinner-border').remove();

				self.monacoEditor = monaco.editor.create(self.editorDiv.querySelector('div'), {
					value: JSON.stringify({'key': 'value'}, null, '\t'),
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
				updateMonacoEditorHeight(self.monacoEditor);
				self.monacoEditor.onDidChangeModelContent(() => updateMonacoEditorHeight(self.monacoEditor));
			});
		}
		reset() {
			this.editorDiv.innerHTML = '';
			this.monacoEditor = null;
		}
	}

	class TelegramBotCommandOffcanvas {
		constructor() {
			const self = this;

			this.bootstrap = new bootstrap.Offcanvas('#telegramBotCommandOffcanvas');
			this.title = document.querySelector('#telegramBotCommandOffcanvasLabel');
			this.additions = document.querySelector('#telegramBotCommandOffcanvasAdditions');

			this.name = new Name();
			this.command = new Command();
			this.image = new Image();
			this.messageText = new MessageText();
			this.keyboard = new Keyboard();
			this.apiRequest = new ApiRequest();
			this.databaseRecord = new DatabaseRecord();

			document.querySelector('#telegramBotCommandOffcanvasButton').addEventListener('click', () => this.addCommand());

			this.additions.querySelectorAll('button').forEach(additionButton => {
				const additionButtonAdditionTarget = document.querySelector(additionButton.getAttribute('addition-target'));

				additionButton.addEventListener('click', function() {
					additionButtonAdditionTarget.classList.toggle('d-none');

					if (additionButton.classList.contains('btn-dark')) {
						if (additionButtonAdditionTarget.id === 'telegramBotCommandOffcanvasApiRequestAddition') {
							self.apiRequest.createMonacoEditor();
						} else if (additionButtonAdditionTarget.id === 'telegramBotCommandOffcanvasDatabaseRecordAddition') {
							self.databaseRecord.createMonacoEditor();
						}

						additionButton.classList.replace('btn-dark', 'btn-secondary');
					} else {
						additionButton.classList.replace('btn-secondary', 'btn-dark');
					}
				});
			});
		}
		addCommand() {
			this.title.innerHTML = telegramBotCommandOffcanvasAddCommandTitleText;

			this.reset();

			this.bootstrap.toggle();
		}
		editCommand() {
			
		}
		reset() {
			this.name.reset();
			this.command.reset();
			this.image.reset();
			this.messageText.reset();
			this.keyboard.reset();
			this.apiRequest.reset();
			this.databaseRecord.reset();

			this.additions.querySelectorAll('button').forEach(additionButton => {
				const additionButtonAdditionTarget = document.querySelector(additionButton.getAttribute('addition-target'));

				additionButtonAdditionTarget.classList.add('d-none');
				additionButton.classList.replace('btn-secondary', 'btn-dark');
			});
		}
	}

	var telegramBotCommandOffcanvas = new TelegramBotCommandOffcanvas();
}

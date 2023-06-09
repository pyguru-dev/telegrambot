{
	let addOrEditTelegramBotCommandCardHeader = document.querySelector('#addOrEditTelegramBotCommandCardHeader');

	let telegramBotCommandNameInput = document.querySelector('#telegramBotCommandNameInput');

	let telegramBotCommandAddCommandAdditionButton = document.querySelector('#telegramBotCommandAddCommandAdditionButton');
	let telegramBotCommandCommandAddition = document.querySelector('#telegramBotCommandCommandAddition');
	let telegramBotCommandCommandInput = document.querySelector('#telegramBotCommandCommandInput');

	var telegramBotCommandTextInput = document.querySelector('#telegramBotCommandTextInput');	

	let telegramBotCommandAddImageAdditionButton = document.querySelector('#telegramBotCommandAddImageAdditionButton');
	let telegramBotCommandImageAddition = document.querySelector('#telegramBotCommandImageAddition');
	let telegramBotCommandImagePreview = document.querySelector('#telegramBotCommandImagePreview');
	let telegramBotCommandImageInput = document.querySelector('#telegramBotCommandImageInput');
	let telegramBotCommandImageFile = null;

	let telegramBotCommandAddKeyboardAdditionButton = document.querySelector('#telegramBotCommandAddKeyboardAdditionButton');
	let telegramBotCommandKeyboardAddition = document.querySelector('#telegramBotCommandKeyboardAddition');
	let telegramBotCommandDefaultKeyboardRadio = document.querySelector('#telegramBotCommandDefaultKeyboardRadio');
	let telegramBotCommandInlineKeyboardRadio = document.querySelector('#telegramBotCommandInlineKeyboardRadio');
	let telegramBotCommandKeyboardButtons = document.querySelector('#telegramBotCommandKeyboardButtons');

	let telegramBotCommandAddApiRequestAdditionButton = document.querySelector('#telegramBotCommandAddApiRequestAdditionButton');
	let telegramBotCommandApiRequestAddition = document.querySelector('#telegramBotCommandApiRequestAddition');
	var telegramBotCommandApiRequestUrlInput = document.querySelector('#telegramBotCommandApiRequestUrlInput');
	var telegramBotCommandApiRequestDataInput = document.querySelector('#telegramBotCommandApiRequestDataInput');

	let telegramBotCommandAdditions = {
		telegramBotCommandAddCommandAdditionButton: telegramBotCommandCommandAddition,
		telegramBotCommandAddImageAdditionButton: telegramBotCommandImageAddition,
		telegramBotCommandAddKeyboardAdditionButton: telegramBotCommandKeyboardAddition,
		telegramBotCommandAddApiRequestAdditionButton: telegramBotCommandKeyboardAddition,
	};

	let backAddTelegramBotCommandButton = document.querySelector('.back-add-telegram-bot-command-button');
	var addOrEditTelegramBotCommandButton = document.querySelector('.add-or-edit-telegram-bot-command-button');

	function telegramBotCommandAllClear() {
		addOrEditTelegramBotCommandCardHeader.innerHTML = 'Добавление команды';

		telegramBotCommandNameInput.value = '';
		telegramBotCommandCommandInput.value = '';
		telegramBotCommandTextInput.value = '';

		telegramBotCommandImagePreview.classList.add('d-none');
		telegramBotCommandImagePreview.src = '';
		telegramBotCommandImageInput.value = null;
		telegramBotCommandImageFile = null;

		telegramBotCommandDefaultKeyboardRadio.checked = true;
		telegramBotCommandKeyboardButtons.innerHTML = '';

		telegramBotCommandApiRequestUrlInput.value = '';
		telegramBotCommandApiRequestDataInput.value = '';

		for (let telegramBotCommandAdditionButtonId in telegramBotCommandAdditions) {
			let telegramBotCommandAdditionButton = document.querySelector(`#${telegramBotCommandAdditionButtonId}`);
			let telegramBotCommandAddition = telegramBotCommandAdditions[telegramBotCommandAdditionButtonId];
			
			telegramBotCommandAdditionButton.classList.replace('btn-secondary', 'btn-dark');
			telegramBotCommandAddition.classList.add('d-none');
		}

		backAddTelegramBotCommandButton.classList.add('d-none');

		addOrEditTelegramBotCommandButton.id = '0';
		addOrEditTelegramBotCommandButton.innerHTML = 'Добавить команду';
	}

	for (let telegramBotCommandAdditionButtonId in telegramBotCommandAdditions) {
		let telegramBotCommandAdditionButton = document.querySelector(`#${telegramBotCommandAdditionButtonId}`);
		let telegramBotCommandAddition = telegramBotCommandAdditions[telegramBotCommandAdditionButtonId];

		telegramBotCommandAdditionButton.addEventListener('click', function() {
			if (telegramBotCommandAddition.classList.toggle('d-none') == false) {
				telegramBotCommandAdditionButton.classList.replace('btn-dark', 'btn-secondary');
			} else {
				telegramBotCommandAdditionButton.classList.replace('btn-secondary', 'btn-dark');
			}
		});
	}

	telegramBotCommandImageInput.addEventListener('change', function(event) {
		telegramBotCommandImageFile = event.target.files[0];
		
		let telegramBotCommandImageReader = new FileReader();
		telegramBotCommandImageReader.onload = function(event) {
			telegramBotCommandImagePreview.classList.remove('d-none');
			telegramBotCommandImagePreview.src = event.target.result;
		};
		telegramBotCommandImageReader.readAsDataURL(telegramBotCommandImageFile);
	});

	function telegramBotCommandAddKeyboardButton(id, value) {
		let inputGroup = document.createElement('div');
		inputGroup.classList = 'input-group mb-1';

		let telegramBotCommandKeyboardButton = document.createElement('input');
		telegramBotCommandKeyboardButton.classList = 'form-control btn btn-sm btn-outline-dark keyboard-button';
		telegramBotCommandKeyboardButton.id = id;
		telegramBotCommandKeyboardButton.type = 'text';
		telegramBotCommandKeyboardButton.style.cursor = 'text';
		telegramBotCommandKeyboardButton.value = value;

		let telegramBotCommandKeyboardButtonDelete = document.createElement('button');
		telegramBotCommandKeyboardButtonDelete.classList = 'btn btn-sm btn-danger';
		telegramBotCommandKeyboardButtonDelete.type = 'button';
		telegramBotCommandKeyboardButtonDelete.onclick = function () {
			inputGroup.remove();
		}

		let telegramBotCommandKeyboardButtonDeleteIcon = document.createElement('i');
		telegramBotCommandKeyboardButtonDeleteIcon.classList = 'bi bi-x-lg';
		telegramBotCommandKeyboardButtonDeleteIcon.style.webkitTextStroke = '1.5px';

		inputGroup.append(telegramBotCommandKeyboardButton);
		telegramBotCommandKeyboardButtonDelete.append(telegramBotCommandKeyboardButtonDeleteIcon);
		inputGroup.append(telegramBotCommandKeyboardButtonDelete);
		telegramBotCommandKeyboardButtons.append(inputGroup);

		telegramBotCommandKeyboardButton.focus();
	}

	document.querySelector('#telegramBotCommandAddKeyboardButton').addEventListener('click', () => telegramBotCommandAddKeyboardButton('', ''));

	backAddTelegramBotCommandButton.addEventListener('click', telegramBotCommandAllClear);

	function editTelegramBotCommand(telegramBotCommand) {
		telegramBotCommandAllClear();

		addOrEditTelegramBotCommandCardHeader.innerHTML = 'Редактирование команды';

		telegramBotCommandNameInput.value = telegramBotCommand['name'];

		if (telegramBotCommand['command'] != null) {
			telegramBotCommandAddCommandAdditionButton.classList.replace('btn-dark', 'btn-secondary');
			telegramBotCommandCommandAddition.classList.remove('d-none');
			telegramBotCommandCommandInput.value = telegramBotCommand['command'];
		}

		telegramBotCommandTextInput.value = telegramBotCommand['message_text'];

		if (telegramBotCommand['image'] != '') {
			telegramBotCommandAddImageAdditionButton.classList.replace('btn-dark', 'btn-secondary');
			telegramBotCommandImageAddition.classList.remove('d-none');
			telegramBotCommandImagePreview.classList.remove('d-none');
			telegramBotCommandImagePreview.src = `/${telegramBotCommand['image']}`;
		}

		if (telegramBotCommand['keyboard'] != null) {
			telegramBotCommandAddKeyboardAdditionButton.classList.replace('btn-dark', 'btn-secondary');
			telegramBotCommandKeyboardAddition.classList.remove('d-none');

			telegramBotCommandKeyboardType = telegramBotCommand['keyboard']['type'];
			if (telegramBotCommandKeyboardType == 'default') {
				telegramBotCommandDefaultKeyboardRadio.checked = true;
			} else {
				telegramBotCommandInlineKeyboardRadio.checked = true;
			}

			telegramBotCommand['keyboard']['buttons'].forEach(telegramBotCommandKeyboardButton => telegramBotCommandAddKeyboardButton(
				telegramBotCommandKeyboardButton['id'],
				telegramBotCommandKeyboardButton['text']
			));
		}

		if (telegramBotCommand['api_request'] != null) {
			telegramBotCommandAddApiRequestAdditionButton.classList.replace('btn-dark', 'btn-secondary');
			telegramBotCommandApiRequestAddition.classList.remove('d-none');

			telegramBotCommandApiRequestUrlInput.value = telegramBotCommand['api_request']['link'];
			telegramBotCommandApiRequestDataInput.value = telegramBotCommand['api_request']['data'];
		}

		backAddTelegramBotCommandButton.classList.remove('d-none');

		addOrEditTelegramBotCommandButton.id = telegramBotCommand['id'];
		addOrEditTelegramBotCommandButton.innerHTML = 'Сохранить команду';
	}

	addOrEditTelegramBotCommandButton.addEventListener('click', function() {
		let jsonTelegramBotCommandData = {
			'name': telegramBotCommandNameInput.value,
			'command': null,
			'message_text': telegramBotCommandTextInput.value,
			'keyboard': null,
			'api_request': null,
		}
	
		if (telegramBotCommandCommandAddition.classList.contains('d-none') == false) {
			jsonTelegramBotCommandData['command'] = telegramBotCommandCommandInput.value;
		}

		let telegramBotCommandData = new FormData();
		if (telegramBotCommandImagePreview.classList.contains('d-none') == false && telegramBotCommandImageFile == null) {
			telegramBotCommandData.append('image', 'not_edited');
		} else {
			telegramBotCommandData.append('image', telegramBotCommandImageFile);
		}

		if (telegramBotCommandKeyboardAddition.classList.contains('d-none') == false) {
			let telegramBotCommandKeyboardButtons_ = [];
			
			telegramBotCommandKeyboardButtons.querySelectorAll('input').forEach(telegramBotCommandKeyboardButton => telegramBotCommandKeyboardButtons_.push(
				{
					'id': telegramBotCommandKeyboardButton.id,
					'text': telegramBotCommandKeyboardButton.value,
				}
			));

			jsonTelegramBotCommandData['keyboard'] = {
				'type': telegramBotCommandKeyboardType,
				'buttons': telegramBotCommandKeyboardButtons_,
			}
		}

		if (telegramBotCommandApiRequestAddition.classList.contains('d-none') == false) {
			jsonTelegramBotCommandData['api_request'] = {
				'url': telegramBotCommandApiRequestUrlInput.value,
				'data': telegramBotCommandApiRequestDataInput.value,
			}
		}

		telegramBotCommandData.append('data', JSON.stringify(jsonTelegramBotCommandData));

		fetch(
			(this.id == '0') ? addTelegramBotCommandUrl : `/telegram-bot/${telegramBotId}/command/${this.id}/edit/`,
			{
				method: 'POST',
				body: telegramBotCommandData
			}
		).then(response => {
			if (response.ok) {
				getTelegramBotCommands();
				telegramBotCommandAllClear();

				response.text().then(responseText => createAlert(mainAlertContainer, responseText, 'success'));
			} else {
				response.text().then(responseText => createAlert(mainAlertContainer, responseText, 'danger'));
			}
		});
	});
}
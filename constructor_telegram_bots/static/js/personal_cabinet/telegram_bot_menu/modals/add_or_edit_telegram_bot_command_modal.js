{
	var keyboard = document.querySelector('.keyboard');
	var keyboardButtons = document.querySelector('#keyboardButtons');

	var keyboardButtonNum = 0;

	var addOrEditTelegramBotCommandUrl;

	function createKeyboardInput(value) {
		let keyboardButtonDiv = document.createElement('div');
		keyboardButtonDiv.setAttribute('class', 'input-group mb-1');

		let keyboardInput = document.createElement('input');
		keyboardInput.setAttribute('class', 'btn btn-sm btn-outline-dark border-end-0 rounded-0 rounded-start');
		keyboardInput.id = keyboardButtonNum;
		keyboardInput.type = 'text';
		keyboardInput.style = 'cursor: text; width: 90%;';
		keyboardInput.value = value;
		keyboardButtonDiv.append(keyboardInput);

		let deleteKeyboardButton = document.createElement('button')
		deleteKeyboardButton.setAttribute('class', 'btn btn-sm btn-danger rounded-0 rounded-end');
		deleteKeyboardButton.id = keyboardButtonNum;
		deleteKeyboardButton.type = 'button';
		deleteKeyboardButton.style = 'width: 10%;';
		deleteKeyboardButton.innerHTML = '<i class="bi bi-x-lg"></i>';
		keyboardButtonDiv.append(deleteKeyboardButton);

		keyboardButtons.append(keyboardButtonDiv);

		deleteKeyboardButton.addEventListener('click', function() {
			keyboardInput.remove();
			this.remove();
		});

		return keyboardInput;
	}

	function keyboardButtonFunc(keyboardButton, keyboardType) {
		keyboardButton.remove();
		
		if (keyboardType == 'inlineKeyboard') {
			createKeyboardInput('{}:{}').focus();
		} else{
			createKeyboardInput('').focus();
		}

		createKeyboardButton(keyboardType);
	}

	function createKeyboardButton(keyboardType) {
		let keyboardButton = document.createElement('button');
		keyboardButton.setAttribute('class', `btn btn-sm btn-outline-dark w-100`);
		keyboardButton.id = keyboardButtonNum;
		keyboardButton.type = 'button';
		keyboardButton.innerHTML = 'Добавить кнопку';
		keyboardButtons.append(keyboardButton);

		keyboardButton.addEventListener('click', () => keyboardButtonFunc(keyboardButton, keyboardType));

		keyboardButtonNum ++;
	}
}

{
	var examplekeyboardButton = document.querySelector('#examplekeyboardButton');

	var offKeyboardRadio = document.querySelector('#offKeyboardRadio');
	offKeyboardRadio.addEventListener('click', offKeyboard);

	function offKeyboard() {
		if (keyboard.id != 'offKeyboard') {
			keyboard.classList.add('d-none');
			keyboard.id = 'offKeyboard';
			keyboardButtons.innerHTML = '';
			offKeyboardRadio.checked = true;
		}
	}

	const keyboardRadios = [
		document.querySelector('#defaultKeyboardRadio'),
		document.querySelector('#inlineKeyboardRadio'),
	];

	for (let i = 0; i < keyboardRadios.length; i++) {
		keyboardRadios[i].addEventListener('click', function() {
			let keyboardType = keyboardRadios[i].id.replace('Radio', '');

			if (keyboard.id != keyboardType) {
				keyboard.classList.remove('d-none');
				keyboard.id = keyboardType;
				keyboardButtons.innerHTML = '';

				if (keyboardType == 'defaultKeyboard') {
					examplekeyboardButton.innerHTML = '<b>Текст</b>';
				} else {
					examplekeyboardButton.innerHTML = '<b>{Текст}:{CallBack текст}</b> или <b>{Текст}:{Ссылка}</b>';
				}

				createKeyboardButton(keyboardType);
			}
		});
	}
}

{
	var addOrEditTelegramBotCommandModalBootstrap = new bootstrap.Modal('#addOrEditTelegramBotCommandModal');

	var addOrEditTelegramBotCommandModallLabel = document.querySelector('#addOrEditTelegramBotCommandModallLabel');
	var addOrEditTelegramBotCommandModalAlertPlaceholder = document.querySelector('#addOrEditTelegramBotCommandModalAlertPlaceholder');

	var addOrEditTelegramBotCommandNameInput = document.querySelector('#addOrEditTelegramBotCommandNameInput');
	var addOrEditTelegramBotCommandCommandInput = document.querySelector('#addOrEditTelegramBotCommandCommandInput');
	var addOrEditTelegramBotCommandCallBackInput = document.querySelector('#addOrEditTelegramBotCommandCallBackInput');
	var addOrEditTelegramBotCommandTextInput = document.querySelector('#addOrEditTelegramBotCommandTextInput');

	let addOrEditTelegramBotCommandButton = document.querySelector('#addOrEditTelegramBotCommandButton');

	document.querySelector('#addTelegramBotCommandModalButton').addEventListener('click', function() {
		addOrEditTelegramBotCommandModallLabel.innerHTML = 'Добавление команды';

		addOrEditTelegramBotCommandNameInput.value = '';
		addOrEditTelegramBotCommandCommandInput.value = '';
		addOrEditTelegramBotCommandCallBackInput.value = '';
		addOrEditTelegramBotCommandTextInput.value = '';

		offKeyboard();

		addOrEditTelegramBotCommandUrl = `/telegram-bot/${telegramBotId}/command/add/`;

		addOrEditTelegramBotCommandButton.innerHTML = 'Добавить команду';
		addOrEditTelegramBotCommandButton.removeEventListener('click', addOrEditTelegramBotCommand);
		addOrEditTelegramBotCommandButton.addEventListener('click', addOrEditTelegramBotCommand);

		addOrEditTelegramBotCommandModalBootstrap.toggle();
	});

	function editTelegramBotCommandButton() {
		let telegramBotCommandId = this.id;

		let request = new XMLHttpRequest();
		request.open('POST', `/telegram-bot/${telegramBotId}/command/${telegramBotCommandId}/get-data/`, true);
		request.setRequestHeader('Content-Type', 'application/json');
		request.onreadystatechange = checkRequestResponse(function() {
			if (request.status == 200) {
				let telegramBotCommandData = JSON.parse(request.responseText);

				addOrEditTelegramBotCommandModallLabel.innerHTML = 'Редактирование команды';

				addOrEditTelegramBotCommandNameInput.value = telegramBotCommandData['name'];
				addOrEditTelegramBotCommandCommandInput.value = telegramBotCommandData['command'];
				addOrEditTelegramBotCommandCallBackInput.value = telegramBotCommandData['callback'];
				addOrEditTelegramBotCommandTextInput.value = telegramBotCommandData['message_text'];

				let telegramBotCommandKeyboard = JSON.parse(telegramBotCommandData['keyboard']);
				if (telegramBotCommandKeyboard[0] != 'offKeyboard') {
					document.querySelector(`#${telegramBotCommandKeyboard[0]}Radio`).checked = true;

					examplekeyboardButton.innerHTML = (telegramBotCommandKeyboard[0] == 'defaultKeyboard') ? '<b>Текст</b>' : '<b>{Текст}:{CallBack текст}</b> или <b>{Текст}:{Ссылка}</b>';
					
					keyboard.classList.remove('d-none');
					keyboard.id = telegramBotCommandKeyboard[0];
					keyboardButtons.innerHTML = '';

					for (let i = 0; i < telegramBotCommandKeyboard.length; i ++) {
						if (i > 0) {
							createKeyboardInput(telegramBotCommandKeyboard[i]);

							keyboardButtonNum ++;
						}
					}

					createKeyboardButton(telegramBotCommandKeyboard[0]);
				} else {
					offKeyboard();
				}

				addOrEditTelegramBotCommandUrl = `/telegram-bot/${telegramBotId}/command/${telegramBotCommandId}/edit/`;

				addOrEditTelegramBotCommandButton.innerHTML = 'Редактировать команду';
				addOrEditTelegramBotCommandButton.removeEventListener('click', addOrEditTelegramBotCommand);
				addOrEditTelegramBotCommandButton.addEventListener('click', addOrEditTelegramBotCommand);

				addOrEditTelegramBotCommandModalBootstrap.toggle();
			}
		});
		request.send();
	}

	function addOrEditTelegramBotCommand() {
		let telegramBotCommandKeyboard = [keyboard.id];

		let telegramBotCommandKeyboardButtons = keyboardButtons.querySelectorAll('input');
		for (let i = 0; i < telegramBotCommandKeyboardButtons.length; i ++) {
			telegramBotCommandKeyboard.push(telegramBotCommandKeyboardButtons[i].value);
		}

		let request = new XMLHttpRequest();
		request.open('POST', addOrEditTelegramBotCommandUrl, true);
		request.setRequestHeader('Content-Type', 'application/json');
		request.onreadystatechange = checkRequestResponse(function() {
			if (request.status == 200) {
				getTelegramBotCommands();

				addOrEditTelegramBotCommandModalBootstrap.toggle();

				myAlert(mainAlertPlaceholder, request.responseText, 'success');
			} else {
				myAlert(addOrEditTelegramBotCommandModalAlertPlaceholder, request.responseText, 'danger');
			}
		});
		request.send(JSON.stringify(
			{
				'name': addOrEditTelegramBotCommandNameInput.value,
				'command': addOrEditTelegramBotCommandCommandInput.value,
				'callback': addOrEditTelegramBotCommandCallBackInput.value,
				'message_text': addOrEditTelegramBotCommandTextInput.value,
				'keyboard': JSON.stringify(telegramBotCommandKeyboard),
			}
		));
	}
}
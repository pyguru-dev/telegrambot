{
	var addOrEditTelegramBotCommandModalBootstrap = new bootstrap.Modal('#addOrEditTelegramBotCommandModal');

	var addOrEditTelegramBotCommandModallLabel = document.querySelector('#addOrEditTelegramBotCommandModallLabel');
	let addOrEditTelegramBotCommandModalAlertPlaceholder = document.querySelector('#addOrEditTelegramBotCommandModalAlertPlaceholder');

	var addOrEditTelegramBotCommandNameInput = document.querySelector('#addOrEditTelegramBotCommandNameInput');
	var addOrEditTelegramBotCommandCommandInput = document.querySelector('#addOrEditTelegramBotCommandCommandInput');
	var addOrEditTelegramBotCommandCallBackInput = document.querySelector('#addOrEditTelegramBotCommandCallBackInput');
	var addOrEditTelegramBotCommandTextInput = document.querySelector('#addOrEditTelegramBotCommandTextInput');

	var offKeyboardRadio = document.querySelector('#offKeyboardRadio');

	var keyboard = document.querySelector('.keyboard');
	var keyboardButtons = document.querySelector('#keyboardButtons');

	var keyboardButtonNum = 0;

	var addOrEditTelegramBotCommandUrl;

	function addOrEditTelegramBotCommandTextInputInsert(value) {
		addOrEditTelegramBotCommandTextInput.value = `${addOrEditTelegramBotCommandTextInput.value}${value}`;
		addOrEditTelegramBotCommandTextInput.focus();
	}

	function createKeyboardInput(keyboardType, value) {
		let keyboardInput = document.createElement('input');
		keyboardInput.setAttribute('class', `btn btn-sm btn-outline-dark ${keyboardType}-input border-end-0`);
		keyboardInput.id = keyboardButtonNum;
		keyboardInput.type = 'text';
		keyboardInput.value = value;
		keyboardButtons.append(keyboardInput);

		let deleteKeyboardButton = document.createElement('button')
		deleteKeyboardButton.setAttribute('class', 'btn btn-sm btn-danger delete-keyboard-button');
		deleteKeyboardButton.id = keyboardButtonNum;
		deleteKeyboardButton.type = 'button';
		deleteKeyboardButton.innerHTML = '<i class="bi bi-x-lg"></i>';
		keyboardButtons.append(deleteKeyboardButton);

		deleteKeyboardButton.addEventListener('click', function() {
			keyboardInput.remove();
			this.remove();
		});

		return keyboardInput;
	}

	function keyboardButtonFunc(keyboardButton, keyboardType) {
		keyboardButton.remove();

		console.log(keyboardType)
		
		if (keyboardType == 'inline-keyboard') {
			createKeyboardInput(keyboardType, '{}:{}').focus();
		} else{
			createKeyboardInput(keyboardType, '').focus();
		}

		createKeyboardButton(keyboardType);
	}

	function createKeyboardButton(keyboardType) {
		let keyboardButton = document.createElement('button');
		keyboardButton.setAttribute('class', `btn btn-sm btn-outline-dark ${keyboardType}-button w-100`);
		keyboardButton.id = keyboardButtonNum;
		keyboardButton.type = 'button';
		keyboardButton.innerHTML = 'Добавить кнопку';
		keyboardButtons.append(keyboardButton);

		keyboardButton.addEventListener('click', () => keyboardButtonFunc(keyboardButton, keyboardType));

		keyboardButtonNum ++;
	}

	function offKeyboard() {
		if (keyboard.id != 'offKeyboard') {
			keyboard.setAttribute('class', `${keyboard.getAttribute('class')} d-none`);
			keyboard.id = 'offKeyboard';

			keyboardButtons.innerHTML = '';
		}
	}

	offKeyboardRadio.addEventListener('click', offKeyboard);

	const keyboardRadios = [
		document.querySelector('#defaultKeyboardRadio'),
		document.querySelector('#inlineKeyboardRadio'),
	];

	let examplekeyboardButton = document.querySelector('#examplekeyboardButton');

	for (let i = 0; i < keyboardRadios.length; i++) {
		keyboardRadios[i].addEventListener('click', function() {
			let keyboardType = keyboardRadios[i].id.replace('Radio', '');

			if (keyboard.id != keyboardType) {
				keyboard.setAttribute('class', keyboard.getAttribute('class').replace(' d-none', ''));
				keyboard.id = keyboardType;
				keyboardButtons.innerHTML = '';

				if (keyboardType == 'defaultKeyboard') {
					keyboardType = 'default-keyboard';

					examplekeyboardButton.innerHTML = '<b>Текст</b>';
				} else {
					keyboardType = 'inline-keyboard';

					examplekeyboardButton.innerHTML = '<b>{Текст}:{CallBack текст}</b> или <b>{Текст}:{Ссылка}</b>';
				}

				createKeyboardButton(keyboardType);
			}
		});
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
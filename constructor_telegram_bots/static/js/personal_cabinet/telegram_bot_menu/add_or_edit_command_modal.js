{
	function addOrEditTelegramBotCommandTextInputInsert(value) {
		addOrEditTelegramBotCommandTextInput.value = `${addOrEditTelegramBotCommandTextInput.value} ${value}`;
		addOrEditTelegramBotCommandTextInput.focus();
	}

	var keyboardButtonNum = 0;

	offKeybordRadio.addEventListener('click', offKeybord);

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
		
		createKeyboardInput(keyboardType, '').focus();
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
}
{
	let keyboardButtonNum = 0;

	offKeybordRadio.addEventListener('click', offKeybord);

	function keyboardButtonFunc(keyboardButton, keyboardButtonNum, keyboardType) {
		keyboardButton.outerHTML = `<input class="${keyboardButton.getAttribute('class').replace('button w-100', 'input border-end-0')}" id="${keyboardButtonNum}" type="text">`;

		let deleteKeyboardButton = document.createElement('button')
		deleteKeyboardButton.setAttribute('class', 'btn btn-sm btn-danger delete-keyboard-button');
		deleteKeyboardButton.id = keyboardButtonNum;
		deleteKeyboardButton.innerHTML = '<i class="bi bi-x-lg"></i>';
		deleteKeyboardButton.type = 'button';
		keyboardButtons.append(deleteKeyboardButton);

		let keyboardInput = document.querySelector(`.${keyboardType}-input[id="${keyboardButtonNum}"]`);
		keyboardInput.focus();

		deleteKeyboardButton.addEventListener('click', function() {
			keyboardInput.remove();
			this.remove();
		});

		createKeyboardButton(keyboardType);
	}

	function createKeyboardButton(keyboardType) {
		let keyboardButton = document.createElement('button');
		keyboardButton.setAttribute('class', `btn btn-sm btn-outline-dark ${keyboardType}-button w-100`);
		keyboardButton.id = keyboardButtonNum;
		keyboardButton.type = 'button';
		keyboardButton.innerHTML = 'Добавить кнопку';
		keyboardButtons.append(keyboardButton);

		keyboardButton.addEventListener('click', () => keyboardButtonFunc(keyboardButton, keyboardButtonNum - 1, keyboardType));

		keyboardButtonNum ++;
	}

	const keyboardRadios = [
		document.querySelector('#defaultKeyboardRadio'),
		document.querySelector('#inlineKeyboardRadio'),
	];

	for (let i = 0; i < keyboardRadios.length; i++) {
		keyboardRadios[i].addEventListener('click', function() {
			let keyboardType = keyboardRadios[i].id.replace('Radio', '');

			if (keyboard.id != keyboardType) {
				keyboard.setAttribute('class', keyboard.getAttribute('class').replace(' d-none', ''));
				keyboard.id = keyboardType;
				keyboardButtons.innerHTML = '';

				if (keyboardType == 'defaultKeyboard') {
					keyboardType = 'default-keyboard';
				} else {
					keyboardType = 'inline-keyboard';
				}

				createKeyboardButton(keyboardType);
			}
		});
	}
}
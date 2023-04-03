{
	let startOrStopTelegramBotButton = document.querySelector('#startOrStopTelegramBotButton');
	startOrStopTelegramBotButton.addEventListener('click', function() {
		let startOrStopTelegramBotButtonBackground = (this.getAttribute('class').search('danger') != -1) ? 'danger' : 'success';

		let request = new XMLHttpRequest();
		request.open('POST', (startOrStopTelegramBotButtonBackground == 'success') ? `/telegram_bot/${telegramBotId}/start/` : `/telegram_bot/${telegramBotId}/stop/`, true);
		request.onreadystatechange = checkRequestResponse(function() {
			if (request.status == 200) {
				let cardHeader = document.querySelector('.card-header');
				
				if (startOrStopTelegramBotButtonBackground == 'success') {
					cardHeader.innerHTML = 'Telegram бот включен';
					cardHeader.setAttribute('class', cardHeader.getAttribute('class').replace('danger', 'success'));
					
					startOrStopTelegramBotButton.innerHTML = 'Выключить Telegram бота';
					startOrStopTelegramBotButton.setAttribute('class', startOrStopTelegramBotButton.getAttribute('class').replace('success', 'danger'));
				} else {
					cardHeader.innerHTML = 'Telegram бот выключен';
					cardHeader.setAttribute('class', cardHeader.getAttribute('class').replace('success', 'danger'));

					startOrStopTelegramBotButton.innerHTML = 'Включить Telegram бота';
					startOrStopTelegramBotButton.setAttribute('class', startOrStopTelegramBotButton.getAttribute('class').replace('danger', 'success'));
				}

				myAlert(mainAlertPlaceholder, request.responseText, 'success');
			} else {
				myAlert(mainAlertPlaceholder, request.responseText, 'danger');
			}
		});
		request.send();
	});

	var duplicateTelegramBotModalBootstrap = new bootstrap.Modal('#duplicateTelegramBotModal');
	document.querySelector('#duplicateTelegramBotModalButton').addEventListener('click', function() {
		duplicateTelegramBotModalBootstrap.toggle();
	});

	document.querySelector('#deleteTelegramBotButton').addEventListener('click', () => askConfirmModal(
		'Удаление Telegram бота',
		'Вы точно хотите удалить Telegram бота?',
		function() {
			let request = new XMLHttpRequest();
			request.open('POST', `/telegram_bot/${telegramBotId}/delete/`, true);
			request.setRequestHeader('Content-Type', 'application/json');
			request.onreadystatechange = checkRequestResponse(function() {
				if (request.status == 200) {
					setTimeout("window.location.href = '../';", 1000);

					myAlert(mainAlertPlaceholder, request.responseText, 'success');
				} else {
					myAlert(mainAlertPlaceholder, request.responseText, 'danger');
				}
			});
			request.send();
		}
	));
}

{
	telegramBotPrivateCheckBox.addEventListener('click', function() {
		let request = new XMLHttpRequest();
		request.open('POST', `/telegram_bot/${telegramBotId}/edit/private/`, true);
		request.setRequestHeader('Content-Type', 'application/json');
		request.onreadystatechange = checkRequestResponse(function() {
			if (request.status == 200) {
				let telegramBotAllowedUserButtons = document.querySelectorAll('.telegram-bot-allowed-user-button');

				if (telegramBotPrivateCheckBox.checked) {
					for (let i = 0; i < telegramBotAllowedUserButtons.length; i++) {
						telegramBotAllowedUserButtons[i].setAttribute('class', telegramBotAllowedUserButtons[i].getAttribute('class').replace(' d-none', ''));
					}
				} else {
					for (let i = 0; i < telegramBotAllowedUserButtons.length; i++) {
						telegramBotAllowedUserButtons[i].setAttribute('class', `${telegramBotAllowedUserButtons[i].getAttribute('class')} d-none`);
					}
				}

				myAlert(mainAlertPlaceholder, request.responseText, 'success');
			} else {
				myAlert(mainAlertPlaceholder, request.responseText, 'danger');
			}
		});
		request.send(JSON.stringify(
			{
				'telegram_bot_private': this.checked,
			}
		));
	});
}

{
	let addOrEditTelegramBotCommandModalBootstrap = new bootstrap.Modal('#addOrEditTelegramBotCommandModal');

	let addOrEditTelegramBotCommandModallLabel = document.querySelector('#addOrEditTelegramBotCommandModallLabel');
	let addOrEditTelegramBotCommandModalAlertPlaceholder = document.querySelector('#addOrEditTelegramBotCommandModalAlertPlaceholder');

	let addOrEditTelegramBotCommandNameInput = document.querySelector('#addOrEditTelegramBotCommandNameInput');
	let addOrEditTelegramBotCommandCommandInput = document.querySelector('#addOrEditTelegramBotCommandCommandInput');
	let addOrEditTelegramBotCommandCallBackInput = document.querySelector('#addOrEditTelegramBotCommandCallBackInput');
	var addOrEditTelegramBotCommandTextInput = document.querySelector('#addOrEditTelegramBotCommandTextInput');

	var offKeyboardRadio = document.querySelector('#offKeyboardRadio')

	var keyboard = document.querySelector('.keyboard');
	var keyboardButtons = document.querySelector('#keyboardButtons');

	let addOrEditTelegramBotCommandButton = document.querySelector('#addOrEditTelegramBotCommandButton');

	function offKeyboard() {
		if (keyboard.id != 'offKeyboard') {
			keyboard.setAttribute('class', `${keyboard.getAttribute('class')} d-none`);
			keyboard.id = 'offKeyboard';

			keyboardButtons.innerHTML = '';
		}
	}

	var addOrEditTelegramBotCommandUrl;
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

	document.querySelector('#addTelegramBotCommandModalButton').addEventListener('click', function() {
		addOrEditTelegramBotCommandModallLabel.innerHTML = 'Добавление команды';

		addOrEditTelegramBotCommandNameInput.value = '';
		addOrEditTelegramBotCommandCommandInput.value = '';
		addOrEditTelegramBotCommandCallBackInput.value = '';
		addOrEditTelegramBotCommandTextInput.value = '';

		offKeyboard();
		offKeyboardRadio.checked = true;

		addOrEditTelegramBotCommandUrl = `/telegram_bot/${telegramBotId}/command/add/`;

		addOrEditTelegramBotCommandButton.innerHTML = 'Добавить команду';
		addOrEditTelegramBotCommandButton.removeEventListener('click', addOrEditTelegramBotCommand);
		addOrEditTelegramBotCommandButton.addEventListener('click', addOrEditTelegramBotCommand);

		addOrEditTelegramBotCommandModalBootstrap.toggle();
	});

	function editTelegramBotCommandButton() {
		let telegramBotCommandId = this.id;

		let request = new XMLHttpRequest();
		request.open('POST', `/telegram_bot/${telegramBotId}/get_command_data/${telegramBotCommandId}/`, true);
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

					keyboard.setAttribute('class', keyboard.getAttribute('class').replace(' d-none', ''));
					keyboard.id = telegramBotCommandKeyboard[0];
					keyboardButtons.innerHTML = '';
					
					let keyboardType = (telegramBotCommandKeyboard[0] == 'defaultKeyboard') ? 'default-keyboard' : 'inline-keyboard';

					examplekeyboardButton.innerHTML = (keyboardType == 'defaultKeyboard') ? '<b>{Текст}:{CallBack текст}</b> или <b>{Текст}:{Ссылка}</b>' : '<b>Текст</b>';

					for (let i = 0; i < telegramBotCommandKeyboard.length; i ++) {
						if (i > 0) {
							createKeyboardInput(keyboardType, telegramBotCommandKeyboard[i]);

							keyboardButtonNum ++;
						}
					}

					createKeyboardButton(keyboardType);
				}

				addOrEditTelegramBotCommandUrl = `/telegram_bot/${telegramBotId}/command/${telegramBotCommandId}/edit/`;

				addOrEditTelegramBotCommandButton.innerHTML = 'Редактировать команду';
				addOrEditTelegramBotCommandButton.removeEventListener('click', addOrEditTelegramBotCommand);
				addOrEditTelegramBotCommandButton.addEventListener('click', addOrEditTelegramBotCommand);

				addOrEditTelegramBotCommandModalBootstrap.toggle();
			}
		});
		request.send();
	}
}
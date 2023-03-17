const telegramBotId = window.location.href.split('/')[4]
const mainAlertPlaceholder = document.querySelector('#mainAlertPlaceholder');

const telegramBotPrivateCheckBox = document.querySelector('#telegramBotPrivateCheckBox');

get_telegram_bot_commands();
function get_telegram_bot_commands() {
	let request = new XMLHttpRequest();
	request.open('POST', `/telegram_bot/${telegramBotId}/get_commands/`, true);
	request.setRequestHeader('Content-Type', 'application/json');
	request.onreadystatechange = checkRequestResponse(function() {
		if (request.status == 200) {
			let telegramBotCommandsDiv = document.querySelector('.telegram-bot-commands');
			telegramBotCommandsDiv.innerHTML = '';

			let telegramBotCommands = JSON.parse(request.responseText);
			let telegramBotCommandsKeys = Object.keys(telegramBotCommands);

			if (telegramBotCommandsKeys.length > 0) {
				for (let i = 0; i < telegramBotCommandsKeys.length; i++) {
					let wrapper = document.createElement('div');
					wrapper.setAttribute('class', 'list-group-item pb-1');
					wrapper.innerHTML = [
						'<div class="row justify-content-between">',
						'	<div class="col-auto">',
						`		<p class="my-2">${telegramBotCommands[telegramBotCommandsKeys[i]]}</p>`,
						'	</div>',
						'	<div class="col-auto">',
						`		<button class="btn delete-command-button rounded-0 p-0" id="${telegramBotCommandsKeys[i]}" type="button" data-bs-toggle="tooltip" data-bs-placement="bottom" title="Удалить команду">`,
						'			<i class="bi bi-trash text-danger" style="font-size: 1.5rem;"></i>',
						'		</button>',
						`		<button class="btn edit-command-button rounded-0 p-0" id="${telegramBotCommandsKeys[i]}" type="button" data-bs-toggle="tooltip" data-bs-placement="bottom" title="Редактировать команду">`,
						'			<i class="bi bi-pencil-square text-secondary" style="font-size: 1.5rem;"></i>',
						'		</button>',
						'	</div>',
						'</div>',
					].join('');
					telegramBotCommandsDiv.append(wrapper);
				}
			} else {
				let wrapper = document.createElement('div');
				wrapper.setAttribute('class', 'list-group-item pb-1');
				wrapper.innerHTML = `<p class="my-2">Вы ещё не добавили команды Telegram боту</p>`;
				telegramBotCommandsDiv.append(wrapper);
			}
		}
	});
	request.send();
}

get_telegram_bot_users();
function get_telegram_bot_users() {
	let request = new XMLHttpRequest();
	request.open('POST', `/telegram_bot/${telegramBotId}/get_users/`, true);
	request.setRequestHeader('Content-Type', 'application/json');
	request.onreadystatechange = checkRequestResponse(function() {
		if (request.status == 200) {
			let telegramBotUsersDiv = document.querySelector('.telegram-bot-users');
			telegramBotUsersDiv.innerHTML = '';

			let telegramBotUsers = JSON.parse(request.responseText);
			let telegramBotUsersKeys = Object.keys(telegramBotUsers);

			if (telegramBotUsersKeys.length > 0) {
				for (let i = 0; i < telegramBotUsersKeys.length; i++) {
					let wrapper = document.createElement('tr');
					wrapper.setAttribute('class', 'text-center');
					wrapper.innerHTML = [
						`<th class="align-middle" scope="row">${i + 1}</th>`,
						`<td class="align-middle">@${telegramBotUsers[telegramBotUsersKeys[i]]['username']}</td>`,
						`<td class="align-middle">${telegramBotUsers[telegramBotUsersKeys[i]]['date_started']}</td>`,
						'<td class="align-middle">',
						'	<button class="btn rounded-0 p-0" type="button" data-bs-toggle="tooltip" data-bs-placement="bottom" title="Удалить пользователя">',
						'		<i class="bi bi-trash text-danger" style="font-size: 1.5rem;"></i>',
						'	</button>',
						`	<button class="btn rounded-0 p-0 ${(telegramBotPrivateCheckBox.checked) ? '' : 'd-none'}" id="giveUserAccessButton" type="button" data-bs-toggle="tooltip" data-bs-placement="bottom" title="Дать пользователю доступ к Telegram боту">`,
						'		<i class="bi bi-star text-warning" style="font-size: 1.5rem;"></i>',
						'	</button>',
						'</td>',
					].join('');
					telegramBotUsersDiv.append(wrapper);
				}
			} else {
				telegramBotUsersDiv.innerHTML = '<p>Вашего Telegram бота ещё никто не активировал</p>';
			}
		}
	});
	request.send();
}

{
	let startOrStopTelegramBotButton = document.querySelector('#startOrStopTelegramBotButton');
	startOrStopTelegramBotButton.addEventListener('click', function() {
		let startOrStopTelegramBotButtonBackground = this.getAttribute('class');
		
		if (startOrStopTelegramBotButtonBackground.search('danger') != -1) {
			startOrStopTelegramBotButtonBackground = 'danger';
		} else {
			startOrStopTelegramBotButtonBackground = 'success';
		}

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
		duplicateTelegramBotModalBootstrap.toggle()
	});

	document.querySelector('#deleteTelegramBotButton').addEventListener('click', function() {
		let request = new XMLHttpRequest();
		request.open('POST', `/telegram_bot/${telegramBotId}/delete/`, true);
		request.onreadystatechange = checkRequestResponse(function() {
			if (request.status == 200) {
				setTimeout("window.location.href = '../';", 1000);

				myAlert(mainAlertPlaceholder, request.responseText, 'success');
			} else {
				myAlert(mainAlertPlaceholder, request.responseText, 'danger');
			}
		});
		request.send();
	});
}

{
	telegramBotPrivateCheckBox.addEventListener('click', function() {
		let request = new XMLHttpRequest();
		request.open('POST', `/telegram_bot/${telegramBotId}/edit/private/`, true);
		request.setRequestHeader('Content-Type', 'application/json');
		request.onreadystatechange = checkRequestResponse(function() {
			if (request.status == 200) {
				let giveUserAccessButtons = document.querySelectorAll('#giveUserAccessButton');

				if (telegramBotPrivateCheckBox.checked) {
					for (let i = 0; i < giveUserAccessButtons.length; i++) {
						giveUserAccessButtons[i].setAttribute('class', giveUserAccessButtons[i].getAttribute('class').replace(' d-none', ''));
					}
				} else {
					for (let i = 0; i < giveUserAccessButtons.length; i++) {
						giveUserAccessButtons[i].setAttribute('class', `${giveUserAccessButtons[i].getAttribute('class')} d-none`);
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
	let addOrEditTelegramBotCommandTextInput = document.querySelector('#addOrEditTelegramBotCommandTextInput');
	let addOrEditTelegramBotCommandEditLastMessageCheckBox = document.querySelector('#addOrEditTelegramBotCommandEditLastMessageCheckBox');

	var offKeybordRadio = document.querySelector('#offKeybordRadio')

	var keyboard = document.querySelector('.keyboard');
	var keyboardButtons = document.querySelector('#keyboardButtons');

	function offKeybord() {
		if (keyboard.id != 'offKeybord') {
			keyboard.setAttribute('class', `${keyboard.getAttribute('class')} d-none`);
			keyboard.id = 'offKeybord';

			keyboardButtons.innerHTML = '';
		}
	}

	function addOrEditTelegramBotCommand(url) {
		let telegramBotCommandKeyboard = [keyboard.id];

		let telegramBotCommandKeyboardButtons = keyboardButtons.querySelectorAll('input');
		for (let i = 0; i < telegramBotCommandKeyboardButtons.length; i ++) {
			telegramBotCommandKeyboard.push(telegramBotCommandKeyboardButtons[i].value);
		}

		let request = new XMLHttpRequest();
		request.open('POST', url, true);
		request.setRequestHeader('Content-Type', 'application/json');
		request.onreadystatechange = checkRequestResponse(function() {
			if (request.status == 200) {
				get_telegram_bot_commands()

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
				'is_edit_last_message': addOrEditTelegramBotCommandEditLastMessageCheckBox.checked,
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
		addOrEditTelegramBotCommandEditLastMessageCheckBox.checked = false;

		offKeybord();
		offKeybordRadio.checked = true;
		
		document.querySelector('#addTelegramBotCommandButton').addEventListener('click', function() {
			addOrEditTelegramBotCommand(`/telegram_bot/${telegramBotId}/command/add/`)
		});
		
		addOrEditTelegramBotCommandModalBootstrap.toggle();
	});
}
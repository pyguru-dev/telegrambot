{
    var telegramBotIsPrivateCheckBox = document.querySelector('#telegramBotIsPrivateCheckBox');

    telegramBotIsPrivateCheckBox.addEventListener('click', function() {
        let request = new XMLHttpRequest();
        request.open('POST', `/telegram-bot/${telegramBotId}/edit/`, true);
        request.setRequestHeader('Content-Type', 'application/json');
        request.onreadystatechange = checkRequestResponse(function() {
            let telegramBotAllowedUserButtons = document.querySelectorAll('.telegram-bot-allowed-user-button');

            if (telegramBotIsPrivateCheckBox.checked) {
                for (let i = 0; i < telegramBotAllowedUserButtons.length; i++) {
                    telegramBotAllowedUserButtons[i].classList.remove('d-none');
                }
            } else {
                for (let i = 0; i < telegramBotAllowedUserButtons.length; i++) {
                    telegramBotAllowedUserButtons[i].classList.add('d-none');
                }
            }

            myAlert(mainAlertPlaceholder, request.responseText, 'success');
        });
        request.send(JSON.stringify(
            {
                'is_private': this.checked,
            }
        ));
    });
}

{
	let startOrStopTelegramBotButton = document.querySelector('#startOrStopTelegramBotButton');
	startOrStopTelegramBotButton.addEventListener('click', function() {
		this.disabled = true;

		let request = new XMLHttpRequest();
		request.open('POST', (telegramBotIsRunning) ? `/telegram-bot/${telegramBotId}/stop/` : `/telegram-bot/${telegramBotId}/start/`, true);
		request.onreadystatechange = checkRequestResponse(function() {
			if (request.status == 200) {
				let cardHeader = document.querySelector('.card-header');

				if (telegramBotIsRunning) {
					telegramBotIsRunning = false;

					clearInterval(setIntervalId)

					cardHeader.innerHTML = 'Telegram бот выключен';
					cardHeader.classList.replace('bg-success', 'bg-danger');

					startOrStopTelegramBotButton.innerHTML = 'Включить Telegram бота';
					startOrStopTelegramBotButton.classList.replace('btn-danger', 'btn-success');
				} else {
					telegramBotIsRunning = true;

					getTelegramBotUsers();
					setIntervalId = setInterval(getTelegramBotUsers, 1500);

					cardHeader.innerHTML = 'Telegram бот включен';
					cardHeader.classList.replace('bg-danger', 'bg-success');
					
					startOrStopTelegramBotButton.innerHTML = 'Выключить Telegram бота';
					startOrStopTelegramBotButton.classList.replace('btn-success', 'btn-danger');
				}

				startOrStopTelegramBotButton.disabled = false;

				myAlert(mainAlertPlaceholder, request.responseText, 'success');
			} else {
				myAlert(mainAlertPlaceholder, request.responseText, 'danger');
			}
		});
		request.send();
	});

	document.querySelector('#deleteTelegramBotButton').addEventListener('click', () => askConfirmModal(
		'Удаление Telegram бота',
		'Вы точно хотите удалить Telegram бота?',
		function() {
			let request = new XMLHttpRequest();
			request.open('POST', `/telegram-bot/${telegramBotId}/delete/`, true);
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
	let addOrEditTelegramBotCommandButton = document.querySelector('#addOrEditTelegramBotCommandButton');
	document.querySelector('#addTelegramBotCommandModalButton').addEventListener('click', function() {
		addOrEditTelegramBotCommandModallLabel.innerHTML = 'Добавление команды';

		addOrEditTelegramBotCommandNameInput.value = '';
		addOrEditTelegramBotCommandCommandInput.value = '';
		addOrEditTelegramBotCommandCallBackInput.value = '';
		addOrEditTelegramBotCommandTextInput.value = '';

		offKeyboard();
		offKeyboardRadio.checked = true;

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

					examplekeyboardButton.innerHTML = (telegramBotCommandKeyboard[0] == 'defaultKeyboard') ? '<b>{Текст}:{CallBack текст}</b> или <b>{Текст}:{Ссылка}</b>' : '<b>Текст</b>';

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
}
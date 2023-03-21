const telegramBotId = window.location.href.split('/')[4];
const mainAlertPlaceholder = document.querySelector('#mainAlertPlaceholder');

const telegramBotPrivateCheckBox = document.querySelector('#telegramBotPrivateCheckBox');

function getTelegramBotCommands() {
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
						`		<button class="btn delete-telegram-bot-command-button rounded-0 p-0" id="${telegramBotCommandsKeys[i]}" type="button" data-bs-toggle="tooltip" data-bs-placement="bottom" title="Удалить команду">`,
						'			<i class="bi bi-trash text-danger" style="font-size: 1.5rem;"></i>',
						'		</button>',
						`		<button class="btn edit-telegram-bot-command-button rounded-0 p-0" id="${telegramBotCommandsKeys[i]}" type="button" data-bs-toggle="tooltip" data-bs-placement="bottom" title="Редактировать команду">`,
						'			<i class="bi bi-pencil-square text-secondary" style="font-size: 1.5rem;"></i>',
						'		</button>',
						'	</div>',
						'</div>',
					].join('');
					telegramBotCommandsDiv.append(wrapper);

					document.querySelector(`.delete-telegram-bot-command-button[id="${telegramBotCommandsKeys[i]}"]`).addEventListener('click', () => askConfirmModal('Удаление команды Telegram бота', 'Вы точно хотите удалить команду Telegram бота?', function() {
						let telegramBotCommandId = telegramBotCommandsKeys[i];

						deleteTelegramBotCommandButton(telegramBotCommandId);
					}));
					document.querySelector(`.edit-telegram-bot-command-button[id="${telegramBotCommandsKeys[i]}"]`).addEventListener('click', editTelegramBotCommandButton);
				}
			} else {
				let wrapper = document.createElement('div');
				wrapper.setAttribute('class', 'list-group-item pb-1');
				wrapper.innerHTML = `<p class="my-2">Вы ещё не добавили команды Telegram боту.</p>`;
				telegramBotCommandsDiv.append(wrapper);
			}
		}
		
		getTelegramBotUsers();
	});
	request.send();
}

function getTelegramBotUsers() {
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
				let wrapper = document.createElement('tr');
				wrapper.innerHTML = '<p class="ps-1 pt-0">Вашего Telegram бота ещё никто не активировал.</p>';
				telegramBotUsersDiv.append(wrapper);
			}
		}
	});
	request.send();
}

getTelegramBotCommands();
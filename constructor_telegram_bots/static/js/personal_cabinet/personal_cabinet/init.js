function get_telegram_bots() {
	fetch(getTelegramBotsUrl, {
		method: 'POST',
	}).then(response => {
		if (response.ok) {
			response.json().then(telegramBots => {
				let telegramBotsDiv = document.querySelector('#telegramBots');
				telegramBotsDiv.innerHTML = '';

				if (telegramBots.length > 0) {
					telegramBots.forEach(telegramBot => {
						let telegramBotDiv = document.createElement('div');
						telegramBotDiv.setAttribute('class', 'col py-2');
						telegramBotDiv.innerHTML = [
							'<div class="card h-100">',
							`	<h5 class="card-header bg-${(telegramBot['is_running'] == true) ? 'success' : 'danger'} text-light text-center fw-bold">Telegram бот ${(telegramBot['is_running'] == true) ? 'включен' : 'выключен'}</h5>`,
							'	<div class="card-body p-2">',
							'		<table class="table table-sm table-borderless mb-0">',
							'			<tbody>',
							'				<tr>',
							'					<th class="align-middle" scope="row">Имя:</th>',
							'					<td class="text-break">',
							`						<a class="link-dark text-decoration-none" href="tg://resolve?domain=${telegramBot['name']}">@${telegramBot['name']}</a>`,
							'					</td>',
							'				</tr>',
							'				<tr>',
							'					<th class="align-middle" scope="row">API-токен:</td>',
							`					<td class="text-break">${telegramBot['api_token']}</td>`,
							'				</tr>',
							'				<tr>',
							'					<th scope="row">Количество активаций:</th>',
							`					<td class="align-middle">${telegramBot['users_count']}</td>`,
							'				</tr>',
							'				<tr>',
							'					<th scope="row">Количество команд:</th>',
							`					<td class="align-middle">${telegramBot['commands_count']}</td>`,
							'				</tr>',
							'				<tr>',
							'					<th scope="row">Дата добавления:</th>',
							`					<td class="align-middle">${telegramBot['date_added']}</td>`,
							'				</tr>',
							'			</tbody>',
							'		</table>',
							'	</div>',
							` <a class="card-footer btn btn-light" href="/personal-cabinet/${telegramBot['id']}/">Меню Telegram бота</a>`,
							'</div>',
						].join('');
						telegramBotsDiv.append(telegramBotDiv);
					});
				} else {
					let telegramBotDiv = document.createElement('div');
					telegramBotDiv.setAttribute('class', 'col py-2');
					telegramBotDiv.innerHTML = [
						'<div class="card h-100">',
						'	<div class="card-body">',
						`		<h5 class="text-center text-break mb-0">Вы ещё не добавили Telegram бота</h5>`,
						'	</div>',
						`	<button class="card-footer btn btn-light" type="button" data-bs-toggle="modal" data-bs-target="#howToAddTelegramBotModal">Как добавить Telegram бота?</button>`,
						'</div>',
					].join('');
					telegramBotsDiv.append(telegramBotDiv);
				}
			});
		} else {
			response.text().then(responseText => myAlert(mainAlertPlaceholder, responseText, 'danger'));
		}
	});
}

get_telegram_bots();

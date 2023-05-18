function get_telegram_bots() {
	let request = new XMLHttpRequest();
	request.open('POST', getUserTelegramBotsUrl, true);
	request.setRequestHeader('Content-Type', 'application/json');
	request.onreadystatechange = checkRequestResponse(function() {
		if (request.status == 200) {
			let telegramBotsDiv = document.querySelector('#telegramBots');
			telegramBotsDiv.innerHTML = '';

			let telegramBots = JSON.parse(request.responseText);
			
			if (telegramBots.length > 0) {
				for (let i = 0; i < telegramBots.length; i++) {
					let telegramBot = telegramBots[i]

					let cardHeaderBackgroundColor = (telegramBot['is_running'] == true) ? 'success' : 'danger';
					let cardHeaderText = `Telegram бот ${(telegramBot['is_running'] == true) ? 'включен' : 'выключен'}`;

					let wrapper = document.createElement('div');
					wrapper.setAttribute('class', 'col py-2');
					wrapper.innerHTML = [
						'<div class="card h-100">',
						`	<h5 class="card-header bg-${cardHeaderBackgroundColor} text-light text-center fw-bold">${cardHeaderText}</h5>`,
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
						` <a class="card-footer btn btn-light" href="/personal-cabinet/${telegramBots[i]['id']}/">Меню Telegram бота</a>`,
						'</div>',
					].join('');
					telegramBotsDiv.append(wrapper);
				}
			} else {
				let wrapper = document.createElement('div');
				wrapper.setAttribute('class', 'col py-2');
				wrapper.innerHTML = [
					'<div class="card h-100">',
					'	<div class="card-body">',
					`		<h5 class="text-center text-break mb-0">Вы ещё не добавили Telegram бота</h5>`,
					'	</div>',
					`	<button class="card-footer btn btn-light" type="button" data-bs-toggle="modal" data-bs-target="#howToAddTelegramBotModal">Как добавить Telegram бота?</button>`,
					'</div>',
				].join('');
				telegramBotsDiv.append(wrapper);
			}
		}
	});
	request.send();
}

get_telegram_bots();
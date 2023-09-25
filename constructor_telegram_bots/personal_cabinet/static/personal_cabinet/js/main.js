{
	const telegramBotsDiv = document.querySelector('#telegramBots');

	function addTelegramBot(telegramBot) {
		const telegramBotDiv = document.createElement('div');
		telegramBotDiv.classList = 'col';
		telegramBotDiv.innerHTML = [
			'<div class="card border">',
			`	<h5 class="card-header bg-${(telegramBot.is_running) ? 'success' : 'danger'} border-0 fw-semibold text-light text-center">${(telegramBot.is_running) ? telegramBotCardHeaderIsRunningText : telegramBotCardHeaderIsNotRunningText}</h5>`,
			'	<div class="card-body p-2">',
			'		<table class="table table-borderless mb-0">',
			'			<tbody>',
			'				<tr>',
			`					<th class="align-middle text-nowrap" scope="row">@username:</th>`,
			'					<td class="text-break">',
			`						<a class="link-dark link-underline link-underline-opacity-0" href="tg://resolve?domain=${telegramBot.username}">@${telegramBot.username}</a>`,
			'					</td>',
			'				</tr>',
			'				<tr>',
			`					<th class="align-middle text-nowrap" scope="row">${telegramBotTableLineApiTokenText}:</td>`,
			`					<td class="text-break">${telegramBot.api_token}</td>`,
			'				</tr>',
			'				<tr>',
			`					<th class="text-nowrap" scope="row">${telegramBotTableLineIsPrivateText}:</td>`,
			`					<td>${(telegramBot.is_private) ? '<i class="bi bi-check-circle-fill text-success"></i>' : '<i class="bi bi-x-circle-fill text-danger"></i>'}</td>`,
			'				</tr>',
			'				<tr>',
			`					<th class="align-middle text-nowrap" scope="row">${telegramBotTableLineDateAddedText}:</th>`,
			`					<td class="text-break">${telegramBot.added_date}</td>`,
			'				</tr>',
			'			</tbody>',
			'		</table>',
			'	</div>',
			'	<div class="card-footer border-top p-0">',
			`		<a class="btn btn-light border-0 rounded-top-0 w-100 pt-2" href="/telegram-bot-menu/${telegramBot.id}/" style="height: 42px;">${telegramBotCardFooterPersonalCabinetButtonText}</a>`,
			'	</div>',
			'</div>',
		].join('');
		telegramBotsDiv.appendChild(telegramBotDiv);
	}

	fetch(telegramBotsUrl, {
		method: 'GET',
		headers: {'Authorization': `Token ${userApiToken}`},
	}).then(response => {
		if (response.ok) {
			response.json().then(telegramBots => {
				telegramBotsDiv.innerHTML = '';

				if (telegramBots.length == 0) {
					const telegramBotDiv = document.createElement('div');
					telegramBotDiv.classList = 'col';
					telegramBotDiv.id = 'notAddedTelegramBot';
					telegramBotDiv.innerHTML = `<div class="border rounded text-center p-3">${telegramBotCardBodyNotAddedText}</div>`;
					telegramBotsDiv.appendChild(telegramBotDiv);
				} else {
					telegramBots.forEach(telegramBot => addTelegramBot(telegramBot));
				}
			});
		}
	});
}
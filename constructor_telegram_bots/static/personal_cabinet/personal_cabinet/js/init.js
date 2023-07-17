{
	const telegramBotsDiv = document.querySelector('#telegramBots');

	function addTelegramBot(telegramBot) {
		const telegramBotDiv = document.createElement('div');
		telegramBotDiv.classList = 'col';
		telegramBotDiv.innerHTML = [
			'<div class="card border h-100">',
			`	<h5 class="card-header border-0 bg-${(telegramBot['is_running']) ? 'success' : 'danger'} text-light text-center fw-bold">${(telegramBot['is_running']) ? telegramBotCardHeaderIsRunningText : telegramBotCardHeaderIsNotRunningText}</h5>`,
			'	<div class="card-body p-2">',
			'		<table class="table table-sm table-borderless mb-0">',
			'			<tbody>',
			'				<tr>',
			`					<th class="align-middle" scope="row">@username:</th>`,
			'					<td class="text-break">',
			`						<a class="link-dark text-decoration-none" href="tg://resolve?domain=${telegramBot['username']}">@${telegramBot['username']}</a>`,
			'					</td>',
			'				</tr>',
			'				<tr>',
			`					<th class="align-middle" scope="row">${telegramBotTableLineApiTokenText}:</td>`,
			`					<td class="text-break">${telegramBot['api_token']}</td>`,
			'				</tr>',
			'				<tr>',
			`					<th scope="row">${telegramBotTableLineUsersCountText}:</th>`,
			`					<td class="align-middle">${telegramBot['users_count']}</td>`,
			'				</tr>',
			'				<tr>',
			`					<th scope="row">${telegramBotTableLineCommandsCountText}:</th>`,
			`					<td class="align-middle">${telegramBot['commands_count']}</td>`,
			'				</tr>',
			'				<tr>',
			`					<th scope="row">${telegramBotTableLineDateAddedText}:</th>`,
			`					<td class="align-middle">${telegramBot['date_added']}</td>`,
			'				</tr>',
			'			</tbody>',
			'		</table>',
			'	</div>',
			'	<div class="card-footer border-top p-0">',
			`		<a class="btn btn-light border-0 rounded-top-0 w-100 pt-2" href="/personal-cabinet/${telegramBot['id']}/" style="height: 42px;">${telegramBotCardFooterPersonalCabinetButtonText}</a>`,
			'	</div>',
			'</div>',
		].join('');
		telegramBotsDiv.append(telegramBotDiv);
	}

	const updateTelegramBots = () => {
		fetch(getTelegramBotsUrl, {
			method: 'POST',
			headers: {'Authorization': `Token ${userApiToken}`},
		}).then(response => {
			if (response.ok) {
				response.json().then(telegramBots => {
					telegramBotsDiv.innerHTML = '';

					if (telegramBots.length == 0) {
						const telegramBotDiv = document.createElement('div');
						telegramBotDiv.classList = 'col';
						telegramBotDiv.id = 'notAddedTelegramBot';
						telegramBotDiv.innerHTML = [
							'<div class="card border h-100">',
							'	<div class="card-body">',
							`		<h5 class="text-center text-break mb-0">${telegramBotCardBodyNotAddedText}</h5>`,
							'	</div>',
							'	<div class="card-footer border-top p-0">',
							`		<button class="btn btn-light border-0 rounded-top-0 w-100" type="button" style="height: 42px;" data-bs-toggle="modal" data-bs-target="#howToAddTelegramBotModal">${telegramBotCardFooterHowToAddButtonText}</button>`,
							'	</div>',
							'</div>',
						].join('');
						telegramBotsDiv.append(telegramBotDiv);
					} else {
						telegramBots.forEach(telegramBot => addTelegramBot(telegramBot));
					}
				});
			}
		});
	}

	updateTelegramBots();
}
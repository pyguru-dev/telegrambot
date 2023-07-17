{
	const telegramBotPluginsLogsDiv = document.querySelector('#telegramBotPluginsLogs');

	const updateTelegramBotPluginsLogs = () => {
		fetch(telegramBotPluginsLogs, {
			method: 'GET',
			headers: {'Authorization': `Token ${userApiToken}`},
		}).then(response => {
			response.json().then(jsonResponse => {
				if (response.ok) {
					telegramBotPluginsLogsDiv.innerHTML = '';

					if (jsonResponse.length > 0) {
						jsonResponse.forEach(telegramBotPluginLog => {
							const telegramBotPluginLogDiv = document.createElement('div');
							telegramBotPluginLogDiv.classList = 'list-group-item telegram-bot-plugin p-3';
							telegramBotPluginLogDiv.innerHTML = `<p class="m-0">[<span class="text-success-emphasis">${telegramBotPluginLog['date_added']}</span>]: <span class="text-primary">${telegramBotPluginLog['plugin_name']}</span> - <span class="text-${telegramBotPluginLog['level']}">${telegramBotPluginLog['message']}</span></p>`;
							telegramBotPluginsLogsDiv.append(telegramBotPluginLogDiv);
						});
					} else {
						const telegramBotNotHavePluginsLogsDiv = document.createElement('div');
						telegramBotNotHavePluginsLogsDiv.classList = 'list-group-item telegram-bot-plugin p-3 ps-2';
						telegramBotNotHavePluginsLogsDiv.innerHTML = `<p class="text-center m-0">${telegramBotNotHavePluginsLogsText}</p>`;
						telegramBotPluginsLogsDiv.append(telegramBotNotHavePluginsLogsDiv);
					}
				} else {createAlert(mainAlertContainer, jsonResponse['message'], jsonResponse['level'])}
			});
		});
	}

	updateTelegramBotPluginsLogs();

	const telegramBotPluginsLogsСollapseButton = document.querySelector('#telegramBotPluginsLogsСollapseButton');
	const updateTelegramBotPluginsLogsButton = document.querySelector('#updateTelegramBotPluginsLogsButton');
	const telegramBotPluginsLogsBootstrapСollapse = new bootstrap.Collapse('#telegramBotPluginsLogsСollapse');

	telegramBotPluginsLogsСollapseButton.addEventListener('click', function() {
		updateTelegramBotPluginsLogsButton.classList.toggle('disabled');
		telegramBotPluginsLogsСollapseButton.innerHTML = (telegramBotPluginsLogsСollapseButton.querySelector('i').classList.contains('bi-arrow-up')) ? '<i class="bi bi-arrow-down d-flex" style="font-size: 20px;"></i>' : '<i class="bi bi-arrow-up d-flex" style="font-size: 20px;"></i>';
		telegramBotPluginsLogsBootstrapСollapse.toggle();
	});
	updateTelegramBotPluginsLogsButton.addEventListener('click', () => updateTelegramBotPluginsLogs());
}
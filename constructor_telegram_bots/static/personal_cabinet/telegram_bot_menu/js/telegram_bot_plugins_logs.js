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
						telegramBotNotHavePluginsLogsDiv.classList = 'list-group-item telegram-bot-plugin text-center p-3';
						telegramBotNotHavePluginsLogsDiv.innerHTML = telegramBotNotHavePluginsLogsText;
						telegramBotPluginsLogsDiv.append(telegramBotNotHavePluginsLogsDiv);
					}
				} else {
					createToast(jsonResponse['message'], jsonResponse['level']);
				}
			});
		});
	}

	updateTelegramBotPluginsLogs();

	const telegramBotPluginsLogsСollapseButton = document.querySelector('#telegramBotPluginsLogsСollapseButton');
	const updateTelegramBotPluginsLogsButton = document.querySelector('#updateTelegramBotPluginsLogsButton');
	const telegramBotPluginsLogsBootstrapСollapse = new bootstrap.Collapse('#telegramBotPluginsLogsСollapse');

	telegramBotPluginsLogsСollapseButton.addEventListener('click', function() {
		updateTelegramBotPluginsLogsButton.classList.toggle('disabled');
		telegramBotPluginsLogsBootstrapСollapse.toggle();

		if (telegramBotPluginsLogsСollapseButton.querySelector('i').classList.contains('bi-arrow-up')) {
			telegramBotPluginsLogsСollapseButton.innerHTML = '<i class="bi bi-arrow-down d-flex" style="font-size: 20px;"></i>';
		} else {
			telegramBotPluginsLogsСollapseButton.innerHTML = '<i class="bi bi-arrow-up d-flex" style="font-size: 20px;"></i>';
		}
	});
	updateTelegramBotPluginsLogsButton.addEventListener('click', () => updateTelegramBotPluginsLogs());
}
function get_added_telegram_bots() {
	let request = new XMLHttpRequest();
	request.open('POST', '/user/get-added-telegram-bots/', true);
	request.setRequestHeader('Content-Type', 'application/json');
	request.onreadystatechange = checkRequestResponse(function() {
		if (request.status == 200) {
			let addedTelegramBotsDiv = document.querySelector('#addedTelegramBots');
			addedTelegramBotsDiv.innerHTML = '';

			let addedTelegramBots = JSON.parse(request.responseText);
			let addedTelegramBotsKeys = Object.keys(addedTelegramBots);
			
			if (addedTelegramBotsKeys.length > 0) {
				for (let i = 0; i < addedTelegramBotsKeys.length; i++) {
					let cardHeaderBackgroundColor = (addedTelegramBots[addedTelegramBotsKeys[i]]['is_running'] == true) ? 'success' : 'danger';
					let cardHeaderText = (addedTelegramBots[addedTelegramBotsKeys[i]]['is_running'] == true) ? 'Telegram бот включен' : 'Telegram бот выключен';

					let wrapper = document.createElement('div');
					wrapper.setAttribute('class', 'col py-2');
					wrapper.innerHTML = [
						'<div class="card h-100">',
						`	<h5 class="card-header bg-${cardHeaderBackgroundColor} text-light text-center fw-bold">${cardHeaderText}</h5>`,
						'	<div class="card-body">',
						'		<table class="w-100 h-100">',
						'			<tbody>',
						'				<tr>',
						'					<td class="align-middle text-center">',
						`						<a class="h5 link-dark text-break text-decoration-none" href="tg://resolve?domain=${addedTelegramBots[addedTelegramBotsKeys[i]]['name']}">@${addedTelegramBots[addedTelegramBotsKeys[i]]['name']}</a>`,
						'					</td>',
						'				</tr>',
						'			</tbody>',
						'		</table>',
						'	</div>',
						'	<div class="card-footer">',
						`		<a class="btn btn-outline-dark w-100 my-2" href="/personal-cabinet/${addedTelegramBotsKeys[i]}/">Меню Telegram бота</a>`,
						'	</div>',
						'</div>',
					].join('');
					addedTelegramBotsDiv.append(wrapper);
				}
			} else {
				let wrapper = document.createElement('div');
				wrapper.setAttribute('class', 'col py-2');
				wrapper.innerHTML = [
					'<div class="card h-100">',
					'	<div class="card-body">',
					`		<h5 class="text-center text-break mb-0">Вы ещё не добавили Telegram бота</h5>`,
					'	</div>',
					'	<div class="card-footer">',
					`		<button class="btn btn-outline-dark w-100 my-2" id="howToAddTelegramBotModalButton" type="button">Как добавить Telegram бота?</button>`,
					'	</div>',
					'</div>',
				].join('');
				addedTelegramBotsDiv.append(wrapper);

				document.querySelector('#howToAddTelegramBotModalButton').addEventListener('click', function() {

				});
			}
		}
	});
	request.send();
}

get_added_telegram_bots();
{
	const diagram = document.querySelector('#diagram');
	const diagramSvg = document.querySelector('#diagramSvg');

	const diagramZoomPercent = document.querySelector('#diagramZoomPercent');
	let diagramCurrentScaleNum = Math.floor(diagramCurrentScale * 10 - 10);

	let selectedDiagramBlockConnector = null;

	const diagramSetZoom = () => {
		diagramZoomPercent.innerHTML = `${Math.floor(100 * diagramCurrentScale)}%`;

		document.querySelectorAll('.diagram-block').forEach(diagramBlock => diagramBlock.style.transform = `scale(${diagramCurrentScale})`);
		document.querySelectorAll('.diagram-block-connector-line').forEach(diagramBlockConnectorLine => {
			const diagramBlockConnectorsId = diagramBlockConnectorLine.id.split('-');

			diagramBlockConnectorLine.remove();
			diagramBlockConnectorLine = createDiagramBlockConnectorLine(
				document.querySelector(`.diagram-block-connector[id="${diagramBlockConnectorsId[0]}"]`),
				document.querySelector(`.diagram-block-connector[id="${diagramBlockConnectorsId[1]}"]`)
			);
			diagramBlockConnectorLine.style = `stroke-width: ${1 + diagramCurrentScale}px;`;
		});
	}

	document.querySelectorAll('.btn-diagram-zoom').forEach(diagramZoomButton => {
		diagramZoomButton.addEventListener('click', function() {
			if (diagramZoomButton.id == '+' && diagramCurrentScaleNum != 10) {
				diagramCurrentScale += 0.1;
				diagramCurrentScaleNum++;
			} else if (diagramZoomButton.id == '-' && diagramCurrentScaleNum != -9) {
				diagramCurrentScale -= 0.1;
				diagramCurrentScaleNum--;
			}

			diagramSetZoom();

			fetch(saveTelegramBotDiagramCurrentScaleUrl, {
				method: 'PATCH',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Token ${userApiToken}`,
				},
				body: JSON.stringify({'diagram_current_scale': diagramCurrentScale}),
			});
		});
	});

	const getCenterDiagramBlockConnectorPosition = (diagramBlockConnector) => {
		const diagramBlockConnectorRect = diagramBlockConnector.getBoundingClientRect();
		const diagramRect = diagram.getBoundingClientRect();

		const x = diagramBlockConnectorRect.left - diagramRect.left + diagram.scrollLeft + diagramBlockConnectorRect.width / 2 - 1;
		const y = diagramBlockConnectorRect.top - diagramRect.top + diagram.scrollTop + diagramBlockConnectorRect.height / 2 - 1;

		return {x, y}
	}

	const createDiagramBlockConnectorLine = (startDiagramBlockConnector, endDiagramBlockConnector) => {
		const startDiagramBlockConnectorPosition = getCenterDiagramBlockConnectorPosition(startDiagramBlockConnector);
		const endDiagramBlockConnectorPosition = getCenterDiagramBlockConnectorPosition(endDiagramBlockConnector);

		const diagramBlockConnectorLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
		diagramBlockConnectorLine.classList = 'diagram-block-connector-line';
		diagramBlockConnectorLine.id = `${startDiagramBlockConnector.id}-${endDiagramBlockConnector.id}`;
		diagramBlockConnectorLine.setAttribute('marker-end', 'url(#arrow)');
		diagramBlockConnectorLine.setAttribute('x1', startDiagramBlockConnectorPosition.x);
		diagramBlockConnectorLine.setAttribute('y1', startDiagramBlockConnectorPosition.y);
		diagramBlockConnectorLine.setAttribute('x2', endDiagramBlockConnectorPosition.x);
		diagramBlockConnectorLine.setAttribute('y2', endDiagramBlockConnectorPosition.y);
		diagramBlockConnectorLine.style.strokeWidth = `${1 + diagramCurrentScale}px`;
		diagramSvg.appendChild(diagramBlockConnectorLine);

		startDiagramBlockConnector.parentElement.querySelectorAll('.diagram-block-connector').forEach(diagramBlockConnector => {
			if (diagramBlockConnector != startDiagramBlockConnector) {
				diagramBlockConnector.classList.add('d-none');
			}
		});

		return diagramBlockConnectorLine;
	}

	const updateDiagramBlockConnectorLine = (diagramBlock) => {
		diagramSvg.querySelectorAll('.diagram-block-connector-line').forEach(diagramBlockConnectorLine => {
			const diagramBlockConnectorsId = diagramBlockConnectorLine.id.split('-');

			for (let i = 0; i < diagramBlockConnectorsId.length; i++) {
				const diagramBlockConnectorId = diagramBlockConnectorsId[i];

				if (diagramBlockConnectorId.split(':')[0] == diagramBlock.id) {
					const diagramBlockConnector = document.querySelector(`.diagram-block-connector[id="${diagramBlockConnectorId}"]`);
					const diagramBlockConnectorPosition = getCenterDiagramBlockConnectorPosition(diagramBlockConnector);

					if (i == 0) {
						diagramBlockConnectorLine.setAttribute('x1', diagramBlockConnectorPosition.x);
						diagramBlockConnectorLine.setAttribute('y1', diagramBlockConnectorPosition.y);
					} else {
						diagramBlockConnectorLine.setAttribute('x2', diagramBlockConnectorPosition.x);
						diagramBlockConnectorLine.setAttribute('y2', diagramBlockConnectorPosition.y);
					}

					break;
				}
			}
		});
	}

	const diagramBlockConnectorClick = (event) => {
		const selectDiagramBlockConnectorPosition = event.target.id.split(':')[1]

		if (selectedDiagramBlockConnector == null && selectDiagramBlockConnectorPosition != 'top') {
			selectedDiagramBlockConnector = event.target;
			selectedDiagramBlockConnector.classList.add('diagram-block-connector-highlight');
		} else if (selectedDiagramBlockConnector != null) {
			const selectedDiagramBlockConnectorBlockId = selectedDiagramBlockConnector.id.split(':')[0];
			const selectedDiagramBlockConnectorPosition = selectedDiagramBlockConnector.id.split(':')[1];
			const selectDiagramBlockConnectorBlockId = event.target.id.split(':')[0];

			if (selectedDiagramBlockConnector != event.target) {
				if (
					selectedDiagramBlockConnectorBlockId != selectDiagramBlockConnectorBlockId &&
					selectedDiagramBlockConnectorPosition != 'top' && selectDiagramBlockConnectorPosition == 'top'
				) {
					let findedDiagramBlockConnectorLine = false;

					diagramSvg.querySelectorAll('.diagram-block-connector-line').forEach(diagramBlockConnectorLine => {
						if (
							diagramBlockConnectorLine.id == `${selectedDiagramBlockConnector.id}-${event.target.id}` ||
							diagramBlockConnectorLine.id == `${event.target.id}-${selectedDiagramBlockConnector.id}`
						) {
							findedDiagramBlockConnectorLine = true;

							diagramBlockConnectorLine.remove();

							selectedDiagramBlockConnector.parentElement.querySelectorAll('.diagram-block-connector').forEach(diagramBlockConnector => diagramBlockConnector.classList.remove('d-none'));

							const diagramBlockKeyboardButtonId = diagramBlockConnectorLine.id.split('-')[0].split(':')[2];

							fetch(`/telegram-bots/${telegramBotId}/commands/${selectedDiagramBlockConnectorBlockId}/keyboard-buttons/${diagramBlockKeyboardButtonId}/telegram-bot-command/`, {
								method: 'DELETE',
								headers: {'Authorization': `Token ${userApiToken}`},
							});
						}
					});

					if (findedDiagramBlockConnectorLine == false) {
						createDiagramBlockConnectorLine(selectedDiagramBlockConnector, event.target);

						const selectedDiagramBlockKeyboardButtonId = selectedDiagramBlockConnector.id.split(':')[2];

						fetch(`/telegram-bots/${telegramBotId}/commands/${selectedDiagramBlockConnectorBlockId}/keyboard-buttons/${selectedDiagramBlockKeyboardButtonId}/telegram-bot-command/`, {
							method: 'POST',
							headers: {
								'Content-Type': 'application/json',
								'Authorization': `Token ${userApiToken}`,
							},
							body: JSON.stringify({
								'telegram_bot_command_id': parseInt(selectDiagramBlockConnectorBlockId),
								'start_diagram_connector': selectedDiagramBlockConnector.id,
								'end_diagram_connector': event.target.id,
							}),
						});
					}

					selectedDiagramBlockConnector.classList.remove('diagram-block-connector-highlight');
					selectedDiagramBlockConnector = null;
				}
			} else {
				selectedDiagramBlockConnector.classList.remove('diagram-block-connector-highlight');
				selectedDiagramBlockConnector = null;
			}
		}
	}

	const enableDiagramBlockDragging = (diagramBlock) => {
		let x = 0, y = 0;

		const startDrag = (event) => {
			event.preventDefault();

			if (event.type == 'touchstart') {
				x = event.touches[0].clientX;
				y = event.touches[0].clientY;
			} else {
				x = event.clientX;
				y = event.clientY;
			}

			diagramBlock.style.zIndex = '3';

			document.onmousemove = drag;
			document.ontouchmove = drag;

			document.onmouseup = endDrag;
			document.ontouchend = endDrag;
		}

		const drag = (event) => {
			event.preventDefault();

			let clientX, clientY;

			if (event.type == 'touchmove') {
				clientX = event.touches[0].clientX;
				clientY = event.touches[0].clientY;
			} else {
				clientX = event.clientX;
				clientY = event.clientY;
			}

			const diagramBlockLeft = diagramBlock.offsetLeft - (x - clientX);
			const diagramBlockTop = diagramBlock.offsetTop - (y - clientY);

			const diagramLeftBorder = (diagramBlock.offsetWidth * diagramCurrentScale - diagramBlock.offsetWidth) / 2;
			const diagramTopBorder = (diagramBlock.offsetHeight * diagramCurrentScale - diagramBlock.offsetHeight) / 2;

			if (diagramBlockLeft >= diagramLeftBorder) {
				diagramBlock.style.left = `${diagramBlockLeft}px`;
			} else {
				diagramBlock.style.left = `${diagramLeftBorder}px`;
			}
			if (diagramBlockTop >= diagramTopBorder) {
				diagramBlock.style.top = `${diagramBlockTop}px`;
			} else {
				diagramBlock.style.top = `${diagramTopBorder}px`;
			}

			x = clientX;
			y = clientY;

			updateDiagramBlockConnectorLine(diagramBlock);
		}

		const endDrag = () => {
			diagramBlock.style.zIndex = '1';

			document.onmousemove = null;
			document.ontouchmove = null;

			document.onmouseup = null;
			document.ontouchend = null;

			fetch(`/telegram-bots/${telegramBotId}/commands/${diagramBlock.id}/save-position/`, {
				method: 'PATCH',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Token ${userApiToken}`,
				},
				body: JSON.stringify({
					'x': diagramBlock.offsetLeft,
					'y': diagramBlock.offsetTop,
				}),
			});
		}

		diagramBlock.onmousedown = startDrag;
		diagramBlock.ontouchstart = startDrag;
	}

	const createDiagramBlock = (telegramBotCommand) => {
		const diagramBlock = document.createElement('div');
		diagramBlock.classList = 'diagram-block';
		diagramBlock.id = telegramBotCommand.id;
		diagramBlock.style.left = `${telegramBotCommand.x}px`;
		diagramBlock.style.top = `${telegramBotCommand.y}px`;
		diagramBlock.innerHTML = [
			`<div class="diagram-block-connector diagram-block-connector-top" id="${diagramBlock.id}:top:${diagramBlock.id}"></div>`,
			`<button class="btn-diagram btn-diagram-edit btn btn-secondary rounded-end-0 text-center" id="${diagramBlock.id}">`,
			`	<i class="bi bi-pencil-square d-flex" style="font-size: 1.5rem;"></i>`,
			`</button>`,
			`<button class="btn-diagram btn-diagram-delete btn btn-danger rounded-start-0 text-center" id="${diagramBlock.id}">`,
			`	<i class="bi bi-trash d-flex" style="font-size: 1.5rem;"></i>`,
			`</button>`,
			`<div class="diagram-block-name bg-light border text-center text-break p-2 mb-2">${telegramBotCommand.name}</div>`,
			(telegramBotCommand.image) ? `<img class="img-thumbnail rounded mb-2" src="${telegramBotCommand.image}">` : '',
			(telegramBotCommand.message_text.mode !== 'default') ? `<div class="language-${telegramBotCommand.message_text.mode} bg-light border rounded text-break p-2" style="font-size: 14px;"><pre class="bg-light p-0 m-0"><code>${telegramBotCommand.message_text.text}</code></pre></div>` : `<div class="bg-light border rounded text-break p-2" style="font-size: 15px;">${telegramBotCommand.message_text.text}</div>`,
		].join('');

		if (telegramBotCommand.keyboard != null) {
			telegramBotCommand.keyboard.buttons.forEach(telegramBotCommandKeyboardButton => {
				const diagramBlockKeyboardButton = document.createElement('div')
				diagramBlockKeyboardButton.className = 'diagram-block-keyboard-button bg-dark rounded text-light text-center text-break w-100 p-2';
				diagramBlockKeyboardButton.id = diagramBlock.id;
				diagramBlockKeyboardButton.innerHTML = [
					`${telegramBotCommandKeyboardButton.text}`,
					`<div class="diagram-block-connector diagram-block-connector-left${(telegramBotCommandKeyboardButton.url != null) ? ' d-none' : ''}" id="${diagramBlock.id}:left:${telegramBotCommandKeyboardButton.id}"></div>`,
					`<div class="diagram-block-connector diagram-block-connector-right${(telegramBotCommandKeyboardButton.url != null) ? ' d-none' : ''}" id="${diagramBlock.id}:right:${telegramBotCommandKeyboardButton.id}"></div>`,
				].join('');
				diagramBlock.appendChild(diagramBlockKeyboardButton);
			});
		}

		diagram.appendChild(diagramBlock);

		const diagramBlockName = diagramBlock.querySelector('.diagram-block-name');

		if (diagramBlockName.offsetHeight > 42) {
			diagramBlockName.classList.add('rounded-bottom');
		}

		let diagramBlockKeyboardButtonPosition = 4;

		diagramBlock.querySelectorAll('.diagram-block-keyboard-button').forEach(diagramBlockKeyboardButton => {
			diagramBlockKeyboardButtonPosition += diagramBlockKeyboardButton.offsetHeight + 4;
			diagramBlockKeyboardButton.style.bottom = `-${diagramBlockKeyboardButtonPosition}px`;
		});

		diagramBlock.querySelectorAll('.diagram-block-connector').forEach(diagramBlockConnector => diagramBlockConnector.addEventListener('click', diagramBlockConnectorClick));

		const diagramBlockEditButton = diagramBlock.querySelector('.btn-diagram-edit');

		diagramBlockEditButton.addEventListener('click', function() {
			fetch(`/telegram-bots/${telegramBotId}/commands/${this.id}/`, {
				method: 'GET',
				headers: {'Authorization': `Token ${userApiToken}`},
			}).then(response => {
				response.json().then(jsonResponse => {
					if (response.ok) {
						telegramBotCommandOffcanvas.show('edit', jsonResponse);
					} else {
						createToast(jsonResponse.message, jsonResponse.level);
					}
				});
			});
		});

		const diagramBlockDeleteButton = diagramBlock.querySelector('.btn-diagram-delete');

		diagramBlockDeleteButton.addEventListener('click', () => askConfirmModal(
			deleteTelegramBotCommandAskConfirmModalTitle,
			deleteTelegramBotCommandAskConfirmModalText,
			function() {
				fetch(`/telegram-bots/${telegramBotId}/commands/${diagramBlockDeleteButton.id}/`, {
					method: 'DELETE',
					headers: {'Authorization': `Token ${userApiToken}`},
				}).then(response => {
					if (response.ok) updateDiagramBlocks();
					response.json().then(jsonResponse => createToast(jsonResponse.message, jsonResponse.level));
				});
			}
		));

		enableDiagramBlockDragging(diagramBlock);
		Prism.highlightAll();
	}

	function updateDiagramBlocks() {
		fetch(telegramBotCommandsUrl, {
			method: 'GET',
			headers: {'Authorization': `Token ${userApiToken}`},
		}).then(response => {
			if (response.ok) {
				response.json().then(telegramBotCommands => {
					document.querySelectorAll('.diagram-block').forEach(diagramBlock => diagramBlock.remove());
					document.querySelectorAll('.diagram-block-connector-line').forEach(diagramBlockConnectorLine => diagramBlockConnectorLine.remove());

					telegramBotCommands.forEach(telegramBotCommand => createDiagramBlock(telegramBotCommand));

					const createDiagramBlockConnectorLines = (telegramBotCommandKeyboard) => {
						telegramBotCommandKeyboard.buttons.forEach(telegramBotCommandKeyboardButton => {
							if (telegramBotCommandKeyboardButton.telegram_bot_command_id != null) {
								const startDiagramBlockConnector = document.querySelector(`.diagram-block-connector[id="${telegramBotCommandKeyboardButton.start_diagram_connector}"]`);
								const endDiagramBlockConnector = document.querySelector(`.diagram-block-connector[id="${telegramBotCommandKeyboardButton.end_diagram_connector}"]`);

								createDiagramBlockConnectorLine(startDiagramBlockConnector, endDiagramBlockConnector);
							}
						});
					}

					telegramBotCommands.forEach(telegramBotCommand => {
						if (telegramBotCommand.keyboard != null) {
							const diagramBlock = document.querySelector(`.diagram-block[id="${telegramBotCommand.id}"]`);
							const diagramBlockImage = diagramBlock.querySelector('img');

							if (diagramBlockImage != null) {
								diagramBlockImage.addEventListener('load', () => createDiagramBlockConnectorLines(telegramBotCommand.keyboard));
							} else {
								createDiagramBlockConnectorLines(telegramBotCommand.keyboard);
							}
						}
					});
				});

				diagramSetZoom();
			} else {
				response.json().then(jsonResponse => createToast(jsonResponse.message, jsonResponse.level));
			}
		});
	}

	updateDiagramBlocks();
}
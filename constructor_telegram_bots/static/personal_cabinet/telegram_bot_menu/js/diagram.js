{
	const diagramSvg = document.querySelector('.diagram-svg');
	const diagramContainer = document.querySelector('.diagram-container');

	let diagramCurrentScaleNum = Math.floor(diagramCurrentScale * 10 - 10);

	function diagramSetZoom() {
		document.querySelectorAll('.diagram-block').forEach(diagramBlock => diagramBlock.style.transform = `scale(${diagramCurrentScale})`);
		document.querySelectorAll('.connector-line').forEach(connectorLine => {
			const diagramConnectorsId = connectorLine.id.split('-');

			connectorLine.remove();
			connectorLine = createDiagramConnectorLine(
				document.querySelector(`.diagram-connector[id="${diagramConnectorsId[0]}"]`),
				document.querySelector(`.diagram-connector[id="${diagramConnectorsId[1]}"]`)
			);
			connectorLine.style = `stroke-width: ${1 + diagramCurrentScale}px;`;
		});
	}

	document.querySelectorAll('.diagram-zoom-btn').forEach(diagramZoomButton => {
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

	const getCenterDiagramConnectorPosition = (diagramConnector) => {
		const diagramConnectorRect = diagramConnector.getBoundingClientRect();
		const diagramContainerRect = diagramContainer.getBoundingClientRect();

		const x = diagramConnectorRect.left - diagramContainerRect.left + diagramContainer.scrollLeft + diagramConnectorRect.width / 2 - 1;
		const y = diagramConnectorRect.top - diagramContainerRect.top + diagramContainer.scrollTop + diagramConnectorRect.height / 2 - 1;

		return {x, y}
	}

	function createDiagramConnectorLine(startDiagramConnector, endDiagramConnector) {
		const startDiagramConnectorPosition = getCenterDiagramConnectorPosition(startDiagramConnector);
		const endDiagramConnectorPosition = getCenterDiagramConnectorPosition(endDiagramConnector);

		const diagramConnectorLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
		diagramConnectorLine.classList = 'connector-line';
		diagramConnectorLine.id = `${startDiagramConnector.id}-${endDiagramConnector.id}`;
		diagramConnectorLine.style.strokeWidth = `${1 + diagramCurrentScale}px`;

		diagramConnectorLine.setAttribute('marker-end', 'url(#arrow)');
		diagramConnectorLine.setAttribute('x1', startDiagramConnectorPosition.x);
		diagramConnectorLine.setAttribute('y1', startDiagramConnectorPosition.y);
		diagramConnectorLine.setAttribute('x2', endDiagramConnectorPosition.x);
		diagramConnectorLine.setAttribute('y2', endDiagramConnectorPosition.y);

		diagramSvg.appendChild(diagramConnectorLine);

		startDiagramConnector.parentElement.querySelectorAll('.diagram-connector').forEach(diagramConnector => {
			if (diagramConnector != startDiagramConnector) {
				diagramConnector.classList.add('d-none')
			}
		});

		return diagramConnectorLine;
	}

	const updateConnectorLine = (block) => {
		diagramSvg.querySelectorAll('.connector-line').forEach(connectorLine => {
			const diagramConnectorsId = connectorLine.id.split('-');

			for (let i = 0; i < diagramConnectorsId.length; i++) {
				const diagramConnectorId = diagramConnectorsId[i];

				if (diagramConnectorId.split(':')[0] == block.id) {
					const diagramConnectorPosition = getCenterDiagramConnectorPosition(
						document.querySelector(`.diagram-connector[id="${diagramConnectorId}"]`)
					);

					if (i == 0) {
						connectorLine.setAttribute('x1', diagramConnectorPosition.x);
						connectorLine.setAttribute('y1', diagramConnectorPosition.y);
					} else {
						connectorLine.setAttribute('x2', diagramConnectorPosition.x);
						connectorLine.setAttribute('y2', diagramConnectorPosition.y);
					}

					break;
				}
			}
		});
	}

	{
		let selectedDiagramConnector = null;

		function connectorClick(event) {
			const selectDiagramConnectorPosition = event.target.id.split(':')[1]

			if (selectedDiagramConnector == null && selectDiagramConnectorPosition != 'top') {
				selectedDiagramConnector = event.target;
				selectedDiagramConnector.classList.add('connector-highlight');
			} else if (selectedDiagramConnector != null) {
				const selectedDiagramConnectorBlockId = selectedDiagramConnector.id.split(':')[0];
				const selectedDiagramConnectorPosition = selectedDiagramConnector.id.split(':')[1];
				const selectDiagramConnectorBlockId = event.target.id.split(':')[0];

				if (selectedDiagramConnector != event.target) {
					if (
						selectedDiagramConnectorBlockId != selectDiagramConnectorBlockId &&
						selectedDiagramConnectorPosition != 'top' && selectDiagramConnectorPosition == 'top'
					) {
						let findDiagramConnectorLine = false;

						diagramSvg.querySelectorAll('.connector-line').forEach(diagramConnectorLine => {
							if (
								diagramConnectorLine.id == `${selectedDiagramConnector.id}-${event.target.id}` ||
								diagramConnectorLine.id == `${event.target.id}-${selectedDiagramConnector.id}`
							) {
								findDiagramConnectorLine = true;

								diagramConnectorLine.remove();

								selectedDiagramConnector.parentElement.querySelectorAll('.diagram-connector').forEach(diagramConnector => diagramConnector.classList.remove('d-none'));

								const diagramKeyboardButtonId = diagramConnectorLine.id.split('-')[0].split(':')[2];

								fetch(`/telegram-bots/${telegramBotId}/commands/${selectedDiagramConnectorBlockId}/keyboard-buttons/${diagramKeyboardButtonId}/telegram-bot-command/`, {
									method: 'DELETE',
									headers: {'Authorization': `Token ${userApiToken}`},
								});
							}
						});

						if (findDiagramConnectorLine == false) {
							createDiagramConnectorLine(selectedDiagramConnector, event.target);

							const selectedDiagramKeyboardButtonId = selectedDiagramConnector.id.split(':')[2];

							fetch(`/telegram-bots/${telegramBotId}/commands/${selectedDiagramConnectorBlockId}/keyboard-buttons/${selectedDiagramKeyboardButtonId}/telegram-bot-command/`, {
								method: 'POST',
								headers: {
									'Content-Type': 'application/json',
									'Authorization': `Token ${userApiToken}`,
								},
								body: JSON.stringify({
									'telegram_bot_command_id': parseInt(selectDiagramConnectorBlockId),
									'start_diagram_connector': selectedDiagramConnector.id,
									'end_diagram_connector': event.target.id,
								}),
							});
						}

						selectedDiagramConnector.classList.remove('connector-highlight');
						selectedDiagramConnector = null;
					}
				} else {
					selectedDiagramConnector.classList.remove('connector-highlight');
					selectedDiagramConnector = null;
				}
			}
		}
	}

	const enableDiagramBlockDragging = (diagramBlock) => {
		let x = 0, y = 0;

		const diagramDragStart = (event) => {
			event.preventDefault();

			if (event.type == 'touchstart') {
				x = event.touches[0].clientX;
				y = event.touches[0].clientY;
			} else {
				x = event.clientX;
				y = event.clientY;
			}

			diagramBlock.style.zIndex = '3';

			document.onmousemove = diagramBlockDrag;
			document.ontouchmove = diagramBlockDrag;

			document.onmouseup = diagramDragEnd;
			document.ontouchend = diagramDragEnd;
		}

		const diagramBlockDrag = (event) => {
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

			const diagramContainerLeftBorder = (diagramBlock.offsetWidth * diagramCurrentScale - diagramBlock.offsetWidth) / 2;
			const diagramContainerTopBorder = (diagramBlock.offsetHeight * diagramCurrentScale - diagramBlock.offsetHeight) / 2;

			if (diagramBlockLeft >= diagramContainerLeftBorder) {
				diagramBlock.style.left = `${diagramBlockLeft}px`;
			} else {
				diagramBlock.style.left = `${diagramContainerLeftBorder}px`;
			}
			if (diagramBlockTop >= diagramContainerTopBorder) {
				diagramBlock.style.top = `${diagramBlockTop}px`;
			} else {
				diagramBlock.style.top = `${diagramContainerTopBorder}px`;
			}

			x = clientX;
			y = clientY;

			updateConnectorLine(diagramBlock);
		}

		const diagramDragEnd = () => {
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

		diagramBlock.onmousedown = diagramDragStart;
		diagramBlock.ontouchstart = diagramDragStart;
	}

	function createDiagramBlock(telegramBotCommand) {
		const diagramBlock = document.createElement('div');
		diagramBlock.classList = 'diagram-block';
		diagramBlock.id = telegramBotCommand['id'];
		diagramBlock.style.left = `${telegramBotCommand['x']}px`;
		diagramBlock.style.top = `${telegramBotCommand['y']}px`;
		diagramBlock.innerHTML = [
			`<div class="diagram-connector diagram-connector-top" id="${telegramBotCommand['id']}:top:${telegramBotCommand['id']}"></div>`,
			`<button class="diagram-button diagram-edit-button btn btn-secondary rounded-end-0 text-center" id="${telegramBotCommand['id']}">`,
			`	<i class="bi bi-pencil-square d-flex" style="font-size: 1.5rem;"></i>`,
			`</button>`,
			`<button class="diagram-button diagram-delete-button btn btn-danger rounded-start-0 text-center" id="${telegramBotCommand['id']}">`,
			`	<i class="bi bi-trash d-flex" style="font-size: 1.5rem;"></i>`,
			`</button>`,
			`<div class="diagram-name bg-light border text-center text-break p-2 mb-2">${telegramBotCommand['name']}</div>`,
			(telegramBotCommand['image'] != '') ? `<img class="img-thumbnail rounded mb-2" src="/${telegramBotCommand['image']}">` : '',
			`<div class="language-html bg-light border rounded text-break p-2" style="font-size: 14px;"><pre class="bg-light p-0 m-0"><code>${telegramBotCommand['message_text']}</code></pre></div>`,
		].join('');

		if (telegramBotCommand['keyboard'] != null) {
			telegramBotCommand['keyboard']['buttons'].forEach(telegramBotCommandKeyboardButton => {
				const diagramKeyboardButton = document.createElement('div')
				diagramKeyboardButton.className = 'diagram-keyboard-button bg-dark rounded text-light text-center text-break w-100 p-2';
				diagramKeyboardButton.id = telegramBotCommand['id'];
				diagramKeyboardButton.innerHTML = [
					`${telegramBotCommandKeyboardButton['text']}`,
					`<div class="diagram-connector diagram-connector-left${(telegramBotCommandKeyboardButton['url'] != null) ? ' d-none' : ''}" id="${telegramBotCommand['id']}:left:${telegramBotCommandKeyboardButton['id']}"></div>`,
					`<div class="diagram-connector diagram-connector-right${(telegramBotCommandKeyboardButton['url'] != null) ? ' d-none' : ''}" id="${telegramBotCommand['id']}:right:${telegramBotCommandKeyboardButton['id']}"></div>`,
				].join('');
				diagramBlock.append(diagramKeyboardButton);
			});
		}

		diagramContainer.append(diagramBlock);

		let diagramKeyboardButtonPosition = 4;

		diagramBlock.querySelectorAll('.diagram-keyboard-button').forEach(diagramKeyboardButton => {
			diagramKeyboardButtonPosition += diagramKeyboardButton.offsetHeight + 4;
			diagramKeyboardButton.style.bottom = `-${diagramKeyboardButtonPosition}px`;
		});

		Prism.highlightAll();

		enableDiagramBlockDragging(diagramBlock);
	}
}
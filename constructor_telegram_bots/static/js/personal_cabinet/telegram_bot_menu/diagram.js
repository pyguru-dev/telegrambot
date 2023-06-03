{
	let diagramSvg = document.querySelector('.diagram-svg');

	let diagramContainer = document.querySelector('.diagram-container');

	let diagramCurrentScaleNum = 0;

	if (diagramCurrentScale != 1) {
		let diagramCurrentScaleTest = 1.0;
		
		if (diagramCurrentScale > 1.0) {
			for (diagramCurrentScaleNum; diagramCurrentScaleNum < 10; diagramCurrentScaleNum++) {
				if (diagramCurrentScaleTest == diagramCurrentScale) {
					break;
				}
				diagramCurrentScaleTest += 0.1;
			}
		} else if (diagramCurrentScale < 1.0) {
			for (diagramCurrentScaleNum; diagramCurrentScaleNum > -9; diagramCurrentScaleNum--) {
				if (diagramCurrentScaleTest == diagramCurrentScale) {
					break;
				}
				diagramCurrentScaleTest -= 0.1;
			}
		}
	}

	function diagramSetZoom() {
		document.querySelectorAll('.diagram-block').forEach(diagramBlock => diagramBlock.style.transform = `scale(${diagramCurrentScale})`);
		document.querySelectorAll('.connector-line').forEach(connectorLine => {
			let diagramConnectorsId = connectorLine.id.split('-');
			let startDiagramConnector = document.querySelector(`.diagram-connector[id="${diagramConnectorsId[0]}"]`);
			let endDiagramConnector = document.querySelector(`.diagram-connector[id="${diagramConnectorsId[1]}"]`);

			connectorLine.remove();

			connectorLine = createDiagramConnectorLine(startDiagramConnector, endDiagramConnector);
			connectorLine.style = `stroke-width: ${1 + diagramCurrentScale}px;`;
		});
	}

	document.querySelectorAll('.diagram-zoom-btn').forEach(diagramZoomButton => {
		diagramZoomButton.addEventListener('click', function() {
			if (this.id == '+' && diagramCurrentScaleNum != 10) {
				diagramCurrentScale += 0.1;
				diagramCurrentScaleNum++;
			} else if (this.id == '-' && diagramCurrentScaleNum != -9) {
				diagramCurrentScale -= 0.1;
				diagramCurrentScaleNum--;
			}

			fetch(saveTelegramBotDiagramCurrentScaleUrl, {
				method: 'POST',
				headers: {'Content-Type': 'application/json'},
				body: JSON.stringify(
					{
						'diagram_current_scale': diagramCurrentScale,
					}
				),
			});

			diagramSetZoom();
		});
	});

	function getCenterDiagramConnectorPosition(diagramConnector) {
		let diagramConnectorRect = diagramConnector.getBoundingClientRect();
		let diagramContainerRect = diagramContainer.getBoundingClientRect();

		let x = diagramConnectorRect.left - diagramContainerRect.left;
		x += diagramContainer.scrollLeft + diagramConnectorRect.width / 2;
		x--;
		let y = diagramConnectorRect.top - diagramContainerRect.top;
		y += diagramContainer.scrollTop + diagramConnectorRect.height / 2;
		y--;

		return {x, y}
	}

	function updateConnectorLine(block) {
		diagramSvg.querySelectorAll('.connector-line').forEach(connectorLine => {
			let diagramConnectorsId = connectorLine.id.split('-');

			for (let i = 0; i < diagramConnectorsId.length; i++) {
				let diagramConnectorId = diagramConnectorsId[i];

				if (diagramConnectorId.split(':')[0] == block.id) {
					let diagramConnector = document.querySelector(`.diagram-connector[id="${diagramConnectorId}"]`);
					let diagramConnectorPosition = getCenterDiagramConnectorPosition(diagramConnector);

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

	function createDiagramConnectorLine(startDiagramConnector, endDiagramConnector) {
		let diagramConnectorLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');

		let startDiagramConnectorPosition = getCenterDiagramConnectorPosition(startDiagramConnector);
		let endDiagramConnectorPosition = getCenterDiagramConnectorPosition(endDiagramConnector);

		diagramConnectorLine.classList = 'connector-line';
		diagramConnectorLine.id = `${startDiagramConnector.id}-${endDiagramConnector.id}`;
		diagramConnectorLine.style = `stroke-width: ${1 + diagramCurrentScale}px;`;

		diagramConnectorLine.setAttribute('marker-end', 'url(#arrow)');
		diagramConnectorLine.setAttribute('x1', startDiagramConnectorPosition.x);
		diagramConnectorLine.setAttribute('y1', startDiagramConnectorPosition.y);
		diagramConnectorLine.setAttribute('x2', endDiagramConnectorPosition.x);
		diagramConnectorLine.setAttribute('y2', endDiagramConnectorPosition.y);
		
		diagramSvg.appendChild(diagramConnectorLine);

		return diagramConnectorLine;
	}

	{
		let selectedDiagramConnector = null;

		function connectorClick(event) {
			let selectDiagramConnectorPosition = event.target.id.split(':')[1]

			if (selectedDiagramConnector == null && selectDiagramConnectorPosition != 'top') {
				selectedDiagramConnector = event.target;
				selectedDiagramConnector.classList.add('connector-highlight');
			} else if (selectedDiagramConnector != null) {
				let selectedDiagramConnectorBlockId = selectedDiagramConnector.id.split(':')[0]
				let selectedDiagramConnectorPosition = selectedDiagramConnector.id.split(':')[1]
				let selectDiagramConnectorBlockId = event.target.id.split(':')[0]

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

								let diagramKeyboardButtonId = diagramConnectorLine.id.split('-')[0].split(':')[2];

								fetch(`/telegram-bot/${telegramBotId}/command/${selectedDiagramConnectorBlockId}/keyboard-button/${diagramKeyboardButtonId}/delete-telegram-bot-command/`, {
									method: 'POST',
								});
							}
						});

						if (findDiagramConnectorLine == false) {
							createDiagramConnectorLine(selectedDiagramConnector, event.target);

							let selectedDiagramKeyboardButtonId = selectedDiagramConnector.id.split(':')[2];

							fetch(`/telegram-bot/${telegramBotId}/command/${selectedDiagramConnectorBlockId}/keyboard-button/${selectedDiagramKeyboardButtonId}/add-telegram-bot-command/`, {
								method: 'POST',
								headers: {'Content-Type': 'application/json'},
								body: JSON.stringify(
									{
										'telegram_bot_command_id': parseInt(selectDiagramConnectorBlockId),
										'start_diagram_connector': selectedDiagramConnector.id,
										'end_diagram_connector': event.target.id,
									}
								),
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


	function enableDiagramBlockDragging(diagramBlock) {
		let x = 0, y = 0;
	
		function diagramDragStart(event) {
			event = event || window.event;
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
	
		function diagramBlockDrag(event) {
			event = event || window.event;
			event.preventDefault();
	
			let clientX, clientY;
	
			if (event.type == 'touchmove') {
				clientX = event.touches[0].clientX;
				clientY = event.touches[0].clientY;
			} else {
				clientX = event.clientX;
				clientY = event.clientY;
			}
	
			let diagramBlockLeft = diagramBlock.offsetLeft - (x - clientX);
			let diagramBlockTop = diagramBlock.offsetTop - (y - clientY);
	
			let diagramContainerLeftBorder = (diagramBlock.offsetWidth * diagramCurrentScale - diagramBlock.offsetWidth) / 2;
			let diagramContainerTopBorder = (diagramBlock.offsetHeight * diagramCurrentScale - diagramBlock.offsetHeight) / 2;
	
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
	
		function diagramDragEnd() {
			diagramBlock.style.zIndex = '1';
	
			document.onmousemove = null;
			document.ontouchmove = null;
	
			document.onmouseup = null;
			document.ontouchend = null;
	
			fetch(`/telegram-bot/${telegramBotId}/command/${diagramBlock.id}/save-position/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
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
		let diagramBlock = document.createElement('div');
		diagramBlock.classList = 'diagram-block';
		diagramBlock.id = telegramBotCommand['id'];
		diagramBlock.style.left = `${telegramBotCommand['x']}px`;
		diagramBlock.style.top = `${telegramBotCommand['y']}px`;
		diagramBlock.innerHTML = [
			`<div class="diagram-connector diagram-connector-top" id="${telegramBotCommand['id']}:top:${telegramBotCommand['id']}"></div>`,
			`<button class="diagram-button diagram-edit-button btn btn-secondary rounded-end-0 text-center" id="${telegramBotCommand['id']}">`,
			`	<i class="bi bi-pencil-square" style="font-size: 1.5rem;"></i>`,
			`</button>`,
			`<button class="diagram-button diagram-delete-button btn btn-danger rounded-start-0 text-center" id="${telegramBotCommand['id']}">`,
			`	<i class="bi bi-trash" style="font-size: 1.5rem;"></i>`,
			`</button>`,
			`<div class="diagram-name bg-light border text-center text-break p-2 mb-2">${telegramBotCommand['name']}</div>`,
			(telegramBotCommand['image'] != '') ? `<img class="img-thumbnail rounded mb-2" src="/${telegramBotCommand['image']}">` : '',
			`<div class="bg-light border rounded text-break p-2">${telegramBotCommand['message_text']}</div>`,
		].join('');

		let diagramKeyboardButtonPosition = 46;

		if (telegramBotCommand['keyboard'] != null) {
			telegramBotCommand['keyboard']['buttons'].forEach(telegramBotCommandKeyboardButton => {
				let diagramKeyboardButton = document.createElement('div')
				diagramKeyboardButton.className = 'diagram-keyboard-button btn btn-dark w-100';
				diagramKeyboardButton.id = telegramBotCommand['id'];
				diagramKeyboardButton.style.bottom = `-${diagramKeyboardButtonPosition}px`;
				diagramKeyboardButton.innerHTML = [
					`${telegramBotCommandKeyboardButton['text']}`,
					`<div class="diagram-connector diagram-connector-left" id="${telegramBotCommand['id']}:left:${telegramBotCommandKeyboardButton['id']}"></div>`,
					`<div class="diagram-connector diagram-connector-right" id="${telegramBotCommand['id']}:right:${telegramBotCommandKeyboardButton['id']}"></div>`,
				].join('');
				diagramBlock.append(diagramKeyboardButton);

				diagramKeyboardButtonPosition += 38 + 4;
			});
		}

		enableDiagramBlockDragging(diagramBlock);
		diagramContainer.append(diagramBlock);
	}
}
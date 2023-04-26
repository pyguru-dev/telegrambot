{
    var infoAboutTelegramBotModalBootstrap = new bootstrap.Modal('#infoAboutTelegramBotModal');

    let infoAboutTelegramBotModalAlertPlaceholder = document.querySelector('#infoAboutTelegramBotModalAlertPlaceholder');

    telegramBotPrivateCheckBox.addEventListener('click', function() {
        let request = new XMLHttpRequest();
        request.open('POST', `/telegram-bot/${telegramBotId}/edit/private/`, true);
        request.setRequestHeader('Content-Type', 'application/json');
        request.onreadystatechange = checkRequestResponse(function() {
            let telegramBotAllowedUserButtons = document.querySelectorAll('.telegram-bot-allowed-user-button');

            if (telegramBotPrivateCheckBox.checked) {
                for (let i = 0; i < telegramBotAllowedUserButtons.length; i++) {
                    telegramBotAllowedUserButtons[i].classList.remove('d-none');
                }
            } else {
                for (let i = 0; i < telegramBotAllowedUserButtons.length; i++) {
                    telegramBotAllowedUserButtons[i].classList.add('d-none');
                }
            }

            myAlert(infoAboutTelegramBotModalAlertPlaceholder, request.responseText, 'success');
        });
        request.send(JSON.stringify(
            {
                'telegram_bot_private': this.checked,
            }
        ));
    });
}
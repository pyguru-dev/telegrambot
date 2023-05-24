# Constructor Telegram Bots
**Constructor Telegram Bots** - сайт, с помощью которого вы можете легко, бесплатно и без каких-либо знаний в программирование, сделать своего многофункционального Telegram бота.

Сайт является некоммерческим и не преследует цель заработать на своих пользователях.

Сайт был создан, потому-что к сожелению все похожие сайты являються коммерческими и преследуют цель заработать на своих пользователях, а бесплатный тариф на таких сайтах очень сильно ограничивает своих же пользователей сайта.

Если вы хотите как-то поддержать сайт, то вы можете сделать пожертвование сайту.<br> 
Ваше пожертвование очень сильно поможет развитию и улучшению сайта.<br>
Пожертвование сайту можно сделать по данной ссылке: **https://www.paypal.com/donate/?hosted_button_id=RBCS5HAMZS5Z6**

# Требование
- Python **3.10.11**

# Установка проекта и запуск его
1. Устанавливаем проект:
```sh
git clone https://github.com/EXG1O/Constructor-Telegram-Bots.git
cd Constructor-Telegram-Bots
python -m venv env
source env/bin/activate
pip install -U pip
pip install -r requirements.txt
cd constructor_telegram_bots
python manage.py migrate
```
2. Запускаем **manage.py** файл:
```sh
python manage.py runserver
```
3. Если вы всё правильно сделали, то у вас будет такой вывод:
```
Enter the Constructor Telegram bot API-token in the file ./data/constructor_telegram_bot_api.token!
```
4. Теперь вам нужно создать своего Telegram бота через [BotFather](https://t.me/BotFather) Telegram бота.
5. После того, как вы создали Telegram бота, вам нужно скопировать его **API-токен** и добавить его в файл **./data/constructor_telegram_bot_api.token**.
6. Теперь в файле **./constructor_telegram_bots/settings.py** на **12** строке включите **DEBUG** режим.
7. После этого в файле **./templates/navbar.html** на **28** строке замените **username** Telegram бота на **username** своего выше созданного Telegram бота.
6. Запускаем ещё раз **manage.py** файл:
```sh
python manage.py runserver
```
7. Если вы всё сделали правильно, то в консоли будет следующий вывод:
```
[ДАТА ВРЕМЯ]: Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
ДАТА - ВРЕМЯ
Django version 4.2.1, using settings 'constructor_telegram_bots.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
8. Переходим по ссылке **http://127.0.0.1:8000/** и пользуемся сайтом. ☺️

# Cтруктура проекта
```
Constructor-Telegram-Bots
├── constructor_telegram_bots
│   ├── constructor_telegram_bots
│   │   ├── asgi.py
│   │   ├── decorators.py
│   │   ├── functions.py
│   │   ├── __init__.py
│   │   ├── gunicorn_config.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── donation
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── templates
│   │   │   ├── base_donation.html
│   │   │   ├── donation_completed.html
│   │   │   └── donation.html
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── home
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── templates
│   │   │   └── home.html
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── personal_cabinet
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── templates
│   │   │   ├── modals
│   │   │   │   └── add_or_duplicate_telegram_bot_modal.html
│   │   │   ├── personal_cabinet
│   │   │   │   ├── modals
│   │   │   │   │   └── how_to_add_telegram_bot_modal.html
│   │   │   │   └── main.html
│   │   │   ├── telegram_bot_menu
│   │   │   │   ├── modals
│   │   │   │   │   └── add_or_edit_telegram_bot_command_modal.html
│   │   │   │   └── main.html
│   │   │   └── base_personal_cabinet.html
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── privacy_policy
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── templates
│   │   │   └── privacy_policy.html
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── static
│   │   ├── icons
│   │   │   └── favicon.ico
│   │   └── js
│   │       ├── global
│   │       │   ├── modals
│   │       │   │   └── ask_confirm_modal.js
│   │       │   ├── alert.js
│   │       │   ├── init.js
│   │       │   └── logout.js
│   │       └── personal_cabinet
│   │           ├── modals
│   │           │   └── add_or_duplicate_telegram_bot_modal.js
│   │           ├── personal_cabinet
│   │           │   └── init.js
│   │           └── telegram_bot_menu
│   │               ├── modals
│   │               │   └── add_or_edit_telegram_bot_command_modal.js
│   │               ├── init.js
│   │               └── main.js
│   ├── telegram_bot
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   └── __init__.py
│   │   ├── apps.py
│   │   ├── decorators.py
│   │   ├── functions.py
│   │   ├── __init__.py
│   │   ├── managers.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── telegram_bots
│   │   ├── __init__.py
│   │   ├── constructor_telegram_bot.py
│   │   ├── custom_aiogram.py
│   │   ├── functions.py
│   │   └── user_telegram_bot.py
│   ├── templates
│   │   ├── modals
│   │   │   └── ask_confirm_modal.html
│   │   ├── 404.html
│   │   ├── base_error_or_success.html
│   │   ├── base.html
│   │   ├── footer.html
│   │   └── navbar.html
│   ├── user
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   └── __init__.py
│   │   ├── templates
│   │   │   ├── login.html
│   │   │   └── logout.html
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── managers.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   └── manage.py
├── .gitignore
├── LICENSE.md
├── README.md
└── requirements.txt
```
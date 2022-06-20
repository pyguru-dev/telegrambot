# WebSite Exg1o
**WebSite Exg1o** - сайт с помощью которого вы сможете легко и без каких либо навыков в программирование сделать своего Telegram бота.

# Возможности сайта
- Создавать своих ботов;
- Глубокая настройка своих ботов;
- Добавлять команды для своих ботов.

# Установка и использовани
1. Устанавливаем **Python 3.9.0**;
2. Устанавливаем и запускаем сайт:
```sh
git clone https://github.com/EXG1O/WebSite-Exg1o.git
cd WebSite-Exg1o/exg1o/exg1o
```
3. В файле **settings.py** на **27** строке меняем константу **DEBUG**:
```sh
DEBUG = True
```
4. Запускаем сайт:
```sh
python manage.py runserver
```
5. Если всё успешно запустилось, то в консоль должно вывестись это:
```sh
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
June 13, 2022 - 11:49:34
Django version 4.0.4, using settings 'exg1o.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```
6. Пользуемся сайтом 😊!

# Демонстрация сайта
## Главное страница
![site](site_pages_images/main_page.jpg)
## Страница регистрации
![site](site_pages_images/registration_page.jpg)
## Страница авторизации
![site](site_pages_images/authorization_page.jpg)
## Страница аккаунта
![site](site_pages_images/account_view_page.jpg)
## Страница улучшения аккаунта
![site](site_pages_images/upgrade_account_page.jpg)
## Страница списка ботов
![site](site_pages_images/konstruktor_page.jpg)
## Страница добавления бота
![site](site_pages_images/add_bot.jpg)
## Страница конструктора бота
![site](site_pages_images/view_bot_konstruktor_page.jpg)
## Страница добавление команд боту
![site](site_pages_images/add_command_page.jpg)
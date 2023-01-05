# Constructor Telegram Bots
**Constructor Telegram Bots** - сайт с помощью которого вы сможете легко и без каких либо навыков в программирование сделать своего Telegram бота.

# Возможности сайта
- Создать собственного Telegram бота;
- Легко и гипко настроить вашего Telegram бота;
- Добавить команды с любым функционалом вашему Telegram боту;
- Изменять или удалять ранее добавленные команду вашего Telegram бота.

# Установка и использовани
1. Устанавливаем **Python 3.10.7** (Установить другую версию **Python** можно спомощью программы **Python3 Installer**: https://github.com/EXG1O/Python3-Installer);
2. Устанавливаем сайт:
```sh
git clone https://github.com/EXG1O/Constructor-Telegram-Bots.git
cd Constructor-Telegram-Bots
pip3 install -r requirements.txt
cd constructor_telegram_bots/constructor_telegram_bots
nano settings.py
```
3. В файле **settings.py** на **27** строке меняем константу **DEBUG**:
```sh
DEBUG = True
```
4. Запускаем сайт:
```sh
cd ..
python3 manage.py migrate
python3 manage.py runserver
```
5. Если всё успешно запустилось, то в консоль должно вывестись это:
```sh
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
June 13, 2022 - 11:49:34 # Дата может быть другая!!!
Django version 4.1.1, using settings 'constructor_telegram_bots.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```
6. Пользуемся сайтом 😊!
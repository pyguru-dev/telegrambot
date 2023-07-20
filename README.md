# 🇷🇺 **На русском языке**
## **Constructor Telegram Bots**</a>
<a href="https://constructor.exg1o.org/">**Constructor Telegram Bots**</a> - сайт, с помощью которого вы можете легко, бесплатно и без каких-либо знаний в программирование, сделать своего многофункционального Telegram бота.

Сайт является некоммерческим и не преследует цель заработать на своих пользователях.

Сайт был создан, потому-что к сожелению все похожие сайты являються коммерческими и преследуют цель заработать на своих пользователях, а бесплатный тариф на таких сайтах очень сильно ограничивает своих же пользователей сайта.

Если вы хотите как-то поддержать сайт, то вы можете сделать пожертвование сайту.<br> 
Ваше пожертвование очень сильно поможет развитию и улучшению сайта.<br>
Пожертвование сайту можно сделать по данной ссылке: **https://www.paypal.com/donate/?hosted_button_id=RBCS5HAMZS5Z6**

## Требования
- Python 3.10.11
- PostgreSQL
- MongoDB
- Redis

## Установка проекта и запуск сайта
1. Клонируем проект и запускаем скрипт для его установки:
```
git clone https://github.com/EXG1O/Constructor-Telegram-Bots.git
cd Constructor-Telegram-Bots
source scripts/setup.sh
cd constructor_telegram_bots
```
2. Теперь запускаем сайт:
```
python manage.py runserver
```
3. Открываем ещё один терминал и запускаем Celery:
```
cd Constructor-Telegram-Bots
source env/bin/activate
cd constructor_telegram_bots
celery -A constructor_telegram_bots worker --loglevel=INFO -f logs/celery.log
```
4. Пользуемся сайтом ☺️!

# 🇺🇦 **На українській мові**
## **Constructor Telegram Bots**</a>
<a href="https://constructor.exg1o.org/">**Constructor Telegram Bots**</a> - сайт, за допомогою якого ви можете легко, безкоштовно і без будь-яких знань у програмуванні, зробити свого багатофункціонального Telegram бота.

Сайт є некомерційним і не має на меті заробити на своїх користувачах.

Сайт був створений, тому що на жаль всі схожі сайти є комерційними і мають на меті заробити на своїх користувачах, а безкоштовний тариф на таких сайтах дуже сильно обмежує своїх користувачів сайту.

Якщо ви хочете якось підтримати сайт, то ви можете зробити пожертву сайту.<br>
Ваша пожертва дуже сильно допоможе розвитку та покращенню сайту.<br>
Пожертву сайту можна зробити за цим посиланням: **https://www.paypal.com/donate/?hosted_button_id=RBCS5HAMZS5Z6**

## Вимоги
- Python 3.10.11
- PostgreSQL
- MongoDB
- Redis

## Встановлення проекту та запуск сайту
1. Клонуємо проект та запускаємо скрипт для його встановлення:
```
git clone https://github.com/EXG1O/Constructor-Telegram-Bots.git
cd Constructor-Telegram-Bots
source scripts/setup.sh
cd constructor_telegram_bots
```
2. Тепер запускаємо сайт:
```
python manage.py runserver
```
3. Відкриваємо ще один термінал та запускаємо Celery:
```
cd Constructor-Telegram-Bots
source env/bin/activate
cd constructor_telegram_bots
celery -A constructor_telegram_bots worker --loglevel=INFO -f logs/celery.log
```
4. Користуємося сайтом ☺️!

# 🇬🇧 **On the English language**
## **Constructor Telegram Bots**</a>
<a href="https://constructor.exg1o.org/">**Constructor Telegram Bots**</a> - a site with which you can easily, for free and without any knowledge into programming, to make your multifunctional Telegram bot.

The site is non-commercial and does not aim to make money on its users.

The site was created because, unfortunately, all similar sites are commercial and aim to make money on their users, and the free tariff on such sites severely limits their own users of the site.

If you want to somehow support the site, you can donate the site.<br>
Your donation will greatly contribute to the development and improvement of the site.<br>
You can donate to the site at this link: **https://www.paypal.com/donate/?hosted_button_id=RBCS5HAMZS5Z6**

## Requirements
- Python 3.10.11
- PostgreSQL
- MongoDB
- Redis

## Installing the project and running the site
1. Clone the project and run the script to install it:
```
git clone https://github.com/EXG1O/Constructor-Telegram-Bots.git
cd Constructor-Telegram-Bots
source scripts/setup.sh
cd constructor_telegram_bots
```
2. Now run the site:
```
python manage.py runserver
```
3. Open another terminal and run Celery:
```
cd Constructor-Telegram-Bots
source env/bin/activate
cd constructor_telegram_bots
celery -A constructor_telegram_bots worker --loglevel=INFO -f logs/celery.log
```
4. Use the site ☺️!

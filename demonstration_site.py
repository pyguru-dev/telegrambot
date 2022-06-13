from selenium import webdriver
import time

SITE = 'http://127.0.0.1:8000/'

browser = webdriver.Chrome()
browser.set_window_size(1920, 1080)

initial_pages ={
	'main': '',
	'authorization': 'authorization/',
	'registration': 'registration/'
}

for page in initial_pages:
	browser.get(f'{SITE}{initial_pages[page]}')
	time.sleep(1)
	browser.save_screenshot(f'demonstration_images/{page}_page.jpg')

browser.get(f'{SITE}authorization/')
time.sleep(1)
login_input = browser.find_element_by_class_name('login-input-control')
login_input.send_keys('Exg1o')
password_input = browser.find_element_by_class_name('password-input-control')
password_input.send_keys('Somova1985')
authorization_button = browser.find_element_by_class_name('authorization-button-control')
authorization_button.click()
time.sleep(1)
browser.save_screenshot(f'demonstration_images/account_view_page.jpg')

upgrade_account_buttom = browser.find_element_by_class_name('upgrade-account-buttom-control')
upgrade_account_buttom.click()
time.sleep(1)
browser.save_screenshot(f'demonstration_images/upgrade_account_page.jpg')

konstruktor_button = browser.find_element_by_id('konstruktorButtonLink')
konstruktor_button.click()
time.sleep(1)
browser.save_screenshot(f'demonstration_images/konstruktor_page.jpg')

add_bot_button = browser.find_element_by_class_name('add-bot-button-control')
add_bot_button.click()
time.sleep(1)
browser.save_screenshot(f'demonstration_images/add_bot.jpg')
back_button = browser.find_element_by_class_name('back-button-control')
back_button.click()
time.sleep(1)

bot_link = browser.find_element_by_class_name('bot-name')
bot_link.click()
time.sleep(1)
browser.save_screenshot(f'demonstration_images/view_bot_konstruktor_page.jpg')

add_command_button = browser.find_element_by_class_name('add-command-button-control')
add_command_button.click()
time.sleep(1)
browser.save_screenshot(f'demonstration_images/add_command_page.jpg')

browser.close()
""""
Скрипт для того, чтобы сделать скрины всех страниц на сайте "Exg1o".
Скрипт не будет работать без драйвера "selenium" для Chrome (Только для Windows!!!).
Скрипт можно удалить, если вам он не нужен!
"""

from selenium.webdriver.common.by import By
from selenium import webdriver
import time

class DemonstrationSitePages:
	def __init__(self, site_address: str, screen_size: list):
		self.SITE = site_address

		self.browser = webdriver.Chrome()
		self.browser.set_window_size(screen_size[0], screen_size[1])

	def click_button(self, by: By, element: str):
		time.sleep(1)
		button = self.browser.find_element(by, element)
		button.click()
		time.sleep(1)

	def screenshot_page(self, screenshot_name: str):
		time.sleep(1)
		self.browser.save_screenshot(f'site_pages_images/{screenshot_name}.png')

	def screenshot_initial_pages(self):
		initial_pages ={
			'1_main_page': '',
			'2_authorization_page': 'authorization/',
			'3_registration_page': 'registration/'
		}

		for page in initial_pages:
			self.browser.get(f'{self.SITE}{initial_pages[page]}')
			self.screenshot_page(page)

	def auth_on_site(self):
		self.browser.get(f'{self.SITE}authorization/')
		time.sleep(1)
		login_input = self.browser.find_element(By.CLASS_NAME, 'login-input-control')
		login_input.send_keys('Exg1o')
		password_input = self.browser.find_element(By.CLASS_NAME, 'password-input-control')
		password_input.send_keys('Somova1985')
		self.click_button(By.CLASS_NAME, 'authorization-button-control')

	def screenshot_other_pages(self):
		other_pages = {
			'4_account_view_page': 'account/view/Exg1o/',
			'5_upgrade_account_page': 'account/Exg1o/upgrade/',
			'6_constructor_page': 'constructor/Exg1o/',
			'7_add_bot_page': 'constructor/Exg1o/add_bot/',
			'8_view_bot_constructor_page': 'bot-name',
			'9_add_command_page': 'add-command-button-control',
			'10_edit_command_page': 'bot-command-name'
		}

		for page in other_pages:
			if page in ['8_view_bot_constructor_page', '9_add_command_page', '10_edit_command_page']:
				self.browser.get(f'{self.SITE}constructor/Exg1o/')
				self.click_button(By.CLASS_NAME, 'bot-name')
				if page == 'view_bot_constructor_page':
					self.screenshot_page(page)
				else:
					self.click_button(By.CLASS_NAME, other_pages[page])
					self.screenshot_page(page)
			else:
				self.browser.get(f'{self.SITE}{other_pages[page]}')
				self.screenshot_page(page)

	def start(self):
		self.screenshot_initial_pages()
		self.auth_on_site()
		self.screenshot_other_pages()
		self.browser.close()

if __name__ == '__main__':
	demonstration_site_pages = DemonstrationSitePages('http://127.0.0.1:8000/', [1920, 1080])
	demonstration_site_pages.start()
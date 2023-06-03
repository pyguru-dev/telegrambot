from kombu.exceptions import OperationalError

import sys
import os


def main() -> None:
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'constructor_telegram_bots.settings')

	try:
		from django.core.management import execute_from_command_line
	except ImportError as exc:
		raise ImportError(
			"Couldn't import Django. Are you sure it's installed and "
			"available on your PYTHONPATH environment variable? Did you "
			"forget to activate a virtual environment?"
		) from exc

	try:
		execute_from_command_line(sys.argv)
	except OperationalError:
		pass

if __name__ == '__main__':
	main()

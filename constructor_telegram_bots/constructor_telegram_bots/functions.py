from urllib.parse import ParseResult, urlparse

import random


def generate_random_string(length: int, chars: str) -> str:
	random_string = ''
	for num in range(length):
		random_string += random.choice(chars)
	return random_string


def is_valid_url(url: str) -> bool:
	parse_result: ParseResult = urlparse(url=url)
	return all([parse_result.scheme, parse_result.netloc])
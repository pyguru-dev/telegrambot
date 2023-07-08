from urllib.parse import ParseResult, urlparse

import random


def generate_random_string(length: int, chars: str) -> str:
	return ''.join([random.choice(chars) for num in range(length)])

def is_valid_url(url: str) -> bool:
	parse_result: ParseResult = urlparse(url=url)
	return all([parse_result.scheme, parse_result.netloc])

import random


def generate_random_string(length: int, chars: str) -> str:
	return ''.join([random.choice(chars) for num in range(length)])

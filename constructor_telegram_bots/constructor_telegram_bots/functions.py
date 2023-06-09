import random


def generate_random_string(length: int, chars: str) -> str:
	random_string = ''
	for _ in range(length):
		random_string += random.choice(chars)
	return random_string

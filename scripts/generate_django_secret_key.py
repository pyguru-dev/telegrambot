import random


random_string = ''
for num in range(50):
	random_string += random.choice('abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_')

print(f'django-insecure-{random_string}')

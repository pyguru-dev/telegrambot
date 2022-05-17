import os

try:
	os.mkdir('files')
	os.mkdir('files/users')
except FileExistsError:
	pass
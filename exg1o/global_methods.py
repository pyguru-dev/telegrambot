from Crypto.Cipher import DES

def clear_key(key: str): # Получение чистого ключа из пароля
	key = ''.join(list(key)[0:8]).encode('UTF-8')
	return key

def encrypt(key: str, data): # Шифрование
	def pad(data):
		while len(data) % 8 != 0:
			data += b' '
		return data

	key = clear_key(key)
	des = DES.new(key, DES.MODE_ECB)
	padded_data = pad(data.encode('UTF-8'))
	encrypted_data = des.encrypt(padded_data)
	return encrypted_data

def decrypt(key: str, encrypted_data): # Дешифровка
	key = clear_key(key)
	des = DES.new(key, DES.MODE_ECB)
	decrypted_data = des.decrypt(encrypted_data)
	return decrypted_data.decode('UTF-8').strip()
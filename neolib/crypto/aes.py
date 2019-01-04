from Crypto.Cipher import AES

from neolib.crypto.block_cipher import BaseBlockCipher128


class BlockCipherAES(BaseBlockCipher128):
	def encrypt_round(self, Src):
		obj = AES.new(self.user_key, AES.MODE_ECB)
		return obj.encrypt(Src)



	def decrypt_round(self, Src):
		obj = AES.new(self.user_key, AES.MODE_ECB)
		return obj.decrypt(Src)



if __name__ == '__main__':
	KEY = '00000000000000000000000000000000'
	IV = 'FFFFFFFFFFFFFFFF8000000000000000'
	PT = '00000000000000000000000000000000'
	CT = '3C5A01FA83BD62EA796EA867C4BA13ED'


	pass

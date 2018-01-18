from Crypto.Cipher import AES

from neolib.crypto.block_cipher import BaseBlockCipher128


class BlockCipherAES(BaseBlockCipher128):
	def encrypt_round(self, Src):
		obj = AES.new(self.user_key, AES.MODE_ECB)
		return obj.encrypt(Src)



	def decrypt_round(self, Src):
		obj = AES.new(self.user_key, AES.MODE_ECB)
		return obj.decrypt(Src)

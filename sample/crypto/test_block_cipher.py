import unittest


import Crypto.Util.Counter
from Crypto.Cipher import AES
from neolib.crypto.aes import BlockCipherAES
from neolib.crypto.block_cipher import BlockCipherMode

from neolib.hexstr_util import tobytes, tohexstr
from neolib import crypto_util_bin
#from study_test.crypto.block_cipher import BlockCipherAES


class MyTestCase(unittest.TestCase):
	key = tobytes('008545CC1BA298F2C9C10A18FE205D3D')
	msg = tobytes('F84015FFDB88A19DD5600D047C5E803A' + "F84015FFDB88A19DD5600D047C5E803A")
	cipher = tobytes('ED08818197015FA4812E75BFF06515D8')
	nonce = crypto_util_bin.getrandom(16)
	iv = b'\x00' * 16
	iv_2 = b'\x01' * 16

	def test_something(self):
		self.assertEqual(True, True)

	def test_aes_cbc(self):
		print('test_aes_cbc')
		obj = AES.new(self.key, AES.MODE_CBC, self.iv)
		cipher = obj.encrypt(self.msg)
		obj = AES.new(self.key, AES.MODE_CBC, self.iv)
		dec = obj.decrypt(cipher)
		self.assertEqual(self.msg,dec)

		s = BlockCipherAES(self.key, self.iv,BlockCipherMode.CBC)

		cipher2 = s.encrypt(self.msg)
		dec2 = s.decrypt(cipher2)

		self.assertEqual(cipher, cipher2)
		self.assertEqual(self.msg, dec2)
		print(tohexstr(self.msg))
		print(tohexstr(cipher))
		print(tohexstr(cipher2))
		print(tohexstr(dec))

		print(tohexstr(dec2))


	def test_aes_ecb(self):
		print('test_aes_ecb')
		obj = AES.new(self.key, AES.MODE_ECB, self.iv)
		cipher = obj.encrypt(self.msg)
		obj = AES.new(self.key, AES.MODE_ECB, self.iv)
		dec = obj.decrypt(cipher)
		self.assertEqual(self.msg,dec)

		s = BlockCipherAES(self.key,self.iv,BlockCipherMode.ECB)

		cipher2 = s.encrypt(self.msg)
		dec2 = s.decrypt(cipher2)

		self.assertEqual(cipher, cipher2)
		self.assertEqual(self.msg, dec2)
		print(tohexstr(self.msg))
		print(tohexstr(cipher))
		print(tohexstr(cipher2))
		print(tohexstr(dec))
		print(tohexstr(dec2))
	def ctr_reset(self):
		self.count = 0

	def ctr_counter(self):
		ret = self.nonce[0:8] + self.count.to_bytes(8, 'big')
		self.count +=1
		return ret

	def test_aes_ctr(self):
		print('test_aes_ctr')
		#ctr = Crypto.Util.Counter.new(128, initial_value=int.from_bytes(self.iv,'big'))
		self.count = 0
		obj = AES.new(self.key, AES.MODE_CTR,counter=self.ctr_counter)
		cipher = obj.encrypt(self.msg)
		ctr = Crypto.Util.Counter.new(128, initial_value=0)
		self.count = 0
		obj = AES.new(self.key, AES.MODE_CTR, self.iv,counter=self.ctr_counter)
		dec = obj.decrypt(cipher)
		self.assertEqual(self.msg,dec)


		s = BlockCipherAES(self.key, self.nonce, BlockCipherMode.CTR)

		cipher2 = s.encrypt(self.msg)
		dec2 = s.decrypt(cipher2)

		print("msg",tohexstr(self.msg))
		print("cipher",tohexstr(cipher))
		print("cipher2",tohexstr(cipher2))
		print("dec",tohexstr(dec))
		print("dec2",tohexstr(dec2))

		self.assertEqual(self.msg, dec2)

		self.assertEqual(cipher, cipher2)

	def test_aes_ctr_1(self):
		print('test_aes_ctr_1')
		# ctr = Crypto.Util.Counter.new(128, initial_value=int.from_bytes(self.iv,'big'))
		self.count = 0
		ctr = Crypto.Util.Counter.new(128, initial_value=int.from_bytes(self.nonce[0:8]+b'\x00'*8, 'big'))
		# asfsa = ctr()
		#
		# print(tohexstr(asfsa))
		# asfsa = ctr()
		#print(tohexstr(asfsa))
		obj = AES.new(self.key, AES.MODE_CTR, counter=ctr)
		cipher = obj.encrypt(self.msg)
		ctr = Crypto.Util.Counter.new(128, initial_value=int.from_bytes(self.nonce[0:8]+b'\x00'*8, 'big'))
		self.count = 0
		obj = AES.new(self.key, AES.MODE_CTR, self.iv, counter=ctr)
		dec = obj.decrypt(cipher)
		self.assertEqual(self.msg, dec)

		s = BlockCipherAES(self.key, self.nonce, BlockCipherMode.CTR)

		cipher2 = s.encrypt(self.msg)
		dec2 = s.decrypt(cipher2)


		print("msg", tohexstr(self.msg))
		print("cipher", tohexstr(cipher))
		print("cipher2", tohexstr(cipher2))
		print("dec", tohexstr(dec))
		print("dec2", tohexstr(dec2))

		self.assertEqual(self.msg, dec2)

		self.assertEqual(cipher, cipher2)




if __name__ == '__main__':
	unittest.main()

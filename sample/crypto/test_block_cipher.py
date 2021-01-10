import unittest

import Crypto.Util.Counter
from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long

from neolib import crypto_util_bin
from neolib.crypto.aes import BlockCipherAES
from neolib.crypto.block_cipher import BlockCipherMode
from neolib.hexstr_util import tobytes, tohexstr
# from study_test.crypto.block_cipher import BlockCipherAES
from sample.crypto.aes_gcm_ref import AES_GCM, InvalidTagException


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
	def test_aes_gcm(self):
		master_key = 0xfeffe9928665731c6d6a8f9467308308
		plaintext = b'\xd9\x31\x32\x25\xf8\x84\x06\xe5' + \
		            b'\xa5\x59\x09\xc5\xaf\xf5\x26\x9a' + \
		            b'\x86\xa7\xa9\x53\x15\x34\xf7\xda' + \
		            b'\x2e\x4c\x30\x3d\x8a\x31\x8a\x72' + \
		            b'\x1c\x3c\x0c\x95\x95\x68\x09\x53' + \
		            b'\x2f\xcf\x0e\x24\x49\xa6\xb5\x25' + \
		            b'\xb1\x6a\xed\xf5\xaa\x0d\xe6\x57' + \
		            b'\xba\x63\x7b\x39'
		auth_data = b'\xfe\xed\xfa\xce\xde\xad\xbe\xef' + \
		            b'\xfe\xed\xfa\xce\xde\xad\xbe\xef' + \
		            b'\xab\xad\xda\xd2'
		init_value = 0xcafebabefacedbaddecaf888
		ciphertext = b'\x42\x83\x1e\xc2\x21\x77\x74\x24' + \
		             b'\x4b\x72\x21\xb7\x84\xd0\xd4\x9c' + \
		             b'\xe3\xaa\x21\x2f\x2c\x02\xa4\xe0' + \
		             b'\x35\xc1\x7e\x23\x29\xac\xa1\x2e' + \
		             b'\x21\xd5\x14\xb2\x54\x66\x93\x1c' + \
		             b'\x7d\x8f\x6a\x5a\xac\x84\xaa\x05' + \
		             b'\x1b\xa3\x0b\x39\x6a\x0a\xac\x97' + \
		             b'\x3d\x58\xe0\x91'
		auth_tag = 0x5bc94fbc3221a5db94fae95ae7121a47

		print('plaintext:', hex(bytes_to_long(plaintext)))

		my_gcm = AES_GCM(master_key)
		encrypted, new_tag = my_gcm.encrypt(init_value, plaintext, auth_data)
		print('encrypted:', hex(bytes_to_long(encrypted)))
		print('auth tag: ', hex(new_tag))

		try:
			decrypted = my_gcm.decrypt(init_value, encrypted,
			                           new_tag + 1, auth_data)
		except InvalidTagException:
			decrypted = my_gcm.decrypt(init_value, encrypted, new_tag, auth_data)
			print('decrypted:', hex(bytes_to_long(decrypted)))


		self.assertEqual(decrypted, plaintext)

		pass



if __name__ == '__main__':
	unittest.main()

import unittest
# from study_test.crypto.neo_sm4 import BlockCipherSM4
from base64 import b64encode, b64decode

from neolib.crypto.sm4 import BlockCipherSM4

from neolib.crypto.block_cipher import BlockCipherMode
from neolib.hexstr_util import tobytes, tohexstr
from sample.crypto import sm4_ref


class MyTestCase(unittest.TestCase):
	def test_unit_encrpyt(self):
		clear_num = 0x0123456789abcdeffedcba9876543210
		# 密钥
		mk = 0x0123456789abcdeffedcba9876543210
		# 加密
		inst = BlockCipherSM4(tobytes('0123456789abcdeffedcba9876543210'),None)
		cipher_num = sm4_ref.encrypt(clear_num, mk)
		cipher = inst.encrypt_round(tobytes('0123456789abcdeffedcba9876543210'))

		print(hex(cipher_num)[2:].replace('L', ''))
		print(tohexstr(cipher))
		self.assertEqual(cipher_num, int.from_bytes(cipher,'big'))

		dec = sm4_ref.decrypt(cipher_num, mk)
		dec2 = inst.decrypt_round(cipher)

		print(hex(dec)[2:].replace('L', ''))
		print(tohexstr(dec2))
		self.assertEqual(clear_num, dec)
		self.assertEqual(int.from_bytes(dec2,'big'), dec)

	def make_bt_key(self,text_key):
		return int.from_bytes(text_key.encode(), 'big').to_bytes(16, 'big')

	def make_bt_msg(self,text_msg):
		bt_plain = text_msg.encode()
		rest = 16 - len(bt_plain) % 16
		bt_plain += bytes([rest]) * rest
		return bt_plain

	def remove_padding(self,bt_msg):
		size = bt_msg[-1]
		dec2_remove_padding = bt_msg[:-size]
		return dec2_remove_padding

	def test_sm4_ecb(self):
		print('test_sm4_ecb')
		plain_text = 'pysm4是国密SM4算法的Python实现'
		key = 'hello, world!'  # 密钥长度小于等于16字节

		# 加密
		cipher_text = sm4_ref.encrypt_ecb(plain_text, key)
		print(cipher_text,tohexstr(b64decode(cipher_text)))

		dec = sm4_ref.decrypt_ecb(cipher_text, key)
		self.assertEqual(plain_text, dec)

		# bt_plain = plain_text.encode()
		# rest = 16 - len(bt_plain)%16
		# bt_plain += bytes([rest])*rest

		bt_key = self.make_bt_key(key)
		bt_plain =self.make_bt_msg(plain_text)

		#bt_key = int.from_bytes(key.encode(),'big').to_bytes(16,'big')
		print("bt_plain",tohexstr(bt_plain))
		print("bt_key", tohexstr(bt_key))

		inst = BlockCipherSM4(bt_key,None,BlockCipherMode.ECB)
		enc2 = inst.encrypt(bt_plain)
		dec2 = inst.decrypt(enc2)
		print(tohexstr(enc2))
		print(tohexstr(dec2))
		print(tohexstr(bt_plain))
		size = dec2[-1]

		dec2_remove_padding = self.remove_padding(dec2)
		print(dec2_remove_padding.decode())

		self.assertEqual(bt_plain, dec2)
		self.assertEqual(b64decode(cipher_text), enc2)
		self.assertEqual(dec2_remove_padding, plain_text.encode())







		print(cipher_text, plain_text)
	def test_sm4_cbc_from_ref(self):
		aes_key = tobytes('91F33CD73198E5CFD964C26B08FB3AB26A855F32B0435A2D0BA693EFBBA186ED')[:16]
		msg = tobytes("D498F47B8BBE5A650BFFF561A6088939CCB5953715E0C3399B0F07B00B505F3B")
		iv = tobytes("5DE0033B09C684C6B66BAF147506452D")
		cipher = tobytes("5EF49F59003627CD512C420F789B3A67AC5C7312F55BF95DCDEB94FE646F302A")
		print("msg",b64encode(msg))

		cipher_text = sm4_ref.encrypt_cbc_bt(msg,aes_key,iv)
		print(cipher_text, tohexstr(cipher_text))
		self.assertEqual(cipher_text, cipher)

		inst = BlockCipherSM4(aes_key, iv, BlockCipherMode.CBC)
		enc = inst.encrypt(msg)
		print(tohexstr(enc))
		self.assertEqual(enc, cipher)
		dec = inst.decrypt(enc)
		self.assertEqual(msg, dec)






	def test_sm4_cbc(self):
		print('test_sm4_cbc')
		plain_text = 'pysm4是国密SM4算法的Python实现'
		key = 'hello, world!'  # 密钥长度小于等于16字节
		iv = '11111111'

		# 加密
		cipher_text = sm4_ref.encrypt_cbc(plain_text, key, iv)
		print(cipher_text,tohexstr(b64decode(cipher_text)))


		dec = sm4_ref.decrypt_cbc(cipher_text, key, iv)
		self.assertEqual(plain_text, dec)

		# bt_plain = plain_text.encode()
		# rest = 16 - len(bt_plain)%16
		# bt_plain += bytes([rest])*rest

		bt_key = self.make_bt_key(key)
		bt_iv = self.make_bt_key(iv)
		bt_plain =self.make_bt_msg(plain_text)

		#bt_key = int.from_bytes(key.encode(),'big').to_bytes(16,'big')
		print("bt_plain",tohexstr(bt_plain))
		print("bt_key", tohexstr(bt_key))

		#inst = BlockCipherSM4(bt_key)
		inst = BlockCipherSM4(bt_key, bt_iv, BlockCipherMode.CBC)

		print(tohexstr(iv.encode()),len(iv.encode()))

		enc2 = inst.encrypt(bt_plain)
		dec2 = inst.decrypt(enc2)
		print(tohexstr(enc2))
		print(tohexstr(dec2))
		print(tohexstr(bt_plain))
		size = dec2[-1]

		dec2_remove_padding = self.remove_padding(dec2)
		print(dec2_remove_padding.decode())

		self.assertEqual(bt_plain, dec2)
		self.assertEqual(b64decode(cipher_text), enc2)
		self.assertEqual(dec2_remove_padding, plain_text.encode())







		print(cipher_text, plain_text)



if __name__ == '__main__':
	unittest.main()

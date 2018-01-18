from enum import Enum

from Crypto.Cipher import AES

from neolib.crypto_util_bin import *


from neolib import neoutil

class BlockCipherMode(Enum):
	ECB =0
	CBC = 1
	CTR  = 2


class BaseBlockCipher128:
	unit_size = 16

	def __init__(self, user_key,iv,block_mode = BlockCipherMode.CBC):
		'''

		:param UserKey: 16바이트
		'''
		self.user_key = tobytes(user_key)
		self.iv = tobytes(iv)

		self.map_process_block = {
			BlockCipherMode.ECB :(self.ECB_enc,self.ECB_dec),
			BlockCipherMode.CBC: (self.CBC_enc, self.CBC_dec),
			BlockCipherMode.CTR: (self.CTR_enc, self.CTR_dec),
		}
		self.enc_block,self.dec_block = self.map_process_block[block_mode]

	
	def crypto_template(self, src, iv, prev_iv_process, post_iv_process, round_calc):
		idx = 0
		remain_length = len(src)
		result_buff = b''

		class Struct:
			None

		struct = Struct()
		struct.iv = iv
		count = 0
		src = zero_padding(src, self.unit_size)
		#print('org src:', ByteArray2HexString(src))
		while remain_length > 0:
			real_size = min(remain_length, self.unit_size)
			round_buff = src[idx:idx + self.unit_size]
			#print('round_buff:', ByteArray2HexString(round_buff))

			struct.src_buff = round_buff
			struct.count = count

			calc_in = prev_iv_process(round_buff, struct)

			calc_out = round_calc(calc_in)

			crypt = post_iv_process(calc_out, struct)

			result_buff += crypt

			remain_length -= real_size
			idx += real_size
			count += 1

		return result_buff

	def ECB_dec(self, src):
		return self.crypto_template(src, None, lambda src, struct: src, lambda dst, struct: dst, self.decrypt_round)

	# return self.ECB_calc(src,self.decrypt)
	# None

	def ECB_enc(self, src):
		return self.crypto_template(src, None, lambda src, struct: src, lambda dst, struct: dst, self.encrypt_round)

	# return self.ECB_calc(src,self.encrypt)


	def CBC_enc(self, src):
		def prev_iv_process(src, struct):
			input_value = calc_xor(src, struct.iv)
			# bytes([ src[idx]^struct.iv[idx] for idx in range(len(src))])
			return input_value

		def post_iv_process(dst, struct):
			struct.iv = dst
			return dst

		return self.crypto_template(src, self.iv, prev_iv_process, post_iv_process, self.encrypt_round)

		None

	def CBC_dec(self, src):

		def prev_iv_process(src, struct):
			struct.iv2 = src
			return src

		def post_iv_process(dst, struct):
			cypherkey = calc_xor(dst, struct.iv)
			#			cypherkey = bytes([dst[idx] ^ struct.iv[idx] for idx in range(len(dst))])
			struct.iv = struct.src_buff
			return cypherkey

		return self.crypto_template(src, self.iv, prev_iv_process, post_iv_process,self.decrypt_round)

	def CTR_Comm(self, src,  calc):
		def prev_iv_process(src, struct):
			ret = struct.iv[0:8] + struct.count.to_bytes(8, 'big')
			return ret

		def post_iv_process(dst, struct):
			input_value = calc_xor(dst, struct.src_buff)
			# input_value = bytes([ src[idx]^dst[idx] for idx in range(len(src))])
			return input_value

		return self.crypto_template(src, self.iv, prev_iv_process, post_iv_process, calc)

	def CTR_enc(self, src):
		return self.CTR_Comm(src,  self.encrypt_round)

	def CTR_dec(self, src):
		return self.CTR_Comm(src,  self.encrypt_round)
	def encrypt_round(self, msg):

		pass

	def decrypt_round(self, msg):
		pass

	def encrypt(self, msg):
		return self.enc_block(msg)

	def decrypt(self, msg):
		return self.dec_block(msg)


class SampleAES(BaseBlockCipher128):
	def encrypt_round(self, Src):
		obj = AES.new(self.user_key, AES.MODE_ECB)
		return obj.encrypt(Src)



	def decrypt_round(self, Src):
		obj = AES.new(self.user_key, AES.MODE_ECB)
		return obj.decrypt(Src)

if __name__ == '__main__':
	key = tobytes('008545CC1BA298F2C9C10A18FE205D3D')
	msg = tobytes('F84015FFDB88A19DD5600D047C5E803A'+"F84015FFDB88A19DD5600D047C5E803A")
	cipher = tobytes('ED08818197015FA4812E75BFF06515D8')
	iv = b'\x01' * 16
	obj = AES.new(key, AES.MODE_ECB)
	cipher = obj.encrypt(msg)

	print(tohexstr(key),tohexstr(msg),tohexstr(cipher))

	obj = AES.new(key, AES.MODE_CBC, iv)
	cipher = obj.encrypt(msg)
	print(tohexstr(key), tohexstr(msg), tohexstr(cipher))
	#exit()



	s = SampleAES(key)
	enc = s.CBC_enc(msg,iv)
	dec = s.CBC_dec(enc, iv)

	print(tohexstr(enc), tohexstr(dec))

	s = SampleAES(key)

	enc = s.ECB_enc (msg)
	dec = s.ECB_dec(enc)
	print(tohexstr(enc),tohexstr(dec))
	exit()
	#s.base_check()
	# # 1. ����Ű �׽�Ʈ
	# #k = s.SeedRoundKey(b'\x00' * 16)
	#
	# test_rk  = '7E8C8F7C2CA237C7DB6C27FF4A68CAA7'
	# test_rk += 'A1019D2F419E0470C4B359AE0CE94542'
	# test_rk += '0F40D6A14E39C1DB08359685CB1F5F0C'
	# test_rk += 'A7BD84B6AEAEA46141077ED1A10AE9FE'
	# test_rk += 'D505CC7694737AE9926FAC50E566261B'
	# test_rk += '4A90B765B3A7C38E222E7E2FB921B1A2'
	# test_rk += 'E4FD0B4D9B8D884EDC8D1C63C4A67843'
	# test_rk += '5FF66A2131C0787850118971B055B298'
	# test_rk = neoutil.HexString2ByteArray(test_rk)
	# i = 0
	# for key in s.RoundKey:
	# 	print(hex(key),test_rk[i * 4:(i * 4) + 4])
	# 	tk = int.from_bytes(test_rk[i * 4:(i * 4) + 4],'little')#
	# 	i+= 1
	# 	# test_rk[i * 4:(i * 4) + 4] #struct.unpack('<L', test_rk[i * 4:(i * 4) + 4])[0]
	# 	if key == tk:
	# 		continue
	# 	else:
	# 		print('[1] ERROR')
	# 		exit(0)
	#
	# # for i in range(32) :
	# # 	tk = struct.unpack('<L', test_rk[i*4:(i*4)+4])[0]
	# #
	# # 	if s.RoundKey[i] == tk :
	# # 		continue
	# # 	else :
	# # 		print ('[1] ERROR')
	# # 		exit(0)

	print('[1] OK')
	print([hex(tmp) for tmp in s.RoundKey])



	# 2. ��ȣȭ �׽�Ʈ
	enc = s.SeedEncrypt(plan)
	print(enc)
	print(neoutil.ByteArray2HexString(b'\x00' * 16))
	print(neoutil.ByteArray2HexString(plan), neoutil.ByteArray2HexString(enc))
	if enc == ciph:
		print('[2] OK')
	else:
		print('[2] ERROR')

	# 3. ��ȣȭ �׽�Ʈ
	dec = s.SeedDecrypt(enc)

	if dec == plan:
		print('[3] OK')
	else:
		print('[3] ERROR')


	enc = s.CBC_enc(plan, b'\x00' * 16)
	dec = s.CBC_dec(enc, b'\x00' * 16)

	print(neoutil.ByteArray2HexString(enc))
	print('5EBAC6E0054E166819AFF1CC6D346CDBC619F2C0A615CDF2E77843B306E775F4')
	print(neoutil.ByteArray2HexString(dec))

from neolib import neoutil,neo_class,crypto_util,crypto_util_bin
from neolib.neoutil import tobytes,tohexstr

from  comm.open_ssl_define import *
#try:
from neolib.crypto.load_open_ssl import *
from neolib.crypto import load_open_ssl
from _ctypes import PyObj_FromPtr
#except:
#	pass


class NeoEccHandler():
	def __init__(self,nid=NID_X9_62_prime256v1):

		from comm import load_open_ssl
		from _ctypes import PyObj_FromPtr
		loading_ssl_functions(globals())

		self.g_ecc_group = EC_GROUP_new_by_curve_name(nid)
		self.ctx = BN_CTX_new()
		self.g_ecc_key = EC_KEY_new() # 키할당
		ret = EC_KEY_set_group(self.g_ecc_key, self.g_ecc_group)  # 그룹설정
		self.ec_point_public_key = None
		pass
		#neo_class.NeoRunnableClass.__init__(self)
	def generate_key(self):

		#EC_KEY_set_group(self.g_ecc_key, self.g_ecc_group) # 그룹설정
		EC_KEY_generate_key(self.g_ecc_key) # 키
		EC_KEY_check_key(self.g_ecc_key) # 키
		self.ec_point_public_key = EC_KEY_get0_public_key(self.g_ecc_key) # 공개키
		self.bn_private_key = EC_KEY_get0_private_key(self.g_ecc_key) # 개인키



	def get_hexstr_keys(self):
		hexstr_puk = EC_POINT_point2hex(self.g_ecc_group, self.ec_point_public_key, POINT_CONVERSION_UNCOMPRESSED, self.ctx).decode()
		hexstr_prk = BN_bn2hex(self.bn_private_key).decode()
		return hexstr_puk,hexstr_prk

	def get_kyes(self):
		hex_puk,hex_prk = self.get_hexstr_keys()
		return neoutil.HexString2ByteArray(hex_puk),neoutil.HexString2ByteArray(hex_prk)


	def init_key(self,puk,prk):
		#print(tohexstr(puk),tohexstr(prk))
		hex_str = tohexstr(puk)

		puk_t = EC_POINT_new(self.g_ecc_group)
		if puk != None and puk != b'':
			self.ec_point_public_key = EC_POINT_hex2point(self.g_ecc_group, hex_str.encode(), puk_t, self.ctx)
			ret = EC_KEY_set_public_key(self.g_ecc_key, self.ec_point_public_key) # puk
			#print('EC_KEY_set_public_key',ret)
			if ret != 1:
				raise Exception("FAIL TO IMORT PUBKEY")
		if prk != None and prk != b'':
			prk = tobytes(prk)
			self.bn_private_key = BN_new()
			BN_bin2bn(prk, len(prk), self.bn_private_key)
			ret = EC_KEY_set_private_key(self.g_ecc_key, self.bn_private_key) # prv
			#print('EC_KEY_set_private_key', ret)
			if ret != 1:
				raise Exception("FAIL TO IMORT PRIV")
	def key_check(self):
		ret = EC_KEY_check_key(self.g_ecc_key)  # 키
		return ret ==1



	def ecds_sign(self,bt_msg):
		bt_msg = tobytes(bt_msg)
		sign = ECDSA_do_sign(bt_msg, len(bt_msg), self.g_ecc_key)

		hexstr_r = BN_bn2hex(sign.contents.r)
		hexstr_s = BN_bn2hex(sign.contents.s)
		ECDSA_SIG_free(sign)
		return tobytes(hexstr_r.decode()),tobytes(hexstr_s.decode())


	def ecds_verify(self,bt_msg,r,s):
		pt_sign_Vc = ECDSA_SIG_new()

		sign_Vc = pt_sign_Vc.contents
		bt_msg = tobytes(bt_msg)


		BN_hex2bn(sign_Vc.r.contents.db_pointer(),tohexstr(r).encode())
		BN_hex2bn(sign_Vc.s.contents.db_pointer(), tohexstr(s).encode())

		ret = ECDSA_do_verify(bt_msg, len(bt_msg), sign_Vc.pointer(), self.g_ecc_key)

		print(ret)
		return ret

	def make_ecdh_from_other(self, other_handler):
		ECDH_P_x = (ctypes.c_ubyte * 65)()
		#print(ECDH_P_x)
		ECDH_P = EC_POINT_new(self.g_ecc_group)

		ret = EC_POINT_mul(self.g_ecc_group, ECDH_P, None, other_handler.ec_point_public_key, self.bn_private_key, self.ctx)
		#print(ret)
		ret = EC_POINT_point2oct(self.g_ecc_group, ECDH_P, POINT_CONVERSION_UNCOMPRESSED, ECDH_P_x, 65, self.ctx)
		#print(ret,ECDH_P_x)

		EC_POINT_free(ECDH_P)
		return bytes(ECDH_P_x)[1:]






		#ECDSA_SIG_free(sign)
	def verify(self,pubkey,privkey,msg,r,s):
		self.init_key(pubkey,privkey)
		ret = self.ecds_verify(msg,r,s)
		print("VERIFY",ret)
		return ret


	def do_test(self):
		self.generate_key()
		manage_pub = tobytes(
			"72CF56F5BF877DCF5823691682E9824C0B9742D1E0B41D288B478ECEF5218BAA1C484CBB848E449A6A5BCD4A686ECE676201073FD61241302BEB185C38E6E4BB")
		manage_priv = tobytes("91F33CD73198E5CFD964C26B08FB3AB26A855F32B0435A2D0BA693EFBBA186ED")

		self.init_key(
			b'\x04'+manage_pub,
			manage_priv)

		print(self.get_hexstr_keys())
		pub,prv = self.get_hexstr_keys()

		# print(self.get_hexstr_keys())

		btmsg = crypto_util.sha256(crypto_util.getrandom(32))

		print("hashoed msg",btmsg)

		hexstr_r,hexstr_s = self.ecds_sign(btmsg)
		print("R,S", tohexstr(hexstr_r), tohexstr(hexstr_s))
		s = BIGNUM()

		#BN_hex2bn(s.db_pointer(), 'E763D0F4C15A02F058951DF4E3DF7A27065F58B1B14576ABB2E83C85BBD2A3AB'.encode())

		#print(BN_bn2hex(s.pointer()))


		self.ecds_verify(btmsg,
		                 hexstr_r ,
		                 hexstr_s)
		#
		# self.ecds_verify('E959787BF9367A1CE99266AFA13CBAE53C4CE3DE0810464D0477B6955258F482',
		#                  'C6A23E1B389F3F4433B2C88D4B225CB585D5C6E20EFCF37C35BFCA907E14B3BA',
		#                  '69A142B10DEE7A431FA58341BDBC39D03D4C9368210104441588233820FFB489')
		#
		self.ecds_verify('DD319DC3C0F9AF7827DD7DA381B5BA36A3C8019F10894DC783F33F6F5A83A8AC',
		                 'B612AE0153AB4F90B3255F8518F3480063359506E9A450ADAF32270C3E16FB50',
		                 '93DCB91EAF73BC35670E26AD64D9D94D88B6D8D6212C37D4528DA246A31D459A')



		self.verify("04 72CF56F5BF877DCF5823691682E9824C0B9742D1E0B41D288B478ECEF5218BAA1C484CBB848E449A6A5BCD4A686ECE676201073FD61241302BEB185C38E6E4BB",
					"91F33CD73198E5CFD964C26B08FB3AB26A855F32B0435A2D0BA693EFBBA186ED"	,
		            btmsg,
		            hexstr_r,
		            hexstr_s            )



	def free(self):
		if self.ec_point_public_key != None:
			EC_POINT_free(self.ec_point_public_key)
		BN_CTX_free(self.ctx)
		#EC_KEY_free(self.g_ecc_key)
		None
		# EC_KEY_free(G_ECCkey_TSM)
		# EC_KEY_free(G_ECCkey_CHIP)
		# EC_KEY_free(G_ECCkey_A)
		# EC_KEY_free(G_ECCkey_B)
		# EC_POINT_free(G_puk_A)


def multi_value( d, G):
	d = tobytes(d)
	hexstr_puk = "04"+tohexstr(G)
	loading_ssl_functions(globals())

	ctx = BN_CTX_new()



	g_ecc_group = EC_GROUP_new_by_curve_name(NID_X9_62_prime256v1)
	puk_t = EC_POINT_new(g_ecc_group)

	ec_point_public_key = EC_POINT_hex2point(g_ecc_group, hexstr_puk.encode(), puk_t, ctx)
	ECDH_P_x = (ctypes.c_ubyte * 65)()

	ECDH_P = EC_POINT_new(g_ecc_group)
	bn_private_key = BN_new()
	BN_bin2bn(d, len(d), bn_private_key)


	ret = EC_POINT_mul(g_ecc_group, ECDH_P, None, ec_point_public_key, bn_private_key,
	                   ctx)
	print(ret)
	ret = EC_POINT_point2oct(g_ecc_group, ECDH_P, POINT_CONVERSION_UNCOMPRESSED, ECDH_P_x, 65, ctx)
	print(ret, ECDH_P_x)

	EC_POINT_free(ECDH_P)
	print(tohexstr(bytes(ECDH_P_x)[1:]))

if __name__ == '__main__':
#

	neo_ecc1 = NeoEccHandler()
	# neo_ecc1.do_test()
	# exit()
	neo_ecc1.init_key('04 0018AC197BAE8B64985E2BC6D75083A1CD7D210C6D5ED4D2D6D53EE261AC494EF7D91FB89A8345D9393C988CCBFC03190D21B53A051B025DBF4F500EFD15D0D5' ,None                 )
	#neo_ecc1.generate_key()

#	print(neo_ecc1.get_hexstr_keys())


	neo_ecc2 = NeoEccHandler()
	neo_ecc2.init_key(
	'04 8817A576A8B2076707057136A362A87B96F9A21F3DBF6864B3A7C06705C984FDA36EA822738FA1E49E2A1E4493EA681A87CA02B13B8963080EA171070FEC3AF2',
	'9862BB3DFAEF918D7D752E13ACB476774F0312947B7832EF36865EA74586B568')
	ret = neo_ecc2.make_ecdh_from_other(neo_ecc1)
	print(tohexstr(ret))

	exit()

	'E959787BF9367A1CE99266AFA13CBAE53C4CE3DE0810464D0477B6955258F482', '0CB68B7535F89653AB1B51B8A57F7340A151164E61B521179574128F0493AAB7818F4D45720EA88CA8487F520C97BB304E389363B6CAC2727431F6D81CAF4E98'
	multi_value("9862BB3DFAEF918D7D752E13ACB476774F0312947B7832EF36865EA74586B568",
	            "0018AC197BAE8B64985E2BC6D75083A1CD7D210C6D5ED4D2D6D53EE261AC494EF7D91FB89A8345D9393C988CCBFC03190D21B53A051B025DBF4F500EFD15D0D5")
#	exit()
	multi_value("9862BB3DFAEF918D7D752E13ACB476774F0312947B7832EF36865EA74586B568",
	            "6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296 4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5")
	#exit()
	ret2 = neo_ecc1.make_ecdh_from_other(neo_ecc2)
	print(ret,ret2)
	assert ret ==ret2

	exit()


	# neo_ecc1.verify('04 72CF56F5BF877DCF5823691682E9824C0B9742D1E0B41D288B478ECEF5218BAA1C484CBB848E449A6A5BCD4A686ECE676201073FD61241302BEB185C38E6E4BB',
	#                 '91F33CD73198E5CFD964C26B08FB3AB26A855F32B0435A2D0BA693EFBBA186ED',
	#                 'C42CB98ACE90A9BDD1F7824D3D673265966DC682A7F7E49BBFA20B4645EF456E',
	#                 '7F151C315A970F8028A94660AFE9748A22205E15558BFB0AF07C569953510F1C',
	#                 'B15E21A6B1D12A191BFAA96878EC6434A93DB7E00A8ACAF94746031F2E4CE5FD')

	neo_ecc1.do_test()
	exit()



import ctypes,os,sys
from comm.open_ssl_define import *
#print(os.path.abspath("libeay32.dll"))
def find_dll():
	for tmp in sys.path:
		if os.path.exists(tmp+"/libeay32.dll"):
			return tmp+"/libeay32.dll"
	return None

# folder = os.path.dirname(os.path.abspath(__file__))
# print(folder)


def get_function(hllDll,func_name,rettype,argtypes):
	function = getattr(hllDll, func_name)
	function.restype = rettype
	function.argtypes = argtypes
	return function



class BASE_STR(ctypes.Structure):
	def db_pointer(self):
		return ctypes.pointer(ctypes.pointer(self))

	def pointer(self):
		return ctypes.pointer(self)

class BIGNUM(BASE_STR):
	_fields_ = [
		('d', ctypes.POINTER(ctypes.c_int)),
		('top', ctypes.c_int),
		('dmax', ctypes.c_int),
		('neg', ctypes.c_int),
		('flags', ctypes.c_int),
	]
class ECDSA_SIG(BASE_STR):
	_fields_ = [
		('r', ctypes.POINTER(BIGNUM)),
		('s', ctypes.POINTER(BIGNUM)),
	]

BN_hex2bn = None
EC_POINT_point2hex = None
BN_bn2hex = None
EC_GROUP_new_by_curve_name = None
EC_KEY_new = None
EC_KEY_set_group = None
EC_KEY_generate_key = None
EC_KEY_check_key = None
EC_KEY_get0_public_key = None
EC_KEY_get0_private_key = None
BN_CTX_new = None
ECDSA_SIG_new = None
BN_bin2bn = None
ECDSA_do_verify = None
ERR_get_error = None
ERR_reason_error_string = None
ERR_error_string = None
ECDSA_SIG_free = None
BN_CTX_free = None
ECDSA_do_sign = None
EC_POINT_hex2point = None
EC_POINT_free = None
EC_KEY_set_public_key = None
EC_POINT_point2oct = None
EC_POINT_mul = None
EC_KEY_free = None
EC_POINT_new = None
BN_new = None
EC_KEY_set_private_key = None
BN_clear_free = None
#정의 되어 있어야..pycharm에서 코드에 빨간색이 안나옴....




def loading_ssl_functions(dist_map):
	dll_name = find_dll()
	print(dll_name)
	hllDll = ctypes.CDLL(dll_name)
	BN_hex2bn = get_function(hllDll,'BN_hex2bn',ctypes.c_int,[ctypes.POINTER(ctypes.POINTER(BIGNUM)) , ctypes.c_char_p])
	EC_POINT_point2hex = get_function(hllDll,'EC_POINT_point2hex',ctypes.c_char_p,[ctypes.c_void_p , ctypes.c_void_p , ctypes.c_int , ctypes.c_void_p])
	BN_bn2hex = get_function(hllDll,'BN_bn2hex',ctypes.c_char_p,[ctypes.POINTER(BIGNUM)])
	EC_GROUP_new_by_curve_name = get_function(hllDll,'EC_GROUP_new_by_curve_name',ctypes.c_void_p,[ctypes.c_int])
	EC_KEY_new = get_function(hllDll,'EC_KEY_new',ctypes.c_void_p,[])
	EC_KEY_set_group = get_function(hllDll,'EC_KEY_set_group',ctypes.c_int,[ctypes.c_void_p , ctypes.c_void_p])
	EC_KEY_generate_key = get_function(hllDll,'EC_KEY_generate_key',ctypes.c_int,[ctypes.c_void_p])
	EC_KEY_check_key = get_function(hllDll,'EC_KEY_check_key',ctypes.c_int,[ctypes.c_void_p])
	EC_KEY_get0_public_key = get_function(hllDll,'EC_KEY_get0_public_key',ctypes.c_void_p,[ctypes.c_void_p])
	EC_KEY_get0_private_key = get_function(hllDll,'EC_KEY_get0_private_key',ctypes.POINTER(BIGNUM),[ctypes.c_void_p])
	BN_CTX_new = get_function(hllDll,'BN_CTX_new',ctypes.c_void_p,[])
	ECDSA_SIG_new = get_function(hllDll,'ECDSA_SIG_new',ctypes.POINTER(ECDSA_SIG),[])
	BN_bin2bn = get_function(hllDll,'BN_bin2bn',ctypes.POINTER(BIGNUM),[ctypes.c_void_p , ctypes.c_int , ctypes.POINTER(BIGNUM)])
	ECDSA_do_verify = get_function(hllDll,'ECDSA_do_verify',ctypes.c_int,[ctypes.c_void_p , ctypes.c_int , ctypes.POINTER(ECDSA_SIG) , ctypes.c_void_p])
	ERR_get_error = get_function(hllDll,'ERR_get_error',ctypes.c_int,[])
	ERR_reason_error_string = get_function(hllDll,'ERR_reason_error_string',ctypes.c_char_p,[ctypes.c_int])
	ERR_error_string = get_function(hllDll,'ERR_error_string',ctypes.c_char_p,[ctypes.c_int , ctypes.c_char_p])
	ECDSA_SIG_free = get_function(hllDll,'ECDSA_SIG_free',None,[ctypes.POINTER(ECDSA_SIG)])
	BN_CTX_free = get_function(hllDll,'BN_CTX_free',None,[ctypes.c_void_p])
	ECDSA_do_sign = get_function(hllDll,'ECDSA_do_sign',ctypes.POINTER(ECDSA_SIG),[ctypes.c_void_p , ctypes.c_int , ctypes.c_void_p])
	EC_POINT_hex2point = get_function(hllDll,'EC_POINT_hex2point',ctypes.c_void_p,[ctypes.c_void_p , ctypes.c_char_p , ctypes.c_void_p , ctypes.c_void_p])
	EC_POINT_free = get_function(hllDll,'EC_POINT_free',None,[ctypes.c_void_p])
	EC_KEY_set_public_key = get_function(hllDll,'EC_KEY_set_public_key',ctypes.c_int,[ctypes.c_void_p , ctypes.c_void_p])
	EC_POINT_point2oct = get_function(hllDll,'EC_POINT_point2oct',ctypes.c_int,[ctypes.c_void_p , ctypes.c_void_p , ctypes.c_int , ctypes.c_void_p , ctypes.c_int , ctypes.c_void_p])
	EC_POINT_mul = get_function(hllDll,'EC_POINT_mul',ctypes.c_int,[ctypes.c_void_p , ctypes.c_void_p , ctypes.POINTER(BIGNUM) , ctypes.c_void_p , ctypes.POINTER(BIGNUM) , ctypes.c_void_p])
	EC_KEY_free = get_function(hllDll,'EC_KEY_free',None,[ctypes.c_void_p])
	EC_POINT_new = get_function(hllDll,'EC_POINT_new',ctypes.c_void_p,[ctypes.c_void_p])
	BN_new = get_function(hllDll,'BN_new',ctypes.POINTER(BIGNUM),[])
	EC_KEY_set_private_key = get_function(hllDll,'EC_KEY_set_private_key',ctypes.c_int,[ctypes.c_void_p , ctypes.POINTER(BIGNUM)])
	BN_clear_free = get_function(hllDll,'BN_clear_free',None,[ctypes.POINTER(BIGNUM)])
	list_function_name = ["BN_hex2bn", "EC_POINT_point2hex", "BN_bn2hex", "EC_GROUP_new_by_curve_name", "EC_KEY_new", "EC_KEY_set_group", "EC_KEY_generate_key", "EC_KEY_check_key", "EC_KEY_get0_public_key", "EC_KEY_get0_private_key", "BN_CTX_new", "ECDSA_SIG_new", "BN_bin2bn", "ECDSA_do_verify", "ERR_get_error", "ERR_reason_error_string", "ERR_error_string", "ECDSA_SIG_free", "BN_CTX_free", "ECDSA_do_sign", "EC_POINT_hex2point", "EC_POINT_free", "EC_KEY_set_public_key", "EC_POINT_point2oct", "EC_POINT_mul", "EC_KEY_free", "EC_POINT_new", "BN_new", "EC_KEY_set_private_key", "BN_clear_free",]

	map_loc = locals()
	for name in list_function_name:
		value = map_loc[name]
		dist_map[name] = value
		#


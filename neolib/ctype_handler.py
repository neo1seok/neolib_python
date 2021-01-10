import ctypes
import enum
import os
import sys


class CALLTYPE(enum.Enum):
	stdcall=0
	cdcall=1


def get_function(hllDll,func_name,rettype,argtypes):
	function = getattr(hllDll, func_name)
	function.restype = rettype
	function.argtypes = argtypes
	return function

def get_handle(dll_name, calltype=CALLTYPE.stdcall):
	if calltype == CALLTYPE.stdcall:
		hllDll = ctypes.windll.LoadLibrary(dll_name)

	elif calltype == CALLTYPE.cdcall:
		hllDll = ctypes.CDLL(dll_name)

	else:
		raise Exception("NO CALL TYPE")
	return hllDll

def load_functions(hllDll,dst_map,list_api_function):
	for api_name,rettype,argtype in list_api_function:
		dst_map[api_name] = get_function(hllDll, api_name, rettype, argtype)

def find_dll(dll_name):
	for tmp in sys.path:
		if os.path.exists(tmp+"/"+dll_name):
			return tmp+"/"+ dll_name
	return None

def main_load(dll_name, dist_map,list_api_function,calltype=CALLTYPE.stdcall):
	hllDll = get_handle(dll_name,calltype)
	load_functions(hllDll,dist_map,list_api_function)
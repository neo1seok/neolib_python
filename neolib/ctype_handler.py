import collections
import ctypes
from ctypes import *
from _ctypes import resize, sizeof
from ctypes import *

def get_function(hllDll,func_name,rettype,argtypes):
	function = getattr(hllDll, func_name)
	function.restype = rettype
	function.argtypes = argtypes
	return function

def get_handle(dll_name, calltype="stdcall"):
	if calltype == "stdcall":
		hllDll = ctypes.windll.LoadLibrary(dll_name)

	elif calltype == "cdcall":
		hllDll = ctypes.CDLL(dll_name)

	else:
		raise Exception("NO CALL TYPE")
	return hllDll

def load_functions(hllDll,dst_map,list_api_function):
	for api_name,rettype,argtype in list_api_function:
		dst_map[api_name] = get_function(hllDll, api_name, rettype, argtype)


def main_load(dll_name, dist_map,list_api_function,calltype="stdcall"):
	hllDll = get_handle(dll_name,calltype)
	load_functions(hllDll,dist_map,list_api_function)
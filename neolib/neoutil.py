

import types
# import xlrd
import subprocess
import logging
# import sys
#fdsdfasf
# import collections
import os
import re
# import  shutil
# import time
#
# import pymysql
# import  json
#
# import xlrd

import array
import json
import sys
import datetime

from neolib.hexstr_util import *
from logging import handlers
from neolib.file_util import *
#from neolib.general_import import *

class Struct:
	def __init__(self, **entries):
		self.__dict__.update(entries)

	def get_dict(self):
		return dict(self.__dict__)

	def from_dict(self,dict):
		self.__dict__.update(dict)





def executeAsync( cmd):
	fd = subprocess.Popen(cmd, shell=True,
						  stdin=subprocess.PIPE,
						  stdout=subprocess.PIPE,
						  stderr=subprocess.PIPE)
	return fd.stdout, fd.stderr

def listarg2Map(list):
	maparg = {}
	i = 0
	while i < len(list):
		value = list[i]


		if value.startswith("-"):
			value = re.sub("-","",value)
			print(value)
			nextvalue = list[i + 1] if i +1 < len(list) else ""
			nextvalue = "" if  nextvalue.startswith("-") else nextvalue

			maparg[value] = nextvalue


		i=i+1
	return maparg

def get_maps_from_args(argv):
	length = len(argv)
	#print(argv)

	maps = {tmp[1:]: '' for tmp in argv if tmp.startswith('-')}

	for key, val in maps.items():
		idx = argv.index('-' + key)
	#	print(idx)
		if idx + 1 >= length: continue
		if argv[idx + 1].startswith('-'): continue

		maps[key] = argv[idx + 1]
	return maps

def getMapsFromArgs(argv):
	return get_maps_from_args(argv)

def get_struct_from_args(argv):
	return Struct(**get_maps_from_args(argv))

#
# def HexString2ByteArray(hexstr) :
# 	return hexstr.
#
# def ByteArray2HexString(bytes,sep="") :
# 	return sep.join('{:02X}'.format(int(x)) for x in array.array('B', bytes))
# 	#return sep.join('{:02X}'.format(ord(x)) for x in bytes)
#
# def HexString2Text(hexstr,enc="utf-8") :
# 	return HexString2ByteArray(hexstr).decode(enc)
#
# def Text2HexString(str,enc="utf-8",sep="") :
# 	return ByteArray2HexString(str.encode(enc),sep)
#
#
# def tobytes(in_data):
# 	if type(in_data) == str:
# 		return HexString2ByteArray(in_data)
# 	if type(in_data) == bytes:
# 		return in_data
#
# def tohexstr(in_data):
# 	if type(in_data) == str:
# 		return in_data
# 	if types(in_data) == bytes:
# 		return ByteArray2HexString(in_data)


def deffilter(root,file):
	return  True

def listAllFile(basedir,filter=deffilter):
	listaa = []
	for root, dirs, files in os.walk(basedir):
		root = root.replace("\\","/")
		for file in files:
			if not filter(root,file): continue
			listaa.append((root,file))

	return listaa

def getExtNameFromPath(path):
	return os.path.splitext(path)[1]


def removeEmptyFolder(basedir):
	listaa = []
	while True:
		for root, dirs, files in os.walk(basedir):
			# print(root,len(files),len(dirs))
			sublen = len(files) + len(dirs)
			if sublen == 0: listaa.append(root)

		if len(listaa) == 0: return

		for tmp in listaa:
			# shutil.rmtree(tmp)
			print(tmp)
			os.rmdir(tmp)

			def removeEmptyFolder(basedir):
				listaa = []
				while True:
					for root, dirs, files in os.walk(basedir):
						# print(root,len(files),len(dirs))
						sublen = len(files) + len(dirs)
						if sublen == 0: listaa.append(root)

					if len(listaa) == 0: return

					for tmp in listaa:
						# shutil.rmtree(tmp)
						print(tmp)
						os.rmdir(tmp)


def get_safe_mapvalue(maparg,key,defvalue=''):
	if key in maparg:
		return maparg[key]
	return defvalue

def _linux_set_time(time_tuple):
	import ctypes
	import ctypes.util
	import time

	# /usr/include/linux/time.h:
	#
	# define CLOCK_REALTIME                     0
	CLOCK_REALTIME = 0

	# /usr/include/time.h
	#
	# struct timespec
	#  {
	#    __time_t tv_sec;            /* Seconds.  */
	#    long int tv_nsec;           /* Nanoseconds.  */
	#  };
	class timespec(ctypes.Structure):
		_fields_ = [("tv_sec", ctypes.c_long),
					("tv_nsec", ctypes.c_long)]

	librt = ctypes.CDLL(ctypes.util.find_library("rt"))

	ts = timespec()
	ts.tv_sec = int( time.mktime( datetime.datetime( *time_tuple[:6]).timetuple() ) )
	ts.tv_nsec = time_tuple[6] * 1000000 # Millisecond to nanosecond

	# http://linux.die.net/man/3/clock_settime
	librt.clock_settime(CLOCK_REALTIME, ctypes.byref(ts))


def create_logger(loggename,formatter = '%(threadName)s %(asctime)s - %(name)s - %(levelname)s - %(message)s',handler=None):
	'''
	formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
	'''
	if handler == None:
		handler = handlers.TimedRotatingFileHandler(filename="log.txt", when='D')

	#handler = handlers.TimedRotatingFileHandler(filename=loggename + ".txt", when='D')
	loggename = loggename
	# create logger
	logger = logging.getLogger(loggename)

	logger.setLevel(logging.DEBUG)

	# create console handler and set level to debug
	ch = logging.StreamHandler()
	ch.setLevel(logging.DEBUG)

	# create formatter
	formatter = logging.Formatter(formatter)

	# add formatter to ch
	ch.setFormatter(formatter)
	handler.setFormatter(formatter)
	# add ch to logger
	logger.removeHandler(ch)
	logger.removeHandler(handler)

	logger.addHandler(ch)
	logger.addHandler(handler)

	return logger

def json_pretty(json_obj):

	return json.dumps(json_obj, sort_keys=True, indent=4, separators=(',', ': '),ensure_ascii=False)

def get_data_from_file(filename):
	str = StrFromFile(filename)
	return json.loads(str)
def note_with_unit(bytes, unit='B'):
	KB = 1024
	tmpByte = float(bytes)
	prevByte = float(tmpByte)
	tuple_bunit = ("", "K", "M", "G", "T")
	count = 0
	while True:
		tmpByte /= KB
		if tmpByte < 1:
			break
		prevByte = tmpByte
		count += 1

	bunit = tuple_bunit[count]


	ret = "%.2f"%prevByte


	return ret + bunit+unit

def devide_by_unitsize(orgsize,unitsize):
	list_inputsize_per_loop = [unitsize for _ in range(int(orgsize / unitsize))]
	remain = orgsize % unitsize
	if remain > 0:
		list_inputsize_per_loop.append(remain)
	return list_inputsize_per_loop



def seperate_filter(hex_str_filter,org_hex_str_buff):
	return [ org_hex_str_buff[match.start(0):match.end(0)] for match in re.finditer(r'FF+',hex_str_filter)]


def imports():
	for name, val in globals().items():
		if isinstance(val, types.ModuleType):
			yield val.__name__

def get_ext_name_from_path(path):
	root,ext = os.path.splitext(path)
	return ext
if __name__ == '__main__':
	ext= get_ext_name_from_path("C:/app/PYTOOL/pythonshell.py")
	print(ext)
	exit()
	print(list(find_files("D:/PROJECT/GIANT/RELEASE/tcp_client_sample/giant_auth")))
	exit()
	print(devide_by_unitsize(1024+1,1024))
	print(note_with_unit(4400000000+4693331968))
	print(note_with_unit(1025))
	print(note_with_unit(0))


						# if __name__ != '__main__':
# 	exit()
#
# print(ConvStringForm(intype="und",outtype='cam').ConvertString("TEST_ABCCC_DDDD"))
# print(ConvStringForm(intype="spc",outtype='cam').ConvertString("TEST ABCCC DDDD"))
# print(ConvStringForm(intype="cam",outtype='und').ConvertString("TestAbhAaaAcc"))
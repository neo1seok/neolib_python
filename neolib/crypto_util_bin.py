from neolib import neoutil,neo_class
from neolib.neoutil import *
import hashlib
def fit_size(src,unit_size):
	real_size = len(src)
	if real_size < unit_size:
		return zero_padding(src, unit_size)
	return src[0:unit_size]

def sha256(bin_input):
	m = hashlib.sha256()
	m.update(bin_input)
	reshash = m.digest()

	return reshash

def sha1(bin_input):
	m = hashlib.sha1()
	m.update(bin_input)
	reshash = m.digest()

	return reshash
def zero_padding( src, unit_size):
	real_size = len(src)
	tailsize = real_size % unit_size
	remainsize = unit_size -tailsize
	return src+b'\x00' * (remainsize)



def restsize_padding( src, unit_size):
	real_size = len(src)
	tailsize = real_size % unit_size
	remainsize = unit_size -tailsize

	if(remainsize<0):
		remainsize = unit_size
	rmbyte = remainsize.to_bytes(1,'big')
	return src+rmbyte*(remainsize)

def restsize_repadding( src):
	lastidx = len(src)-1
	lastbyte = src[-1:]
	remainbytesize = int.from_bytes(lastbyte,"big")

	return src[:-remainbytesize]


def onebyte_padding( src, unit_size,bytevalue):
	real_size = len(src)
	tailsize = real_size % unit_size
	remainsize = unit_size -tailsize-1
	if(remainsize<0):
		remainsize = unit_size-1

	return src+bytevalue+b'\x00' * (remainsize)

def onebyte_repadding( src, bytevalue):
	lastidx = len(src)-1
	idx = src.rindex(bytevalue)
	dstidx = lastidx-idx+1
	return src[:-dstidx]



def bit_operation_template(buff_1,buff_2,operator):
	if len(buff_1) != len(buff_2):
		return None
	return bytes([ operator(buff_1[idx],buff_2[idx]) for idx in range(len(buff_1))])

def bit_single_operation_template(buff,operator):
	return bytes([ operator(bt) for bt in buff])

def calc_xor( buff_1,buff_2):
	#print(ByteArray2HexString(b1),ByteArray2HexString(b2))
	return bit_operation_template(buff_1,buff_2,lambda x,y:x^y)
	#return bytes([b1[idx] ^ b2[idx] for idx in range(len(b1))])

def calc_or( buff_1,buff_2):
	#print(ByteArray2HexString(b1),ByteArray2HexString(b2))
	return bit_operation_template(buff_1,buff_2,lambda x,y:x|y)

def calc_and( buff_1,buff_2):
	#print(ByteArray2HexString(b1),ByteArray2HexString(b2))
	return bit_operation_template(buff_1,buff_2,lambda x,y:x&y)


def calc_complement(buff):
	return bit_single_operation_template(buff,lambda x:(~x)&0xff)


if __name__ == '__main__':


	ret = restsize_padding("0123456789ABCDEF".encode(), 16)
	print(ByteArray2HexString(ret))
	repadd = restsize_repadding(ret)
	print(ByteArray2HexString(repadd))


	ret = restsize_padding("0123456789ABCDEF01".encode(), 16)
	print(ByteArray2HexString(ret))
	repadd = restsize_repadding(ret)
	print(ByteArray2HexString(repadd))

	repadd = restsize_repadding(ret)
	print(ByteArray2HexString(repadd))

	exit()


	ret = onebyte_padding("0123456789ABCDEF".encode(),16,b'\x80')
	print(ByteArray2HexString(ret))
	ret = onebyte_padding("0123456789ABCDEF01".encode(), 16, b'\x80')
	print(ByteArray2HexString(ret))
	repadd = onebyte_repadding(ret, b'\x80')
	print(ByteArray2HexString(repadd))

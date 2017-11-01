from neolib import neoutil,neo_class
import hashlib
import neolib.neoutil as neolib

#import neolib
import random

def sha256(hexstr_input):
	m = hashlib.sha256()
	m.update(neolib.HexString2ByteArray(hexstr_input))
	reshash = m.digest()

	return neolib.ByteArray2HexString(reshash)


def substr(org, index, count):
	return org[2 * index:2 * (index + count)]


def zerofill(count):
	return "00" * count;
def getrandom(size):
	return neolib.ByteArray2HexString(bytearray(random.getrandbits(8) for _ in range(size)))
def xor_calc(org, hashed_value):
	bhashed_value = neolib.HexString2ByteArray(hashed_value)
	borg = neolib.HexString2ByteArray(org)
	# print(org,hashed_value)
	# print(type(borg))
	new_value = b''
	idx = 0
	for bv in borg:
		calcb = bhashed_value[idx % 32]
		new_value+= bytes([bv^calcb])
		idx += 1

	return neolib.ByteArray2HexString(new_value)


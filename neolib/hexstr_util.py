import array

def HexString2ByteArray(hexstr) :
	return bytes.fromhex(hexstr)

def ByteArray2HexString(bytes,sep="") :
	return sep.join('{:02X}'.format(int(x)) for x in array.array('B', bytes))
	#return sep.join('{:02X}'.format(ord(x)) for x in bytes)

def HexString2Text(hexstr,enc="utf-8") :
	return HexString2ByteArray(hexstr).decode(enc)

def Text2HexString(str,enc="utf-8",sep="") :
	return ByteArray2HexString(str.encode(enc),sep)


def tobytes(in_data):
	if type(in_data) == str:
		return HexString2ByteArray(in_data)
	if type(in_data) == bytes:
		return in_data

def tohexstr(in_data):
	if type(in_data) == str:
		return in_data.replace(' ','')
	if type(in_data) == bytes:
		return ByteArray2HexString(in_data)
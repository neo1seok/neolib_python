import os

def StrFromFile(filepath,enc='utf-8'):


	fb = open(filepath,'rb')
	rt = fb.read()
	str = rt.decode(enc)
	fb.close()
	return str

def StrToFile(str,filepath,enc='utf-8'):
	fullpath = os.path.abspath(filepath)
	dir_name = os.path.dirname(fullpath)
	MakeDir(dir_name)

	fb = open(filepath,'wb')
	fb.write(str.encode(enc))
	fb.close()


def MakeDoubleListFromTxt(strtxt):
	strmenu = StrFromFile(strtxt)
	mapobj = map(lambda x: tuple(x.split('\t')), strmenu.split('\r\n'))
	return list(filter(lambda x: len(x) > 1, mapobj))

def MakeDir(path):
	if not os.path.exists(path):
		os.makedirs(path)

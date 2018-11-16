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


def find_files(base_path,is_filter=lambda tuple_path,etc_param:True ,etc_param=None, conv_result = lambda tuplepath,etc_param:tuplepath):
	'''
	이 함수는 특정 패스 밑에 모든 파일을 리커시브하게 읽어가며
	디텍트 하는 함수이다.
	**sample

base_path = "C:/APP/neolib_python"

def is_filter(tuple_arg,etc):
	base_path, path, dirs, tmpfile  =tuple_arg
	filename, file_extension = os.path.splitext(tmpfile)
	if file_extension.lower() != ".py":
		return False
	#print(base_path, path, dirs, tmpfile)
	return True

def conv_result(tuple_arg,etc):
	base_path, path, dirs, tmpfile = tuple_arg
	print(base_path, path, dirs, tmpfile)
	return path,tmpfile
ret = neoutil.find_files(base_path,is_filter=is_filter,conv_result=conv_result)
print(list(ret))

*****
	:param base_path:
	base_path,path,dirs,filename, = tuple_path
	:return:
	'''
	if base_path == '':
		base_path =os.getcwd()

	for path, dirs, files in os.walk(base_path):
		#print(path, dirs, files)
		path = path.replace('\\','/')
		for tmpfile in files:
			tuplepath = (base_path,path,dirs,tmpfile,)
		#	print(is_filter,is_filter(tuplepath,etc_param))
			if is_filter(tuplepath,etc_param):
				ret = conv_result(tuplepath,etc_param)
				yield ret


def find_files_simple(base_path,is_filter=lambda path_name:True ):
	'''
	이 함수는 특정 패스 밑에 모든 파일을 리커시브하게 읽어가며
	디텍트 하는 함수이다.
	**sample

base_path = "C:/APP/neolib_python"

def is_filter(tuple_arg,etc):
	base_path, path, dirs, tmpfile  =tuple_arg
	filename, file_extension = os.path.splitext(tmpfile)
	if file_extension.lower() != ".py":
		return False
	#print(base_path, path, dirs, tmpfile)
	return True


*****
	:param base_path:
	base_path,path,dirs,filename, = tuple_path
	:return:
	'''
	if base_path == '':
		base_path =os.getcwd()

	for path, dirs, files in os.walk(base_path):
		path = path.replace('\\','/')
		for tmpfile in files:
			subpath = path + "/" + tmpfile
			if is_filter(subpath):
				yield subpath


if __name__ == '__main__':
	coruoute = find_files_new(r'D:\down\zave\unscene')
	print(list(coruoute))
	#print(coruoute.__next__())

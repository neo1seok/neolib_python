
from neolib import neoutil,file_util,neo_class

ret = neoutil.HexString2ByteArray('aaaa')
neoutil.ByteArray2HexString(ret)


def isfilter(tuploepath,etc):
	print("isfilter",tuploepath)



	return False
	dir_name,filename = tuploepath

	print(ext_name)
	if ext_name == '.java':
		return True
	return False

class SampleRunnable(neo_class.NeoRunnableClass):
	def __init__(self):
		neo_class.NeoRunnableClass.__init__(self)

	def init_run(self):
		pass

	def do_run(self):
		pass

if __name__ == "__main__":
	SampleRunnable().run()

	pass


print(isfilter)
listfile = file_util.find_files('D:/PROJECT/toolrnd/GIANT_JAVA/giant_3/src/main/java',is_filter=isfilter)
print(list(listfile))
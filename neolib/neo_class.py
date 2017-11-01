

import queue
import threading
from threading import Lock
import datetime
import os
import shutil
import  time
import sys
import re

from neolib import neoutil
def move_exist_file(filename):
	if os.path.isfile(filename):
		shutil.move(filename, "log/"+filename + ".{0}.tmp".format(datetime.datetime.now().strftime("%Y%m%d.%H%M%S")))

class FakeLog:
	def __init__(self,logfile="log.txt"):
		self.queue = queue.Queue()

		self.lock = Lock()
		self.logfile = logfile
		move_exist_file(self.logfile)
		with open(logfile, "wb") as fp:
			fp.close()
		self.th = threading.Thread(target=self.run)
		self.is_run = False
		self.start()
	def start(self):
		self.th.start()
		self.is_run = True
	def stop(self):
		self.is_run = False


	def run(self):
		while True:
			qsize = self.queue.qsize()
			if qsize == 0:
				time.sleep(0.3)
				continue

			with open(self.logfile, "ab") as fp:
				for tmp in range(qsize):
					line = self.queue.get()
					write_msg = line +"\n"
					fp.write(write_msg.encode())
				fp.close()
			time.sleep(0.3)



	def write_message(self, title,msg):
		relamsg = "{0} {1} {2} {3}".format(datetime.datetime.now(),threading.current_thread().getName(),title, msg)
		write_msg = relamsg + "\n"
		self.queue.put(relamsg)
		# self.lock.acquire()
		#
		#
		# with open("log.txt", "ab") as fp:
		# 	fp.write(write_msg.encode())
		# 	fp.close()
		# self.lock.release()
		print(relamsg)
		None

	def write_org(self, title,fmt, *args):
		msg = fmt % args
		self.write_message(title,msg)
	def write_format(self, title,fmt, *args):
		msg = fmt.format(*args)
		self.write_message(title, msg)

	def debug(self, fmt, *args):
		self.write_org("DEBUG",fmt,*args)

	def debug_f(self, fmt, *args):
		self.write_format("DEBUG",fmt,*args)

	def error(self, errr):
		self.write_message("ERROR", errr)
class NeoRunnableClassOldStyle:
	isJustRunThisClass = True

	def __init__(self,**kwargs):
		self.mapArgs = {}
		self.maps = neoutil.getMapsFromArgs(sys.argv)
		self.setDefArges()


		print("__init__",self.__class__)

		self.mapArgs.update(self.defMapArgs)
		self.mapArgs.update(self.maps)
		for key,vlaue in kwargs.items():
			self.mapArgs[key] = vlaue

		self.init_local_set()

	def init_local_set(self):
		None
	def setDefArges(self):
		self.defMapArgs = {
			'exit': True,
		}

	def Run(self):

		try:
			self.exit = self.mapArgs['exit']
		except:
			self.exit = True

		self.InitRun()
		#try:
		self.doRun()

		self.outLog()

		#except Exception as inst:
		#	print(inst.args)
		#finally:
		self.endRun()


	def InitRun(self):
		None

	def doRun(self):
		None


	def outLog(self):
		None

	def endRun(self):

		if self.exit :exit()


class NeoAnalyzeClasss(NeoRunnableClassOldStyle):
	strlines = ""
	def SetClopBoard(self):
		None
	def outLog(self):
		fb = open('sample_xml.txt', 'wb')
		fb.write(self.strlines.encode())
		fb.close()
		self.SetClopBoard()
		#neolib4Win.SetClipBoard(self.strlines)
		None


class ConvStringForm:


	patttotal = r'([A-Za-z0-9_ ]+)(\t|\n|$)'
	pattcamel = r'([A-Za-z][a-z0-9]+)'
	#pattcamel = r'([A-Z][a-z0-9]*)'

	def __init__(self,**kwargs):
		self.maparg = kwargs
		self.InitValue()

	def InitValue(self):

		self.mapMakeArray = {
			"und": self.makeListFromUnderLine,
			"spc": self.makeListFromSpaceDiv,
			"cam": self.makeListFromCamelForm,
		}
		self.mapMakeString = {
			"und": self.convUnserLine,
			"und_row": self.convUnserLineLower,
			"cam": self.convCamelForm,

		}
		self.intype = ""
		self.outtype = ""

		if 'intype' in self.maparg:
			self.intype = self.maparg['intype']

		if 'outtype' in self.maparg:
			self.outtype = self.maparg['outtype']

		self.updateFunction()


		None

	def updateFunction(self):
		if self.intype != "":
			self.arrfunc = self.mapMakeArray[self.intype]

		if self.outtype != "":
			self.strfunc = self.mapMakeString[self.outtype]


	def convCamelForm(self,listarray):
		newarra = []
		for tmp in listarray:
			hd = tmp[0:1].upper()
			boddy = tmp[1:].lower()
			newarra.append(hd+boddy)
		return "".join(newarra)

	def convCamelForm(self,listarray):
		newarra = []
		for tmp in listarray:
			hd = tmp[0:1].upper()
			boddy = tmp[1:].lower()
			newarra.append(hd+boddy)
		return "".join(newarra)

	def convUnserLine(self, listarray):
		newarra = []
		for tmp in listarray:
			newarra.append(tmp.upper())
		return "_".join(newarra)

	def convUnserLineLower(self, listarray):
		return self.convUnserLine(listarray).lower()

	def makeListFromUnderLine(self, orgstr):
		return orgstr.split("_")

	def makeListFromSpaceDiv(self, orgstr):
		return orgstr.split(" ")

	def makeListFromCamelForm(self, orgstr):
		result = re.findall(self.pattcamel,orgstr)
		for tmp in result:
			print(tmp[1])
			None
		return  list(map((lambda n:n),result))



	def ConvertString(self,inputstring):
		self.updateFunction()
		return self.convertWord(inputstring)




	def convertWord(self,strword):
		array = self.arrfunc(strword)
		return self.strfunc(array)


class NeoRunnableClass:
	is_just_run_this_class = True

	def __init__(self, **kwargs):
		self.map_args = {}
		self.maps = neoutil.getMapsFromArgs(sys.argv)
		self.set_def_args()

		print("__init__", self.__class__)

		self.map_args.update(self.defMapArgs)
		self.map_args.update(self.maps)
		for key, vlaue in kwargs.items():
			self.map_args[key] = vlaue
		self.init()

	# def __init__(self):
	# 	None
	def init(self):
		None
	def set_def_args(self):
		self.defMapArgs = {
			'exit': True,
		}

	def run(self):
		try:
			self.exit = self.map_args['exit']
		except:
			self.exit = True

		self.init_run()
		self.do_run()
		self.out_log()
		self.end_run()

	def init_run(self):
		None

	def do_run(self):
		None

	def out_log(self):
		None

	def end_run(self):
		if self.exit: exit()

"""
from neolib import neo_class
class SampleRunnable(neo_class.NeoRunnableClass):
	def init_run(self):
		None

	def do_run(self):
		None


"""

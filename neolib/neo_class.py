
import datetime
import io
import logging
import os
import queue
import re
import shutil
import sys
import threading
import time
from threading import Lock

# from neolib import neoutil
import paho.mqtt.client as mqtt

from neolib import core_util, crypto_util_bin
from neolib.hexstr_util import tobytes, tohexstr


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
		pass


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
		self.maps = core_util.getMapsFromArgs(sys.argv)
		self.setDefArges()


		print("__init__",self.__class__)

		self.mapArgs.update(self.defMapArgs)
		self.mapArgs.update(self.maps)
		for key,vlaue in kwargs.items():
			self.mapArgs[key] = vlaue

		self.init_local_set()

	def init_local_set(self):
		pass
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
		pass

	def doRun(self):
		pass


	def outLog(self):
		pass

	def endRun(self):

		if self.exit :exit()


class NeoAnalyzeClasss(NeoRunnableClassOldStyle):
	strlines = ""
	def SetClopBoard(self):
		pass
	def outLog(self):
		fb = open('sample_xml.txt', 'wb')
		fb.write(self.strlines.encode())
		fb.close()
		self.SetClopBoard()
		#neolib4Win.SetClipBoard(self.strlines)
		pass


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


		pass

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
			pass
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
		self.str_arg_info = ""
		self.map_args = {}
		self.maps = core_util.getMapsFromArgs(sys.argv)
		self.set_def_args()

		#print("__init__", self.__class__)

		self.map_args.update(self.defMapArgs)
		self.map_args.update(self.maps)
		for key, vlaue in kwargs.items():
			self.map_args[key] = vlaue

		self.str_args =core_util.Struct(**self.map_args)
		self.init()

	# def __init__(self):
	# 	None
	def init(self):
		stream = io.StringIO()
		print("Enable args",file=stream)
		for key,val in self.map_args.items():
			print(key,":",val,file=stream)
		self.str_arg_info = stream.getvalue()

		pass
	def set_def_args(self):
		self.defMapArgs = {
			'exit': False,
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
		pass

	def do_run(self):
		pass

	def out_log(self):
		pass

	def end_run(self):
		if self.exit: exit()

class WhileTemplate():

	def __init__(self,main_param, total_size, unit_size):



		#self.prcess_filter = lambda *args: (self.main_param, self.iter, self.buff_index, self.real_size)

		self.main_param = main_param
		self.unit_size = unit_size
		self.total_size = total_size
		self.remain_size = self.total_size

		self.buff_index = 0

		self.iter = 0
		# print(locals().keys())
		self.real_size = 0
		self.do_run()

	def prcess_filter(self, *args):
		return  (self.main_param, self.iter, self.buff_index, self.real_size)
	def def_process(self,*args):
		return None
	def process_init(self,*args):
		return None
	def process_end(self,*args):
		return None
	def process(self,*args):
		n, iter, idx, size = args
		return n[idx:idx + size]

	def do_run(self):
		self.list_ret = []
		args = self.prcess_filter()
		ret_process = self.process_init(*args)

		if ret_process != None:
			self.list_ret.append(ret_process)

		while self.remain_size > 0:
			self.real_size = min(self.remain_size, self.unit_size)
			args = self.prcess_filter()
			ret_process = self.process(*args)
			try:
				if ret_process == None:
					break
				self.list_ret.append(ret_process)
			finally:
				self.remain_size -= self.unit_size
				self.buff_index += self.unit_size
				self.iter += 1
		args = self.prcess_filter()
		ret_process = self.process_end(*args)
		if ret_process != None:
			self.list_ret.append(ret_process)

		return self.list_ret
	def get_result(self):
		return self.list_ret

class SampleWhileTemplate(WhileTemplate):
	def process_init(self,*args):
		n, iter, idx, size,unit_size = args
		return None
	def prcess_filter(self, *args):
		return  (self.main_param, self.iter, self.buff_index, self.real_size,self.unit_size)

	def process(self,n, iter, idx, size,unit_size):
		#n, iter, idx, size,unit_size = args
		return n[idx:idx + size]


def sample_while():
	sample_buff = "0123456789"*10
	print(sample_buff)
	prcess_filter = lambda struct_local: (
	struct_local.main_param, struct_local.iter, struct_local.buff_index, struct_local.real_size)
	prcess = lambda n, iter,idx, size: n[idx:idx + size]

	list_ret = SampleWhileTemplate(sample_buff,len(sample_buff),10).get_result()
	print(list_ret)

class NeoByteIO(io.BytesIO):
	def read_to_int(self,size,byteorder= 'big'):
		buff = self.read(size)
		return int.from_bytes(buff,byteorder)



class NeoAltBytes():
	def __init__(self, org,sep="",enc='utf-8',conv='lower'):
		self.org = tobytes(org)
		self.sep = sep
		self.enc = enc
		#self.conv = conv
		self.conv = lambda a_:a_.lower() if conv == "lower" else a_.upper()
		#print(self.conv)
		#self.conv = lambda a_: a_.upper()

	@property
	def bytes(self):
		return self.org

	@property
	def hexstr(self):
		tohexstr(self.org)

		return self.conv(tohexstr(self.org))

	@property
	def ascii(self):
		return self.org.decode(encoding=self.enc)

	def __str__(self):
		return self.hexstr
"""
from neolib import neo_class
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

"""


class MqttHandler(NeoRunnableClass):
	def init(self):

		self.option = self.map_args.get("option",{})
		self.is_tls = self.map_args.get("is_tls",False)
		self.host = self.map_args.get("host", 'localhost')
		self.port = self.map_args.get("port", 1883)
		self.log_name = self.map_args.get("log_name", 'log')
		self.list_topics = self.map_args.get("list_topics", [])
		self.client_id = self.map_args.get("client_id", None)
		if self.client_id is None:
			self.client_id ="cli_"+tohexstr(crypto_util_bin.getrandom(16))

		self.on_cutom_message = self.map_args.get("on_message", None)
		if not self.on_cutom_message:
			self.on_cutom_message = lambda client, userdata, msg:print('#############',client, userdata, msg)

		self.logger = logging.getLogger(self.log_name)
		self.logger.info(f"cur class {self.__class__.__name__}")
		#client_id = "cli_"+tohexstr(crypto_util_bin.getrandom(16))
		self.client = mqtt.Client(client_id=self.client_id, protocol=mqtt.MQTTv31)
		self.is_connected = False
		pass

	def init_run(self):

		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message
		self.client.on_disconnect = self.on_disconnect

		if self.is_tls:
			self.logger.debug(f"tls_set {self.option}")
			self.client.tls_set(**self.option)
			self.client.tls_insecure_set(True)
		self.logger.info(f"connecting  {self.host} {self.port} is_tls: {self.is_tls}")
		self.client.connect(self.host, self.port, 60)
	def do_run(self):
		pass

	def on_connect(self,client, userdata, flags, rc):
		self.logger.info(f"Connected with result code {client} {self.host} {self.port}  " + str(rc))

		# Subscribing in on_connect() means that if we lose the connection and
		# reconnect then subscriptions will be renewed.
		# client.subscribe("$SYS/#")
		for sub in self.list_topics:
			client.subscribe(sub)
			self.logger.info(f"subscribed :{sub}")
		self.is_connected = True
		# client.subscribe(mqtt_topic_detail)
		# client.subscribe(mqtt_sample)
		# client.subscribe(onem2m_topic)
		# client.subscribe(onem2m_topic_res)

	def on_disconnect(self,client, userdata, rc):
		self.logger.info(f"on_disconnect with result code {client}  {userdata} {rc}")
		self.client.disconnect()


	def on_message(self,client, userdata, msg):
		# print(msg.topic + " ########" + msg.payload.decode())
		self.logger.info(f"SUBS####:topic:{msg.topic} messge:{msg.payload.decode()}")
		if msg.topic in self.list_topics:
			#print(msg.topic + " ########" + msg.payload.decode())
			#self.logger.info(f"SUBS####:topic:{msg.topic} messge:{msg.payload.decode()}")
			self.on_cutom_message(client, userdata, msg)

	def publish(self,topic,messge):

		self.logger.info(f"PUB####:topic:{topic} messge:{messge}")
		self.client.publish(topic, messge)

	def loop_forever(self):
		self.client.loop_forever()
	# client.publish("paho/fuck3", "echo:"+msg.payload.decode())
# elif msg.topic == mqtt_topic_detail:
# 	print(msg.topic+" ########"+msg.payload.decode())
# 	logger.info(f"payload:{msg.payload.decode()}")
# elif msg.topic == mqtt_sample:
# 	print(msg.topic + " ########" + msg.payload.decode())
# 	logger.info(f"payload:{msg.payload.decode()}")
# elif msg.topic == onem2m_topic_res:



if __name__ == '__main__':
	inst = NeoAltBytes(b"\x31\x3f", conv='upper')
	#inst = NeoAltBytes(b"\x31\x3f", conv='lower')

	print(inst.hexstr)

	pass
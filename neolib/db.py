import collections
import json
import re
# from  threading import *
import sqlite3
import threading
import time
from typing import List

import pymysql
import xlrd

import neolib.neoutil as neolib
from neolib import neoutil, neo_class


def makeMapMapDBFromListMapDB(key,listMapDB):
	return collections.OrderedDict([(tmprow[key],tmprow ) for tmprow in listMapDB])

class dbHandleing:
	sqldstfmt = "INSERT INTO {0} (   seq  ,{1}_uid  ,{2}  ,updt_date  ,reg_date  ) VALUES \n{3}"
	# 0:table 1:prefix 2:col araay 3:values
	sqlvalueContents = "({1}  ,'{0}_{1}',{2},now(),now())"

	def __init__(self,**kwargs):
		self.conn = pymysql.connect(**kwargs)
		self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
		self.lock = threading.Lock()







	def select(self,sql):
		#print(sql)
		self.execute(sql)
		return self.cur.fetchall()

	def select_to_map(self, key, sql):
		return self.makeMapMapDBFromListMapDB(key,self.select(sql))

	def execute(self,sql):
		print(sql)
		self.lock.acquire()  # will block if lock is already held
		try:
			self.cur.execute(sql)
		finally:
			self.lock.release()



	def lastSeq(self,tablename):

		sql = "SELECT seq FROM {0} order by seq desc limit 1 ;".format(tablename)
		mapres = self.select(sql)
		if len(mapres) == 0: return 0

		return int(mapres[0]['seq'])

	def insert(self,table,prefix,maprow,lastseq):
		return self.insertList(table,prefix,[maprow],lastseq)



	def insertList(self,table,prefix,listmaprow,lastseq):
		if len(listmaprow)  == 0: return
		maprow = listmaprow[0]

		arraycol = [key if key != 'index' else '`index`' for key,vlaue in maprow.items()]

		lastseq+=1




		# 0:prefix 1:seq 2: values
		iter_temp = iter(listmaprow)
		remain_size = len(listmaprow)


		while remain_size>0:
			values = []
			sub_list = [next(iter_temp) for tmp in range(min(1000,remain_size))]
			remain_size -= len(sub_list)
			print("remain_size:{} ".format(remain_size))

			for maprow in sub_list:
	#			arrayval = list(map(self.mapfunction,maprow.items()))
				arrayval = ["'%s'" % vlaue for key, vlaue in maprow.items()]

				values.append(self.sqlvalueContents.format(prefix,lastseq,",".join(arrayval)))
				lastseq+=1

			sql = self.sqldstfmt.format(table,prefix,",".join(arraycol),",\n".join(values))
			print(sql)
			self.execute(sql)
		return lastseq

	def mapfunction(self, tmp):
		key, value = tmp

		if type(value) == str:
			#print(type(value))
			value = value.replace("'", "\\'")
		return "'%s'" % value

		#0:table 1:prefix 2:seq 3:col araay 4:values

		sql = sqldstfmt.format(table,prefix,lastseq,",".join(arraycol),",".join(arrayval))

		self.execute(sql);


		return lastseq+1

	def deleteTable(self,table):
		self.execute('DELETE FROM %s;'%table)

	def conv_json_to_db_input(self,json_object, ensure_ascii=False):
		ret = json.dumps(json_object, ensure_ascii=ensure_ascii)
		return ret.replace('\\', '\\\\')

class dbHandleingSQLite3(dbHandleing):
	sqlvalueContents = "({1}  ,'{0}_{1}',{2},datetime('now'),datetime('now'))"

	def dict_factory(self,cursor, row):
		d = {}
		for idx, col in enumerate(cursor.description):
			d[col[0]] = row[idx]
		return d


	def __init__(self,**kwargs):
		database = kwargs['db']

		self.conn = sqlite3.connect(database)
		#self.conn.row_factory = sqlite3.Row
		self.conn.row_factory =	self.dict_factory
		self.cur = self.conn.cursor()
		self.lock = threading.Lock()
	def execute(self,sql):
		print(sql)
		self.lock.acquire()  # will block if lock is already held
		try:
			self.cur.execute(sql)
			self.conn.commit()
		finally:
			self.lock.release()

	def conv_json_to_db_input(self,json_object, ensure_ascii=False):
		ret = json.dumps(json_object, ensure_ascii=ensure_ascii)
		return ret


class BaseMySQLRunnable():

	dsttable = "";
	prefix = ""
	colline = ""
	dispalaytitle ="시나리오 상태"

	def setDefArges(self):
		super(BaseMySQLRunnable, self).setDefArges()
		self.defMapArgs.update({'dbaddress': 'localhost'})
		self.defMapArgs.update({'deleteTable': True})


	def InitRun(self):


		self.dbaddress = self.mapArgs['dbaddress']
		self.listmap = []

		print("dst db:"+self.dbaddress)

		self.dstdbHD = dbHandleing(host=self.dbaddress, port=3306, user='ictk', passwd='#ictk1234',	  db='adts', charset='utf8')
		None


	def endRun(self):
		self.dstdbHD.conn.close()
		neo_class.NeoRunnableClassOldStyle.endRun(self)


	def mainProcess(self):
		None


	def append(self, str):
		print(str)
		self.strlines += str

		self.strlines += "\n"

	def appendA(self, *args,**kwargs):

		self.strlines += '\t'.join(args)
		print(self.strlines)

		self.strlines += "\n"


	sentencepatt = r'G([0-9]+):(F|T):([0-9A-Za-z가-힣^.,_$=\-+()*\^ ]*)\^\\'


	def getValue(self, key, maps):
		if key not in maps: return ''
		return maps[key]


	def appendLine(self, **kwargs):
		mapresult = collections.OrderedDict()
		for tmp in self.cols:
			mapresult[tmp] = ''

		for key,value in kwargs.items():
			if type(value) == str:
				value = value.replace("'", "\\'")
			mapresult[key] = value

		self.listmap.append(mapresult)

	def doRun(self):
		self.strlines = ""
		if self.mapArgs['deleteTable'] :
			self.deleteTable()


		self.cols = re.split(r',\s*',self.colline)
		self.listmap = []


		self.processInserValues()

		# for row in self.listmap:
		# 	print(row)

		self.processInserToDB()

		self.processAfterDB()

		time.sleep(0.3)


		None



	def deleteTable(self):
		self.dstdbHD.deleteTable(self.dsttable)

	def processInserValues(self):
		None

	def processInserToDB(self):
		lastseq = self.dstdbHD.lastSeq(self.dsttable)
		self.dstdbHD.insertList(self.dsttable, self.prefix, self.listmap, lastseq)

	def processAfterDB(self):
		None


class MakeCreateTableFor(neo_class.NeoRunnableClassOldStyle,neo_class.NeoRunnableClass):
	createTableForm ="""

CREATE TABLE `{table_name}` (
{list_column_info}
PRIMARY KEY ({list_pki})
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
	"""
#0:tablename 1:fields info 2:pri key array

	fieldForm ="	`{name}` {type} {null_info} COMMENT '{comment}',"
#0:name 1:type 2:null type 3:comment

	procedure_form = """
#################################	
#table:{table_name}
#DROP PROCEDURE IF EXISTS insert_{table_name};
#DELIMITER $$
CREATE PROCEDURE insert_{table_name}
({csv_param_infos} , OUT _cur_seq INT,OUT _cur_uid varchar(20))

BEGIN

  
	DECLARE exit handler for SQLEXCEPTION
	  BEGIN
		ROLLBACK;        
		SET _cur_seq = -1;  
        SET _cur_uid = NULL;  
    
	END;
  
  SET _cur_seq := (SELECT MAX(seq)+1 FROM {table_name});
   IF(_cur_seq IS NULL) THEN
        SET _cur_seq = 1;
    END IF;
  set _cur_uid = concat('{prefix}','_',_cur_seq);  
 	START TRANSACTION;
		INSERT INTO {table_name} ( {csv_culumns})
		VALUE(_cur_seq,_cur_uid, {csv_params}, now(),now(),'');		

	COMMIT;
	
END
#$$DELIMITER ;




	"""
#table_name,csv_param_infos,csv_culumns,csv_params

	xlsDbFile = "rsc/TABLE정보.xlsx"

	dropTableForm = """
	DROP TABLE if EXISTS {table_name};
	"""
	drop_procedure_form = """
	DROP PROCEDURE if EXISTS insert_{table_name};
	"""
	def makeMapFromDoubllist(self,ret):
		maplist =  collections.OrderedDict()
		listaa = []
		for tmp in ret:
			if tmp[0] != '':
				listaa = []
				maplist[tmp[0]] = listaa
			print(tmp)
			listaa.append(tuple(tmp[1:6]))
		return maplist

	def makeMapFromTxt(self,strtxt):
		ret = neolib.MakeDoubleListFromTxt(strtxt)

		return  self.makeMapFromDoubllist(ret)

	def makeMapFromExcel(self,srcxlsfile):



		#fname = 'D:/PROJECT/toolrnd/DeviceTesterSystem/DOCS/DB설계서_161107.xlsx'

		# Open the workbook


		xl_workbook = xlrd.open_workbook(srcxlsfile)
		sheet_names = xl_workbook.sheet_names()
		print('Sheet Names', sheet_names)
		xl_sheet = xl_workbook.sheet_by_name('TABLE정보')
		print('Sheet name: %s' % xl_sheet.name)

		rows = [tmp for tmp in xl_sheet.get_rows()][3:]


		ret = [ tuple([tmp.value for tmp in row][1:]) for row in rows]

		return self.makeMapFromDoubllist(ret)



	def do_run(self):
		ret = self.makeMapFromExcel(self.xlsDbFile)
		self.strlines = self.makeSqlDropAndCreate(ret, self.createTableForm, self.fieldForm)
		neolib.StrToFile(self.strlines, "adts/TABLE.SQL")
		self.strlines = self.makeSqlDropAndCreate(ret, self.dropTableForm, '')
		neolib.StrToFile(self.strlines, "adts/DROP.SQL")

		None

	def doRun(self):
		self.do_run()

	def convType(self,row):
		name, type, nullinfo, comment, pki = row
		return self.fieldForm.format(name, type, nullinfo, comment)

	def makeSqlDropAndCreate(self,ret,mainFmt,fieldForm):


		strlines = ""
		for key, fields in ret.items():

			#listpki = ["`"+name +"`" for name, type, nullinfo, comment, pki in filter(lambda x: x[4] == 'PRI', fields)]
			listpki = ["`" + name + "`" for name, type, nullinfo, comment, pki in fields if pki == 'PRI']
			#filter(lambda x: x[4] == 'PRI', fields)]
			listmethod = [fieldForm.format(name=name, type=type, null_info=nullinfo, comment=comment)  for name, type, nullinfo, comment, pki in fields]
			#listmethod = list(map(self.convType, fields))
			#neoutil.Struct(dict(table=key.lower(),list_pki=",".join(listpki),list_column_info= "\n".join(listmethod)))
			strlines += mainFmt.format(table_name=key.lower(),list_pki=",".join(listpki),list_column_info= "\n".join(listmethod))

		return strlines
	def conv_struct(self,list_fields)->List[neoutil.Struct]:
		return [ neoutil.Struct(name=name, type=type, null_info=null_info, comment=comment, pki=pki) for name, type, null_info, comment, pki in list_fields]

	def make_insert_procedure(self, ret ):
		strlines = ""
		for table_name, list_fields in ret.items():
			list_struct = self.conv_struct(list_fields)
			uid_name = list_struct[1].name
			prefix = uid_name.replace("_uid","")
			list_no_using_col_nmae = ['seq',uid_name,"updt_date","reg_date","comment"]

			for obj in list_struct:
				obj.encoding = ""
				if 'text' in obj.type or 'varchar' in obj.type:
					obj.encoding = "CHARSET utf8"

			csv_param_infos=",".join([ "in _{name} {type} {encoding}".format(**obj.get_dict()) for obj in list_struct if obj.name not in list_no_using_col_nmae])
			csv_culumns=",".join([ "{name}".format(**obj.get_dict()) for obj in list_struct ])
			csv_params=",".join([ "_{name}".format(**obj.get_dict()) for obj in list_struct if obj.name not in list_no_using_col_nmae])

			strlines += self.procedure_form.format(**locals())

		return strlines





		None
"""
MakeDataFieldsClass
해당 클래스는 C# 프로젝트 내에 datafield 클래스 문자열 만들어 주는 클래스 이다.
tableList.txt 파일 은 테이블 , 필드 이름과 타입 정보가 들어 있는데(이는 엑셀로 부터 뭍여 오기 한것임)
여기서 클래스이름을 키로 하고 필드이름 과 타입정보를 한 튜플을 배열화 한 맵정보를 만들고
이를 다시 C#에서 사용 가능한 클래스의 문자열로 만들어 sample_xml.txt와
클립보드에 넣어 주는 클래스 이다.
 """
class MakeDataFieldsClass(MakeCreateTableFor):
	fmtclassForm = "public class {0} \n{{\n{1} \n}}\n"
	#0:classname 1:fields list

	fmtfieldForm = "\tpublic {0} {1} {2};"
	#0:typename 1:fieldname 2: initial



	def convert(self):
		def convType(row ):
			name, type, nullinfo, comment,pki = row
			newtype = 'string'
			strinit = '= ""'
			result = re.match(r'int\(\d+\)',type)
			if result != None :
				newtype = 'int'
				strinit = ''
			if type == 'datetime':
				newtype = 'DateTime'
				strinit = '= DateTime.Now'



			return self.fmtfieldForm.format(newtype,name,strinit)
		#ret = self.makeMapFromTxt("adts/tableList.txt")
		ret = self.makeMapFromExcel(self.xlsDbFile)


		print(ret)
		self.strlines = ''
		classconv = neo_class.ConvStringForm(intype='und', outtype='cam')
		for key, fields in ret.items():
			#listmethod = ["\tpublic string %s ;" % name for name,type in fields]

			listmethod = list(map(convType,fields))
			classname = classconv.ConvertString(key)
			self.strlines += self.fmtclassForm.format(classname, "\n".join(listmethod))

	def doRun(self):

		self.convert();
		# print(str)
		# fb = open('sample_xml.txt', 'wb')
		# fb.write(str.encode())
		# fb.close()
		#
		# neolib4Win.SetClipBoard(str)


class SampleCreateTableAnd(MakeCreateTableFor):
	xlsDbFile = "rsc/TABLE정보.xlsx"
	def do_run(self):
		ret = self.makeMapFromExcel(self.xlsDbFile)
		self.strlines = self.makeSqlDropAndCreate(ret,self.createTableForm,self.fieldForm)
		neolib.StrToFile(self.strlines, "table/TABLE.SQL")
		self.strlines = self.makeSqlDropAndCreate(ret, self.dropTableForm, '')
		neolib.StrToFile(self.strlines, "table/DROP.SQL")
		self.strlines = self.make_insert_procedure(ret)
		neolib.StrToFile(self.strlines, "table/PROCEDURE.SQL")

if __name__ == "__main__":
	SampleCreateTableAnd().run()
	pass
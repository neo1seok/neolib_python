from typing import List

from neolib import neoutil,neo_class
import xlrd
import  collections
def get_shee_names_from_xls(xls_file:str)->list:
	xl_workbook = xlrd.open_workbook(xls_file)
	sheet_names = xl_workbook.sheet_names()
	return sheet_names

def get_lines_from_xls_template_multi(xls_file:str,list_sheet_filter:iter)->list:
	xl_workbook = xlrd.open_workbook(xls_file)
	list_ret = []
	for get_sheet, comp,filter in list_sheet_filter:
		xl_sheet =  get_sheet(xl_workbook,comp)
		rows = [tmp for tmp in xl_sheet.get_rows()]
		lines = [tuple([tmp.value for tmp in row]) for row in rows]
		list_ret.append(filter(lines))
	return list_ret


def get_lines_from_xls_template(xls_file,get_sheet,comp,filter):
# 	xl_workbook = xlrd.open_workbook(xls_file)
# 	xl_sheet =  get_sheet(xl_workbook)
# #	xl_sheet = xl_workbook.sheet_by_name(sheetname)
#
# 	rows = [tmp for tmp in xl_sheet.get_rows()]
#
# 	lines = [tuple([tmp.value for tmp in row]) for row in rows]

	return get_lines_from_xls_template_multi(xls_file,[(get_sheet,comp,filter)])[0]


def get_lines_from_xls(xls_file,sheetname,filter=lambda lines:lines):
	return get_lines_from_xls_template(xls_file,lambda xl_workbook,cmp:xl_workbook.sheet_by_name(cmp),sheetname,filter)


def get_lines_from_xls_by_index(xls_file, index=0, filter=lambda lines:lines):
	return get_lines_from_xls_template(xls_file, lambda xl_workbook,comp: xl_workbook.sheet_by_index(comp),index, filter)


def convert_map_form_lines(list_lines,title_filter = lambda title:title):
	title_name = list_lines[0]
	return [{title_filter(title_name[idx]): col for idx, col in enumerate(line)} for line in list_lines[1:]]


def get_list_map_from_xls(xls_file, sheetname,filter=lambda lines:lines,title_filter = lambda title:title):
	return convert_map_form_lines(get_lines_from_xls(xls_file, sheetname,filter))


def get_list_map_from_xls_by_index(xls_file, list_index,filter=lambda lines:lines,title_filter = lambda title:title):
	return convert_map_form_lines(get_lines_from_xls_by_index(xls_file, list_index,filter))

def convert_struct_form_lines(list_lines:list,title_filter = lambda title:title)->List[neoutil.Struct]:
	title_name = list_lines[0]
	return [neoutil.Struct(**{title_filter(title_name[idx]): col for idx, col in enumerate(line)}) for line in list_lines[1:]]


def get_list_struct_from_xls(xls_file:str, sheetname,filter=lambda lines:lines,title_filter = lambda title:title)->List[neoutil.Struct]:
	return convert_struct_form_lines(get_lines_from_xls(xls_file, sheetname,filter))


def get_list_struct_from_xls_by_index(xls_file:str, list_index,filter=lambda lines:lines,title_filter = lambda title:title)->List[neoutil.Struct]:
	return convert_struct_form_lines(get_lines_from_xls_by_index(xls_file, list_index,filter))



# xl_workbook = xlrd.open_workbook(xls_file)
	# xl_sheet = xl_workbook.sheet_by_index(index)
	#
	# rows = [tmp for tmp in xl_sheet.get_rows()]
	# lines = [tuple([tmp.value for tmp in row]) for row in rows]
	# return filter(lines)

def get_list_lines_from_xls(xls_file,list_sheetname):
	return get_lines_from_xls_template_multi(xls_file,[ (lambda xl_workbook,comp:xl_workbook.sheet_by_name(comp) ,sheetname,lambda lines:lines) for sheetname in list_sheetname])

def get_list_lines_from_xls_by_index(xls_file,list_index):
	return get_lines_from_xls_template_multi(xls_file,[ (lambda xl_workbook,comp:xl_workbook.sheet_by_index(comp) ,index,lambda lines:lines) for index in list_index])



def fill_emptycell_from_prevrowcell(lines,*cols):
	list_row=[]
	global curcel
	curcel = ''
	def fill_cell(lines,rowindex,colindex):
		global curcel
		cellvalue = lines[rowindex][colindex]
		if rowindex==0 or cellvalue != '':
			curcel = cellvalue
			return cellvalue
		return curcel
	for colindex in cols:
		rows = [(colindex,rowindex, fill_cell(lines,rowindex,colindex)) for rowindex in range(len(lines))]
		list_row.extend(rows)
	for col,row,value in  	list_row:
		lines[row][col] = value


	#print(list_row)
	return [tuple(line)for line in lines]

def make_map_lines_from_filled_lines(lines, keyindex):
	maplist =  collections.OrderedDict()
	for line in lines:
		key = line[keyindex]
		if key not in maplist:
			maplist[key] =[]
		maplist[key].append(line)
	return  	maplist

def view_simple_lines(lines):
	for tmp in lines:
		print(tmp)

if __name__ == "__main__":
	ret = get_list_struct_from_xls("D:/PROJECT/GIANT_3/SRC/py_giant3/c_api/rsc/tls_api.xlsx","API")
	for tmp in ret:
		print(tmp.get_dict())
	print(ret)
	exit()

	ret = get_lines_from_xls_by_index("D:/PROJECT/GIANT_3/SRC/py_giant3/c_api/rsc/tls_api.xlsx", 0)
	print(ret)

	ret =get_list_lines_from_xls("D:/PROJECT/GIANT_3/SRC/py_giant3/c_api/rsc/tls_api.xlsx",["API","CONVERT"])
	neoutil.simple_view_list(ret)

	ret =get_list_lines_from_xls_by_index("D:/PROJECT/GIANT_3/SRC/py_giant3/c_api/rsc/tls_api.xlsx",[0,1])
	neoutil.simple_view_list(ret)

	pass
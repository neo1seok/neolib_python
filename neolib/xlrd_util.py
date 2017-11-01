from neolib import neoutil,neo_class
import xlrd
import  collections
def get_shee_names_from_xls(xls_file):
	xl_workbook = xlrd.open_workbook(xls_file)
	sheet_names = xl_workbook.sheet_names()
	return sheet_names

def get_lines_from_xls_template(xls_file,get_sheet,filter):
	xl_workbook = xlrd.open_workbook(xls_file)
	xl_sheet =  get_sheet(xl_workbook)
#	xl_sheet = xl_workbook.sheet_by_name(sheetname)

	rows = [tmp for tmp in xl_sheet.get_rows()]

	lines = [tuple([tmp.value for tmp in row]) for row in rows]

	return filter(lines)


def get_lines_from_xls(xls_file,sheetname,filter=lambda lines:lines):
	return get_lines_from_xls_template(xls_file,lambda xl_workbook:xl_workbook.sheet_by_name(sheetname),filter)

	#
	# xl_workbook = xlrd.open_workbook(xls_file)
	# xl_sheet = xl_workbook.sheet_by_name(sheetname)
	#
	# rows = [tmp for tmp in xl_sheet.get_rows()]
	# lines = [tuple([tmp.value for tmp in row]) for row in rows]
	# return filter(lines)
def get_lines_from_xls_by_index(xls_file, index=0, filter=lambda lines:lines):
	return get_lines_from_xls_template(xls_file, lambda xl_workbook: xl_workbook.sheet_by_index(index), filter)

	# xl_workbook = xlrd.open_workbook(xls_file)
	# xl_sheet = xl_workbook.sheet_by_index(index)
	#
	# rows = [tmp for tmp in xl_sheet.get_rows()]
	# lines = [tuple([tmp.value for tmp in row]) for row in rows]
	# return filter(lines)

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


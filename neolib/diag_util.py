from neolib import neoutil,neo_class
from neolib import  xlrd_util,neoutil
import collections
import re
def make_map_uids(srcxlsfile ,table_list_tab_name):
	lines = xlrd_util.get_lines_from_xls_by_index(srcxlsfile, 0, lambda lines :[list(line[1:]) for line in lines[3:]])
	lines = xlrd_util.fill_emptycell_from_prevrowcell(lines ,0)
	map_lines = xlrd_util.make_map_lines_from_filled_lines(lines, 0)

	table_list = xlrd_util.get_lines_from_xls(srcxlsfile ,table_list_tab_name
											  ,lambda lines :[line[0] for line in lines])
	print(table_list)

	def filter_uid(lines):
		return  [line[1] for line in lines if re.match(r'\w{3,4}_uid', line[1]) != None]

	map_uids = collections.OrderedDict ((lines[1][1] ,neoutil.Struct( **{'title' :key ,'attribute':{},'connected_uids' :filter_uid(lines[2:]) ,"subuids" :[]}))   for key, lines in map_lines.items() if key in table_list)
	print(",".join(map_uids))

	for uid ,comp in map_uids.items():
		title ,list_connect_uid = comp.title ,comp.connected_uids

		list_connectd_table = [map_uids[tmp_uid].title for tmp_uid in list_connect_uid if tmp_uid in map_uids]

		if len(list_connectd_table) == 0 :
			continue
		for tmp_uid in list_connect_uid:
			if tmp_uid not in map_uids:		continue
			map_uids[tmp_uid].subuids.append(uid)
	return map_uids


# print("{0} -> [{1}]".format(title,",".join(list_connectd_table)))

def make_diag_string(map_uids ,fmt_file):


	print()
	# classconv = neoutil.ConvStringForm(intype='und', outtype='und')
	str_diag = ""
	for uid, comp in map_uids.items():
		if len(comp.attribute) >0:
			attribinfo = ",".join(["{0}=\"{1}\"".format(key,value) for key, value in comp.attribute.items()])
			str_diag += "{0}  [{1}];\n".format(comp.title.lower(),attribinfo)

	for uid ,comp in map_uids.items():
		# "".lower()
		list_subtable = [  map_uids[tmp_uid].title.lower() for tmp_uid in comp.subuids]
		if len(list_subtable) == 0 :
			str_diag +="{0};\n".format(comp.title.lower())
			continue
		# for asfdsaf in list_subtable:
		str_diag += "{0} -> {1};\n".format(comp.title.lower(), ",".join(list_subtable))

	# print(str_diag)
	fmt = neoutil.StrFromFile(fmt_file)
	return fmt.format(str_diag)

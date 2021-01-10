import collections
import json
import os
import re

from jinja2 import Environment

from neolib import neoutil, file_util


def plain_text_to_list(plain_text):
	return re.split("\s+", plain_text.replace("\\", "/"))
def classify_from_src(src_list,map_gcc):
	list_src = src_list
	ret_map = collections.OrderedDict()
	def conv(tmp):
		dir,name = os.path.split(tmp)
		name,ext = os.path.splitext(name)
		return dir,name,ext.replace(".","")

	for tmp in list_src:
		dir, name, ext = conv(tmp)
		#print(tmp, dir, name, ext)
		dir_tag =dir.replace("/", "_")
		dir_tag = dir_tag.replace(".", "_")
		tag_name = dir_tag+"_"+ext
		if tag_name not in ret_map:
			ret_map[tag_name] =dict(tag=tag_name,ext=ext,dir=dir,list_name=[],gcc= map_gcc[ext.lower()])
		ret_map[tag_name]["list_name"].append(name)


		#neoutil.simple_view_list([conv(tmp) for tmp in list_src])
		# [os.path.split(tmp)]
		# print("a",os.path.split(tmp))
	return ret_map.values()

def json_file_list_to_MakeFile(fmt_file,json_file,make_file):
	conetnts = file_util.StrFromFile(fmt_file)
	map_comp_info = json.load(open(json_file))
	list_tag = classify_from_src(map_comp_info["src_list"],map_comp_info["map_gcc"])
	map_comp_info["list_src_info"]=list_tag
	# rendor_args = dict(title='neo_c_lib',list_src_info=list_tag,
	#                                                  incs="-Iinclude -I../include",defines="-D_USE_UTF8_ -DNEOUSEMBCS -DNEODEBUG -DNEO_STATIC -DLSA_EXPORTS_NOUSE",
	#                                                  flags="-Wall -O2 -fPIC -Wl,-Bsymbolic -std=gnu++11",ldflags="-shared -fPIC  -L../lib/gnu -ldl",
	#                                                  out_dir="../lib/gnu",	dist_dir="/usr/local",	def_command="static share")

	print(map_comp_info)
	outfile =Environment().from_string(conetnts).render(**map_comp_info)
	file_util.StrToFile(outfile,make_file)


if __name__ == '__main__':
	src_list = r"""
		src\debug_util.cpp
		src\internal.c
		src\user_bypass.cpp
		src\wolfio.c
		src\keys.c
		src\ssl.c
		src\tls.c
		wolfcrypt\src\aes.c
		wolfcrypt\src\arc4.c
		wolfcrypt\src\asn.c
		wolfcrypt\src\coding.c
		wolfcrypt\src\des3.c
		wolfcrypt\src\ecc_empty.c
		wolfcrypt\src\error.c
		wolfcrypt\src\hash.c
		wolfcrypt\src\hmac.c
		wolfcrypt\src\integer.c
		wolfcrypt\src\logging.c
		wolfcrypt\src\memory.c
		wolfcrypt\src\rabbit.c
		wolfcrypt\src\random.c
		wolfcrypt\src\ripemd.c
		wolfcrypt\src\sha256.c
		wolfcrypt\src\signature.c
		wolfcrypt\src\wc_encrypt.c
		wolfcrypt\src\wc_port.c
		wolfcrypt\src\wolfmath.c
		"""
	neoutil.simple_view_list(plain_text_to_list(src_list))
	json_file_list_to_MakeFile("rsc/Makefile.fmt", "rsc/code.json", "out/MakeFile.sample")
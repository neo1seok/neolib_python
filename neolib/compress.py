import zipfile

def unzip(source_file, dest_path,convert_filename = lambda fn:fn.encode('cp437').decode('euc-kr')):
	with zipfile.ZipFile(source_file, 'r') as zf:
		zipInfo = zf.infolist()

		for member in zipInfo:
#			print(member.extra)
			member.filename = convert_filename(member.filename)
			print(member.filename)
			zf.extract(member,dest_path)

import argparse
import os

def main(args:argparse.Namespace):
	print(args)


	pass

def touch(args:argparse.Namespace):
	fname = args.in_file


	#print(os.path.abspath(fname))

	#print(os.path.curdir)
	#print(os.getcwd())
	fname = os.path.abspath(fname)
	print('filename',fname)

	if os.path.exists(fname):
		os.utime(fname, None)
	else:
		open(fname, 'a').close()
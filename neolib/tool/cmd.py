import argparse
import os

def main(args:argparse.Namespace):
	print(args)


	pass

def touch(args:argparse.Namespace):
	fname = args.in_file

	print(fname)
	print(os.path.abspath(fname))

	print(os.path.curdir)
	print(os.getcwd())

	return
	if os.path.exists(fname):
		os.utime(fname, None)
	else:
		open(fname, 'a').close()
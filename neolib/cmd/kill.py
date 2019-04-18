import os, sys


def print_prc(cmd):
	print("########START#########")
	print(cmd)
	print("->")
	os.system(cmd)
	print("########END#########")


if __name__ == '__main__':
	map_args = dict(enumerate(sys.argv))
	print(dict(enumerate(sys.argv)), os.getpid())
	keword = map_args.get(1, "")
	cur_app = os.getpid()
	cmd = f"ps -ef | grep {keword} | grep -v grep | grep -v {cur_app}"
	# cmd = f"ps -ef | grep {keword} | grep -v grep "
	print_prc(cmd)

	killcmd = cmd + " | awk '{print $2}' | xargs kill -9"
	print("########START#########")
	key_val = input("kill this process? y or n?\n")
	print("########END#########")
	if key_val != "y":
		exit()
	print_prc(killcmd)
	print_prc(cmd)

import os,sys

if __name__ == '__main__':
	map_args = dict(enumerate(sys.argv))
	print(dict(enumerate(sys.argv)))
	keword = map_args.get(1,"")
	cur_app = map_args.get(0, "")
	cmd = f"ps -ef | grep {keword} | grep -v grep | grep -v {cur_app}"
	print(cmd)
	os.system(cmd)
	killcmd = cmd+" | awk '{print $2}' | xargs kill -9"
	key_val = input("kill this process? y or n?\n")
	if key_val !="y":
		exit()
	print(killcmd)
	os.system(killcmd)
	print(cmd)
	os.system(cmd)
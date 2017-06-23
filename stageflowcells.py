#Written by Nick Loman @pathogenomenick

import os
import os.path
import sys
import shutil
import re

input_dir = sys.argv[1]
albacore_dir = sys.argv[2]
process_dir = sys.argv[3]

basecalled_files = set()

for root, dirs, files in os.walk(albacore_dir, topdown=False):
	for name in files:
		basecalled_files.add(name)

# don't copy already staged files
for root, dirs, files in os.walk(process_dir, topdown=False):
	for name in files:
		basecalled_files.add(name)

for root, dirs, files in os.walk(input_dir, topdown=False):
	for name in files:
		if name not in basecalled_files:
			m = re.search('_(FN.*?)_', name)
			if not m:
				continue
			flowcell = m.group(1)

			albacore_root = root[len(input_dir):]
			# move it
			checkdir = process_dir + '/' + flowcell + '/' + albacore_root
			if not os.path.exists(checkdir):
				os.makedirs(checkdir)
			movefrom = input_dir + '/' + albacore_root + '/' + name
			moveto = process_dir + '/' + flowcell + '/' + albacore_root + '/' + name
			print "Copy %s to %s" % (movefrom, moveto)
			abspath = os.path.abspath(movefrom)
			print "Abspath %s" % (abspath,)	
			os.symlink(abspath, moveto)
			shutil.copy(movefrom, moveto)





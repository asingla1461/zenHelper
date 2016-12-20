"""
Usage
python main.py testFunctionName
python main.py -r testFunctionName : regenerate all tests incase you added a new one
"""

WORKING_DIR = "/Users/singla/Work/yourPeople3/"
STORAGE_DIR = "/Users/singla/LAB/testHelper/"
OUTPUT_FILE = 'store.txt'
prefix_len = len(WORKING_DIR)

import glob
import pyclbr
import sys
import shelve

all_tests = []

def regenerateAllTests():
	print 'regenerating all tests'

	test_files = []

	test_files = test_files + glob.glob(WORKING_DIR + "*/*test*.py")

	test_files = test_files + glob.glob(WORKING_DIR + "*/*/*test*.py")

	def getImportableName(test_file):
		ret = test_file[prefix_len:]
		ret = ret.replace('/', '.')
		ret = ret[:-3] # remove .py

		return ret

	test_files = [getImportableName(test_file) for test_file in test_files]

	ret = []

	for test_file in test_files:
		module_name = test_file
		try:
			module_info = pyclbr.readmodule(module_name)

			for item in module_info.values():
				methods = item.methods
				class_name = item.name
				for method, lineNo in methods.iteritems():

					if method.startswith("test") or method.startswith("Test"):
						full_test_path = "%s.%s.%s" % (test_file, class_name, method)
						ret.append(full_test_path)

		except Exception as e:
			print e
			pass

	print len(ret)
	return ret

def setUp(force):
	store = shelve.open(STORAGE_DIR + '/' + OUTPUT_FILE)

	if not store.has_key('all_tests') or force:
		store['all_tests'] = regenerateAllTests()
	
	global all_tests
	all_tests = store['all_tests']

	store.close()

def getTestName(test_name):
	for test in all_tests:
		if test_name == test.split('.')[-1]:
			return test

force = False
test_name = sys.argv[1]

if len(sys.argv) == 3:
	test_name = sys.argv[2]
	force = True

setUp(force)

full_test_name = getTestName(test_name)

from subprocess import call
import os 

full_command = "python manage.py test --reusedb --settings=yourpeople.test_local_settings %s" % full_test_name

call(full_command, shell=True)

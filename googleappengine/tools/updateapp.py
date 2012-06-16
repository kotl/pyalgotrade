# PyAlgoTrade
# 
# Copyright 2012 Gabriel Martin Becedillas Ruiz
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from optparse import OptionParser
import sys
import subprocess
import os
import shutil
import fileinput

def parse_cmdline():
	usage = "usage: %prog [options]"
	parser = OptionParser(usage=usage)
	parser.add_option("-i", "--app_id", dest="app_id", help="Google App Engine application identifier")
	parser.add_option("-a", "--app_path", dest="app_path", help="Directory where app.yaml resides")
	parser.add_option("-c", "--appcfg_path", dest="appcfg_path", help="Path where appcfg.py resides")
	mandatory_options = [
		"app_id",
		"app_path"
			]

	(options, args) = parser.parse_args()

	# Check that all mandatory options are available.
	for opt in mandatory_options:
		if getattr(options, opt) == None:
			raise Exception("--%s option is missing" % opt)

	return (options, args)

class AppCfg:
	def __init__(self, appPath, appCfgPath):
		self.__appPath = appPath
		self.__appCfgPath = appCfgPath

	def updateApp(self):
		cmd = []
		if self.__appCfgPath:
			cmd.append(os.path.join(self.__appCfgPath, "appcfg.py"))
		else:
			cmd.append("appcfg.py")
		cmd.append("update")
		cmd.append(self.__appPath)

		popenObj = subprocess.Popen(args=cmd)
		popenObj.communicate()

def update_app_yaml(appPath, appId):
	appYamlPath = os.path.join(appPath, "app.yaml")
	print "Updating app.yaml"
	for line in fileinput.input(appYamlPath, inplace=1):
		line = line.strip("\r\n")
		if line.find("application:") == 0:
			print "application: %s" % appId
		else:
			print line

def update_pyalgotrade(appPath):
	srcPath = os.path.join(appPath, "..", "..", "pyalgotrade")
	dstPath = os.path.join(appPath, "pyalgotrade")
	if os.path.exists(dstPath) == False:
		print "Preparing pyalgotrade package"
		shutil.copytree(srcPath, dstPath)

def main():
	try:
		(options, args) = parse_cmdline()
		update_app_yaml(options.app_path, options.app_id)
		update_pyalgotrade(options.app_path)
		appCfg = AppCfg(options.app_path, options.appcfg_path)
		print "Updating application using appcfg.py"
		appCfg.updateApp()
	except Exception, e:
		sys.stdout.write("Error: %s\n" % e)
		sys.exit(1)

if __name__ == "__main__":
	main()


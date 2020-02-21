import platform, os

def ReadFromFile(path):
	"""\
	Return content of file
	"""
	import os, codecs
	if os.path.exists(path):
		f = codecs.open(path, encoding='utf-8', mode='r')
		text = f.read()#.decode('utf8')
		f.close()
		return text

def WriteToFile(path, string):
	"""\
	Write content to file
	"""
	f = open(path, 'wb')
	f.write(string.encode())
	f.close()
	return True

def Execute(command):
	"""\
	Execute system command, return output.
	"""

	import sys, os, platform

	# if sys.version.startswith("2.3") or platform.system() == "Windows":

	# 	p = os.popen(command, "r")
	# 	response = p.read()
	# 	p.close()
	# 	return response


	# else:

	import subprocess

	process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, close_fds=True)
	os.waitpid(process.pid, 0)
	response = process.stdout.read().strip()
	process.stdout.close()
	process.wait()
	return response


def get_registry_value(key, subkey, value):
	import winreg
	key = getattr(winreg, key)
	handle = winreg.OpenKey(key, subkey)
	(value, type) = winreg.QueryValueEx(handle, value)
	return value


def MachineName():

	machineModelIdentifier = None
	humanReadableName = None
	specsDescription = None

	if platform.system() == 'Windows':

		specsDescription = get_registry_value(
			"HKEY_LOCAL_MACHINE", 
			"HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0",
			"ProcessorNameString")
		humanReadableName = get_registry_value(
			"HKEY_LOCAL_MACHINE", 
			"HARDWARE\\DESCRIPTION\\System\\BIOS",
			"SystemProductName")

	if platform.system() == 'Linux':
		
		cpu = ''
		itemsUsed = []
		procinfo = Execute('cat /proc/cpuinfo').decode()

		for line in procinfo.split('\n'):
			if ':' in line:
				k, v = line.split(':')[:2]
				if k.strip() == 'model name' and not k in itemsUsed:
					cpu += v.strip()
					itemsUsed.append(k)

		if os.path.exists('/sys/devices/virtual/dmi/id/sys_vendor') and os.path.exists('/sys/devices/virtual/dmi/id/product_name'):
			humanReadableName = '%s %s' % (Execute('cat /sys/devices/virtual/dmi/id/sys_vendor').decode(), Execute('cat /sys/devices/virtual/dmi/id/product_name').decode())
		else:
			humanReadableName = 'Google App Engine'
		specsDescription = cpu


	elif platform.system() == 'Darwin':

		name = None


		# Approach 1
		import sys
		import plistlib
		import subprocess
		from Cocoa import NSBundle
		data = plistlib.loads(Execute('system_profiler -xml SPHardwareDataType'))
		model = subprocess.check_output(["/usr/sbin/sysctl", "-n", "hw.model"]).strip()

		# Approach 2
		if not name:
			name = data[0]['_items'][0]['machine_name']

		machineModelIdentifier = data[0]['_items'][0]['machine_model']
		humanReadableName = '%s' % name
		# if not name.startswith('Apple'):
		# 	name = 'Apple ' + name
		specsDescription = []
		# if 'cpu_type' in data[0]['_items'][0]:
		# 	specsDescription.append(data[0]['_items'][0]['cpu_type'])
		if 'current_processor_speed' in data[0]['_items'][0]:
			specsDescription.append(data[0]['_items'][0]['current_processor_speed'])
		specsDescription.append('with')
		if 'physical_memory' in data[0]['_items'][0]:
			specsDescription.append(data[0]['_items'][0]['physical_memory'])

		specsDescription = ' '.join(specsDescription)

	return machineModelIdentifier, humanReadableName, specsDescription

def OSName():

	import platform

	if platform.system() == 'Darwin':
		return 'macOS %s' % platform.mac_ver()[0]

	elif platform.system() == 'Windows':

		return get_registry_value(
			"HKEY_LOCAL_MACHINE", 
			"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",
			"ProductName") + ', ' + str(platform.version())

	elif platform.system() == 'Linux':
		return ' '.join(platform.platform())


def addAttributeToURL(url, attributes):

	from urllib.parse import urlparse
	o = urlparse(url)

	for attribute in attributes.split('&'):

		key, value = attribute.split('=')


		replaced = False
		queryParts = o.query.split('&')
		if queryParts:
			for i, query in enumerate(queryParts):
				if '=' in query and query.startswith(key + '='):
					queryParts[i] = attribute
					replaced = True
					break
		if not replaced:
			if queryParts[0]:
				queryParts.append(attribute)
			else:
				queryParts[0] = attribute
		o = o._replace(query='&'.join(queryParts))

	return o.geturl()


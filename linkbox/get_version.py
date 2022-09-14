####################################################################################
# get_version_number from file (__version__.py, version.py, __init__.py or system) #
# author: cumulus13 <cumulus13@gmail.com>                             			   #
# license: GPL-v2                                                                  #
####################################################################################

from __future__ import print_function

import os
import sys
import inspect
import re

PY_VER = sys.version_info.major + float("0.%0.0f"%(sys.version_info.minor))
if os.getenv('DEBUG'): print("PY_VER:", PY_VER)
if sys.version_info.major == 2:
	import imp
elif PY_VER < 3.5 and PY_VER > 2.7:
	from importlib.machinery import SourceFileLoader 
elif PY_VER > 3.4:
	import importlib.util 
	
def get_from_file(path):
	version = ''
	try:
		with open(path, 'r') as f:
			d = re.findall('^(?i)version.*?=(.*?)$|__version__.*?=(.*?)$', f.read())
			if d: d = filter(None, d[0])
			if d: version = d[0].strip()
	except:
		pass
		
	return version

def get(module_name = None):
	version = ""
	if module_name:
		try:
			if PY_VER < 3.3:
				vers = imp.load_package('version', module_name)
				version = vers.version
		except:
			pass
	
	if not version:
		if os.path.isfile(os.path.join(os.getcwd(), '__version__.py')):
			if PY_VER < 3.3:
				vers = imp.load_source('version', os.path.join(os.getcwd(), '__version__.py'))
				try:
					version = vers.version
				except:
					pass
				if not version:
					version = get_from_file(os.path.join(os.getcwd(), '__version__.py'))
							
			elif PY_VER < 3.5 and PY_VER > 2.7:
				vers = SourceFileLoader("version", os.path.join(os.getcwd(), '__version__.py')).load_module()
				try:
					version = vers.version
				except:
					pass
				if not version:
					version = get_from_file(os.path.join(os.getcwd(), '__version__.py'))
			elif PY_VER > 3.4:
				spec = importlib.util.spec_from_file_location("version", os.path.join(os.getcwd(), '__version__.py'))
				vers = importlib.util.module_from_spec(spec)                           
				sys.modules["version"] = vers
				spec.loader.exec_module(vers)
				try:
					version = vers.version
				except:
					pass
				if not version:
					version = get_from_file(os.path.join(os.getcwd(), '__version__.py'))
				
		elif os.path.isfile(os.path.join(os.getcwd(), '__init__.py')):
			if PY_VER < 3.3:
				vers = imp.load_package('version', os.getcwd())
				try:
					version = vers.version
				except:
					pass
			elif PY_VER < 3.5 and PY_VER > 2.7:
				vers = SourceFileLoader("version", os.path.join(os.getcwd(), '__init__.py')).load_module()                                                        
				try:
					version = vers.version
				except:
					pass
				if not version:
					version = get_from_file(os.path.join(os.getcwd(), '__init__.py'))
			elif PY_VER > 3.4:
				spec = importlib.util.spec_from_file_location("version", os.path.join(os.getcwd(), '__init__.py'))
				vers = importlib.util.module_from_spec(spec)
				sys.modules["version"] = vers
				spec.loader.exec_module(vers)                                                                                                   
				try:
					version = vers.version
				except:
					pass
				if not version:
					version = get_from_file(os.path.join(os.getcwd(), '__init__.py'))
			
		elif os.path.isfile(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__version__.py')):
			if PY_VER < 3.3:
				vers = imp.load_source('version', os.path.join(os.path.dirname(os.path.realpath(__file__)), '__version__.py'))
				try:
					version = vers.version
				except:
					pass
			elif PY_VER < 3.5 and PY_VER > 2.7:
				vers = SourceFileLoader("version", os.path.join(os.path.dirname(os.path.realpath(__file__)), '__version__.py')).load_module()                                                        
				try:
					version = vers.version
				except:
					pass
				if not version:
					version = get_from_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__version__.py'))
			elif PY_VER > 3.4:
				spec = importlib.util.spec_from_file_location("version", os.path.join(os.path.dirname(os.path.realpath(__file__)), '__version__.py'))
				vers = importlib.util.module_from_spec(spec)
				sys.modules["version"] = vers
				spec.loader.exec_module(vers)                                                                                                   
				try:
					version = vers.version
				except:
					pass
				if not version:
					version = get_from_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__version__.py'))
			
		elif os.path.isfile(os.path.join(os.path.dirname(__file__), '__version__.py')):
			if PY_VER < 3.3:
				vers = imp.load_source('version', os.path.join(os.path.dirname(__file__), '__version__.py'))
				try:
					version = vers.version
				except:
					pass
				if not version:
					version = get_from_file(os.path.join(os.path.dirname(__file__), '__version__.py'))
			elif PY_VER < 3.5 and PY_VER > 2.7:
				vers = SourceFileLoader("version", os.path.join(os.path.dirname(__file__), '__version__.py')).load_module()
				try:
					version = vers.version
				except:
					pass
				if not version:
					version = get_from_file(os.path.join(os.path.dirname(__file__), '__version__.py'))
			elif PY_VER > 3.4:
				spec = importlib.util.spec_from_file_location("version", os.path.join(os.path.dirname(__file__), '__version__.py'))
				vers = importlib.util.module_from_spec(spec)
				sys.modules["version"] = vers
				spec.loader.exec_module(vers)                                                                                                   
				try:
					version = vers.version
				except:
					pass
				if not version:
					version = get_from_file(os.path.join(os.path.dirname(__file__), '__version__.py'))
		else:
			if PY_VER < 3.3:
				try:
					vers = imp.load_package('version', os.getcwd())
					version = vers.version
				except:
					pass
			
	if not version:
		try:
			version = inspect.getmodule(inspect.stack()[1][0]).VERSION
		except:
			pass
				
	if not version:
		
		try:
			version = inspect.getmodule(inspect.stack()[1][0]).__version__
		except:
			pass
	if not version:
		
		try:
			version = inspect.getmodule(inspect.stack()[1][0]).version
		except:
			pass
	return version
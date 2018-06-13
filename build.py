#from FlaskServer import app
from distutils.dir_util import copy_tree
#from jsmin import jsmin
import fnmatch
import compileall
import os, glob
import shutil, fnmatch
import json

__BASE_DIR__ = os.path.abspath(os.path.dirname(__file__))
DIST_FOLDER_BASE = __BASE_DIR__ + '/dist'
DIST_FOLDER_PROD = __BASE_DIR__ + '/dist/production'
DIST_FOLDER_DEBUG = __BASE_DIR__ + '/dist/debug'
SOURCE_FOLDER = __BASE_DIR__ + '/FlaskServer'


DIST_FOLDER_PROD_ULC = __BASE_DIR__ + '/dist/production/BL/Routes/ULC'
DIST_FOLDER_DEBUG_ULC = __BASE_DIR__ + '/dist/debug/BL/Routes/ULC'
ULC_ROUTE_PATH = __BASE_DIR__ + '/dist/debug/BL/Routes/ULC/prodroutes.py'
SN_ROUTE_PATH = __BASE_DIR__ + '/dist/debug/BL/Routes/SmartNode/prodroutes.py'

IGNORE_PATTERNS = ('*.log*', 'Dev')
IGNORE_PY_FILES = ('*.py')
CONFIG_FILE = 'setting.py'
PRODUCTIONS_ROUTES_FILE = 'prodroutes.py'

def remove_folders():
	if os.path.exists(DIST_FOLDER_BASE):
		shutil.rmtree(DIST_FOLDER_BASE, ignore_errors=True, onerror=None)


#def set_config_file_in_production():
#	config_file = os.path.join(DIST_FOLDER_DEBUG, CONFIG_FILE)
#	f = open(config_file,'r')
#	filedata = f.read()
#	f.close()
#	newdata = None
#	if 'app.config.from_object(TestingConfig)' in filedata:
#		newdata = filedata.replace("app.config.from_object(TestingConfig)","app.config.from_object(ProductionConfig)")

#	if 'app.config.from_object(TrainingConfig)' in filedata:
#		newdata = filedata.replace("app.config.from_object(TrainingConfig)","app.config.from_object(ProductionConfig)")

#	if newdata:
#		f = open(config_file,'w')
#		f.write(newdata)
#		f.close()

def set_config_file_in_production():

    config_file = os.path.join(DIST_FOLDER_DEBUG, CONFIG_FILE)

    f = open(config_file,'r')
    filedata = f.read()
    f.close()
    newdata = None
    if 'TestingConfig'in filedata:
	    newdata = filedata.replace('TestingConfig','ProductionConfig')

    if 'TrainingConfig' in filedata:
	    newdata = filedata.replace('TrainingConfig','ProductionConfig')

    if newdata:
	    f = open(config_file,'w')
	    f.write(newdata)
	    f.close()

def enable_jwt_required(filePath): 
    config_file = os.path.abspath(filePath)
    f = open(config_file,'r')
    filedata = f.read()
    f.close()
    newdata = None
    if '#@jwt_required()' in filedata:
	    newdata = filedata.replace("#@jwt_required()","@jwt_required()")


    if newdata:
	   f = open(config_file,'w')
	   f.write(newdata)
	   f.close()




#def minify_json_files():
#	minified_files = []
#	for root, dirnames, filenames in os.walk(DIST_FOLDER_DEBUG):
#		for filename in fnmatch.filter(filenames, '*.json'):
#			with open(os.path.join(root, filename)) as js_file:
#				minified_files.append(os.path.join(root, filename))
#				minified = jsmin(js_file.read())
#				with open(os.path.join(root, filename), 'w') as file:
#					json.dump(minified, file)

remove_folders()

# Copy to dist file
shutil.copytree(SOURCE_FOLDER, DIST_FOLDER_DEBUG, ignore=shutil.ignore_patterns(*IGNORE_PATTERNS))

# Remove temp folder
if os.path.exists(os.path.join(DIST_FOLDER_DEBUG, 'temp')):
	shutil.rmtree(os.path.join(DIST_FOLDER_DEBUG, 'temp'))

# Set in production
set_config_file_in_production()

# Set jwt required to production routes FOR ULC ROUTES
enable_jwt_required(ULC_ROUTE_PATH)

# Set jwt required to production routes FOR SmartNode ROUTES
enable_jwt_required(SN_ROUTE_PATH)

# Compile all
compileall.compile_dir(DIST_FOLDER_DEBUG, force=True)

# Copy to py files to debug folder
shutil.copytree(DIST_FOLDER_DEBUG, DIST_FOLDER_PROD, ignore=shutil.ignore_patterns(IGNORE_PY_FILES))

# Delete pyc files from debug folder
for root, dirnames, filenames in os.walk(DIST_FOLDER_DEBUG):
	for filename in fnmatch.filter(filenames, '*.pyc'):
		os.remove(os.path.join(root, filename))

#minify_json_files()

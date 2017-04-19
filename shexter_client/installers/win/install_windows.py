import os
import shutil
import sys
import winreg

APP_NAME = 'shexter'
# client .py and dependencies are kept 2 directories above this script, so use path[0]
CLIENT_DIR = sys.path[0] + '\..\..\\'
# LIB_DIR = FILES_DIR + 'lib\\'
# Add appdirs to the PATH so that we can use that code
# sys.path.append(LIB_DIR)
# from appdirs import user_config_dir

env_var = 'LOCALAPPDATA'
# This code is duped from shexter.py
install_dir = os.getenv(env_var)
if not install_dir:
    # won't happen. I think.
    print('Unable to get config directory. Please set the environment variable ' + env_var
          + ' to something like C:\\Users\\$Username\\AppData\\Local')
    quit()

install_dir = os.path.join(install_dir, APP_NAME)
print("Installing into " + install_dir)

BAT_NAME = APP_NAME + '.bat'
CLIENT_NAME = APP_NAME + '.py'
# PERSIST_NAME = APP_NAME() + '_persistant.py'
# DEPENDENCIES = [ 'appdirs.py' ]		# Add new dependencies to the list and the lib directory

# add lib_dir to each dependency so installer can find
# DEPENDENCIES = [ LIB_DIR + s for s in DEPENDENCIES ]

print('WARNING: This script does edit your registry, so run only if you trust me ' +
      'or understand what this script does!')

print('Confirm install shexter into ' + install_dir + '? y/N: ')
response = input().lower()

if response != 'y':
    print('Sorry to hear that!')
    quit()

# make the dir if necessary
if not os.path.exists(install_dir):
    try:
        os.makedirs(install_dir)
    except PermissionError:
        print('Creating ' + install_dir + ' failed to due permissions error. '
              'Close any applications that are using this folder.')
        quit()

# Delete old files, but not the config file
for file in os.listdir(install_dir):
    if not file.endswith(".ini"):
        try:
            fullpath = os.path.join(install_dir, file)

            if os.path.isdir(fullpath):
                shutil.rmtree(fullpath)
            else:
                os.remove(fullpath)
        except PermissionError as e:
            print(e)
            print('Make sure no other processes are using it.')
            print('If this persists, delete the folder manually.')
            quit()

# copy the files
shutil.copy(CLIENT_DIR + CLIENT_NAME, install_dir)
# shutil.copy(FILES_DIR + PERSIST_NAME, install_dir)
# use path[0] because .bat is in the same folder as this script
shutil.copy(os.path.join(sys.path[0], BAT_NAME), install_dir)
# copy the 'shexter' python module (folder)
shutil.copytree(os.path.join(CLIENT_DIR, APP_NAME), os.path.join(install_dir, APP_NAME))
# for dep in DEPENDENCIES:
# 	shutil.copy(dep, install_dir)

# Assert the files were copied

client_fullpath = install_dir + '\\' + CLIENT_NAME
bat_fullpath = install_dir + '\\' + BAT_NAME
# persist_fullpath = install_dir + '\\' + PERSIST_NAME

if os.path.isfile(client_fullpath):
    print('Copying client script successful.')
else:
    print(client_fullpath + ' was not found. Something went wrong :(')
    quit()

'''
if os.path.isfile(persist_fullpath):
    print('Copying persistant script successful.')
else:
    print(persist_fullpath + ' was not found. Something went wrong :(')
    quit()
'''

if os.path.isfile(bat_fullpath):
    print('Copying .bat successful.')
else:
    print(bat_fullpath + ' was not found. Something went wrong :(')
    quit()

# Edit PATH so you can easily shext from any directory!

print('Adding Shexter to User PATH.')

try:
    pathkey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_ALL_ACCESS)
    SUBKEY = 'PATH'
    currpath = winreg.QueryValueEx(pathkey, SUBKEY)[0]
    if install_dir not in currpath:
        winreg.SetValueEx(pathkey, SUBKEY, 0, winreg.REG_SZ, currpath + ';' + install_dir)

    winreg.CloseKey(pathkey)
    print('Successfully added ' + APP_NAME + ' to PATH.')
except FileNotFoundError:
    # create the key (will this ever happen?)
    print('user PATH not found, should create it.')

print('Install successful. You should now be able to run shexter from anywhere ' +
      'after restarting your terminal.')

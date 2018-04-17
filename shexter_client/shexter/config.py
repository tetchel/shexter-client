import os
import sys
from configparser import ConfigParser
from shutil import get_terminal_size
import socket

from shexter.platform import get_platform, Platform
from shexter.sock import find_phones, port_str_to_int


''' This file deals with reading and writing settings. Call configure() to get the ip address.'''

APP_NAME = 'shexter'
SETTINGS_FILE_NAME = APP_NAME + '.ini'

"""
Settings file explanation:
The setting file contains one entry per client IP, mapping that client IP to a (phoneIP, port) pairing.
The intention is that if the user moves their computer (and therefore the client) to a new LAN, 
the client IP will change, so shexter will recognize the phone must be re-acquired. Then, when the user goes back to
the first LAN, their client and phone IPs will return to the previous values, which will still be stored in the config.
"""
SETTING_PHONE_IP = 'Phone_IP'
SETTING_PHONE_PORT = 'Port'

# These two variables are not to be modified by other classes
# full path to the config file
glob_config_file_path = None


def _get_ip():
    """
    :return: This computer's default AF_INET IP address as a string
    """

    # find ip using answer with 75 votes
    # https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    ip = ''
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # apparently any IP will work
        sock.connect(('192.168.1.1', 1))
        ip = sock.getsockname()[0]
    except Exception:
        print('Error: Couldn\'t get IP!')
    finally:
        sock.close()

    return str(ip)


def _write_config_file(config_filepath, connectioninfo):
    """
    Write the settings to the file.
    :param config_filepath: Path to the file.
    :param connectioninfo: (IP, Port) to write.
    :return: Nothing.
    """

    # configfile = open(user_config_dir(APP_NAME), 'w')
    config = ConfigParser()
    if os.path.isfile(config_filepath):
        try:
            config.read_file(open(config_filepath, 'r'))
            # print('loaded existing config ' + str(config))
        except Exception as e:
            print('Couldn\'t read existing config file: ' + str(e))
            delete_config_file()

    current_pc_ip = _get_ip()
    if not config.has_section(current_pc_ip):
        # print('New client IP')
        config.add_section(current_pc_ip)
    # else:
        # print('Overwriting existing client IP')

    config.set(current_pc_ip, SETTING_PHONE_IP, str(connectioninfo[0]))
    config.set(current_pc_ip, SETTING_PHONE_PORT, str(connectioninfo[1]))
    print('Recorded new Phone location {} for client IP {}'.format(connectioninfo, current_pc_ip))

    config.write(open(config_filepath, 'w'))


def _get_config_file_path():
    """
    Assembles and returns the absolute path to the settings file.
    Should only need to be run ONE TIME.
    :return: Full path to settings file
    """

    # Obtain the platform if it hasn't been done already.
    platf = get_platform()

    if platf == Platform.WIN:
        config_path = os.environ['LOCALAPPDATA']
    else:
        if not (platf == Platform.LINUX or platf == Platform.CYGWIN):
            print('Your platform is not supported, but you can still use '
                  'Shexter by setting the HOME environment variable.')

        config_path = os.path.join(os.environ['HOME'], '.config')

    if not config_path:
        sys.exit('Could not get environment variable for config creation.')

    config_path = os.path.join(config_path, APP_NAME)
    if not os.path.exists(config_path):
        try:
            os.makedirs(config_path)
            print('Creating a new folder at ' + config_path)
        except PermissionError:
            # either user has directory open, or doesn't have w/x permission (on own config dir?)
            sys.exit('Could not access ' + config_path + ', please check the directory\'s permissions, '
                                                         'and close any program using it.')

    return os.path.join(config_path, SETTINGS_FILE_NAME)


def get_tty_width():
    """

    :return: Terminal width as a string
    """
    return str(get_terminal_size()[0])


def get_glob_config_filepath():
    # glob should only be set once
    global glob_config_file_path
    config_file_path = glob_config_file_path
    # initialize it if necessary
    if not config_file_path:
        config_file_path = _get_config_file_path()
        glob_config_file_path = config_file_path

    return glob_config_file_path


def delete_config_file():
    config_file_path = get_glob_config_filepath()

    if os.path.isfile(config_file_path):
        os.remove(config_file_path)
        print('Removed config file at ' + config_file_path)


def configure(force_new_config):
    """
    First, tries to ping the phone using the existing settings file. If the phone is not found,
    tries to find it using find_phones(). If it is still not found,
    user can enter info manually, or quit.
    :param force_new_config: If True, will skip over reading the config file and will jump straight to
    acquiring the phone.
    :return: (IP, Port) that was recorded (either autoconnected or manual).
    """

    config_file_path = get_glob_config_filepath()

    config = ConfigParser()
    config.read(config_file_path)

    client_ip = _get_ip()
    try:
        config[client_ip]
    except KeyError:
        print('No saved phone IP for current client IP ' + client_ip)
        force_new_config = True

    connectinfo = ()
    if not force_new_config:
        try:
            #print('Looking up stored connectinfo for client_ip ' + client_ip)
            ip_addr = config[client_ip][SETTING_PHONE_IP]
            port = config[client_ip][SETTING_PHONE_PORT]

            # print('Current phone info for client_ip {}: ({}, {})'.format(client_ip, ip_addr, port))

            port = port_str_to_int(port)
            if not port:
                # An invalid port was in the config file
                raise KeyError

            connectinfo = (ip_addr, port)
        except KeyError:
            print('Error parsing config for current client IP')
            print('If you keep having issues with your configuration file, please try deleting ' +
                  get_glob_config_filepath())

            config.remove_section(client_ip)

    if not connectinfo or force_new_config:
        print('Forcing reconfigure')
        try:
            connectinfo = find_phones()
        except (KeyboardInterrupt, EOFError):
            print('\nPhone finder cancelled')

        if not connectinfo:
            manual = input('Couldn\'t find your phone - configure manually? Y/n: ')
            if manual is not 'n' and manual is not 'N':

                ip_addr = ''
                port = -1

                passed = False
                first = True
                while first or not passed:
                    first = False
                    ip_addr = input('Enter the IP Address in the app, eg. "192.168.1.100" : ')
                    try:
                        socket.inet_aton(ip_addr)
                        passed = True
                    except (KeyboardInterrupt, EOFError):
                        print(APP_NAME + ' cannot run without a valid IP.')
                        quit()
                    except OSError:
                        print('"' + ip_addr + '" is not a valid IP. ')

                passed = False
                first = True
                while first or not passed:
                    first = False
                    port_str = input('Enter the Port in the app, which should be "23457": ')
                    try:
                        port = port_str_to_int(port_str)
                        passed = port is not None
                    except (KeyboardInterrupt, EOFError):
                        print(APP_NAME + ' cannot run without a valid port number.')
                        quit()

                connectinfo = (ip_addr, port)

        if connectinfo: 
            _write_config_file(config_file_path, connectinfo)
        else:
            quit()

    return connectinfo

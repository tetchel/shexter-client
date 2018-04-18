#!/usr/bin/env python3

from threading import Thread
from time import sleep
import logging

import shexter.requester
import shexter.platform as platform
import shexter.config


"""
This file is for the shexter daemon, which runs persistantly. Every 5 seconds, it polls the phone to see if there are
unread messages. If there are, it displays a notification to the user.
This file is meant to be run directly; not to be imported by any other file.
"""


def notify(msg: str, title=shexter.config.APP_NAME):
    # Note swap of msg, title order
    print(title + ': ' + msg)
    notify_function(title, msg)


def _parse_contact_name(line: str):
    # print('parsing contact name from "{}"'.format(line))
    # The contact name is the first word after the first ']'
    return line.split(']')[1].strip().split()[0].rstrip(':')


def notify_unread(unread: str) -> None:

    unread_lines = unread.splitlines()
    # Remove the first line, which is just "Unread Lines"
    unread_lines = unread_lines[1:]
    if len(unread_lines) > 1:
        notify_title = str(len(unread_lines)) + ' New Messages'
        notify_msg = 'Messages from '
        contact_names = []
        for line in unread_lines:
            contact_name = _parse_contact_name(line)
            # Don't repeat contacts
            if contact_name not in contact_names:
                notify_msg += contact_name + ', '

            contact_names.append(contact_name)

        # Remove last ', '
        notify_msg = notify_msg[:-2]
    else:
        contact_name = _parse_contact_name(unread_lines[0]  )
        notify_title = 'New Message'
        notify_msg = 'Message from ' + contact_name

    # A cool title would be the phone's hostname.
    notify(notify_msg, title=notify_title)


def init_notifier_win():
    try:
        import win10toast
        toaster = win10toast.ToastNotifier()
        toaster.show_toast(shexter.config.APP_NAME, 'Notifications enabled', duration=5, threaded=True)
        return toaster
    except ImportError as e:
        print(e)
        print('***** To use the ' + shexter.config.APP_NAME + ' daemon on Windows you must install win10toast'
                                                        ' with "[pip | pip3] install win10toast"')
        quit()


def notify_win(title: str, msg: str) -> None:
    # Notifier is a win10toast.ToastNotifier
    notifier.show_toast(title, msg, duration=5, threaded=True)


"""
def build_notifier_macos():
    # Fuck this for now

    try:
        import gntp.notifier
    except ImportError:
        print('To use the ' + shexter.config.APP_NAME + ' daemon on OSX you must install Growl (see http://growl.info) 
                                                        and its python library with "pip3 install gntp"')
        quit()
"""


def init_notifier_nix():
    return 'poop'


def notify_nix(title: str, msg: str):
    print('linux notify func')
    pass


def init_notifier():
    """
    Initializes the 'notifier' and 'notify_function' globals, which are later called by notify
    The notifier is an object for the notify_platform functions to use
    """
    platf = platform.get_platform()
    global notifier, notify_function
    if platf == platform.Platform.WIN:
        notifier = init_notifier_win()
        notify_function = notify_win
    elif platf == platform.Platform.LINUX:
        notifier = init_notifier_nix()
        notify_function = notify_nix
    else:
        print('Sorry, notifications are not supported on your platform, which appears to be ' + platf)
        return None


# Must match response from phone in the case of no msgs.
NO_UNREAD_RESPONSE = 'No unread messages.'


def main(connectinfo: tuple):
    running = True

    logging.basicConfig(filename=shexter.config.APP_NAME.lower() + 'd.log', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(shexter.config.APP_NAME)

    launched_msg = shexter.config.APP_NAME + ' daemon launched'
    logger.info(launched_msg)
    logger.info('ConnectInfo: ' + str(connectinfo))
    print(launched_msg + ' - CTRL + C to quit')

    try:
        while running:
            unread_result = shexter.requester.unread_command(connectinfo, silent=True)
            # print('result: ' + str(type(unread_result)) + ' ' + unread_result)
            if not unread_result:
                logger.info('Failed to connect to phone')
            elif unread_result != NO_UNREAD_RESPONSE:
                # new messages
                Thread(target=notify_unread, args=(unread_result,)).start()
                logger.info('Got at least 1 msg')
            else:
                logger.debug('No unread')
                # print('no unread')

            sleep(5)
    except (KeyboardInterrupt, EOFError):
        print('Exiting')
        quit(0)


_connectinfo = shexter.config.configure(False)
if not _connectinfo:
    print('Please run ' + shexter.config.APP_NAME + ' config first, so the daemon knows how to find your phone.')
    quit()

# Initialize globals
notifier = None
notify_function = None
init_notifier()
if not notifier:
    notify_function = print

# Call the main loop
main(_connectinfo)

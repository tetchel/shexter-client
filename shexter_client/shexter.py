#!/usr/bin/env python3

import argparse
import sys

import shexter.config
from shexter.requester import DEFAULT_READ_COUNT, request


def _get_argparser():
    """
    :return: Shexter's ArgumentParser
    """

    # description='Send and read texts using your ' + 'Android phone from the command line.'

    parser = argparse.ArgumentParser(prog='', usage='command [contact_name] [options]\n'
                                                    'You can also run "' + shexter.config.APP_NAME.lower() +
                                                    ' help" to see commands and their options.')
    parser.add_argument('command', type=str,
                        help='Possible commands: Send $ContactName, Read $ContactName, Unread, Contacts, Ring, ' +
                             'SetPref $ContactName, Config. Not case sensitive.')
    parser.add_argument('contact_name', type=str, nargs='*',
                        help='Specify contact for SEND and READ commands.')
    parser.add_argument('-c', '--count', default=DEFAULT_READ_COUNT, type=int,
                        help='Specify how many messages to retrieve with the READ command. ' +
                             str(DEFAULT_READ_COUNT) + ' by default.')
    parser.add_argument('-m', '--multi', default=False, action='store_const', const=True,
                        help='Keep entering new messages to SEND until cancel signal is given. ' +
                             'Useful for sending multiple texts in succession.')
    parser.add_argument('-s', '--send', default=None, type=str,
                        help='Allows sending messages as a one-liner. Put your message in quotes after the flag. ')
    parser.add_argument('-n', '--number', default=None, type=str,
                        help='Specify a phone number instead of a contact name for send, read, and unread commands.')

    return parser


COMMAND_CONFIG = 'config'
COMMAND_CONFIG_2 = 'configure'
COMMAND_HELP = 'help'
COMMAND_HELP_2 = 'h'


def main(args_list):
    parser = _get_argparser()
    args = parser.parse_args(args_list)

    command = args.command.lower()
    if command == COMMAND_HELP or command == COMMAND_HELP_2:
        parser.print_help()
        quit()

    if command == COMMAND_CONFIG or command == COMMAND_CONFIG_2:
        shexter.config.configure(True)
        print('Config complete to ' + shexter.config.get_glob_config_filepath())
        quit()

    first = True
    result = None
    while first and not result:
        # Force a new config after the first try, or if 'shexter config' was run
        connectinfo = shexter.config.configure(not first)

        result = request(connectinfo, args)
        first = False

    if result:
        print(result)

    return result


# for calling shexter directly
if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except (KeyboardInterrupt, EOFError):
        print('\nTerminating.')
        quit()

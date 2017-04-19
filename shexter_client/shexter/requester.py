#!/usr/bin/env python3

from shexter.sock import contact_server
from shexter.config import get_tty_width

''' Build requests, and send them to the server. '''

# Command constants, must match those in the server code.
COMMAND_SEND = "send"
COMMAND_READ = "read"
COMMAND_GETCONTACTS = "contacts"
COMMAND_UNRE = "unread"
# If the user is sending to/reading from a number rather than a contact name
NUMBER_FLAG = "-number"

SETPREF_NEEDED = "NEED-SETPREF"
COMMAND_SETPREF = "setpref"
COMMAND_SETPREF_LIST = COMMAND_SETPREF + "-list"

DEFAULT_READ_COUNT = 20
READ_COUNT_LIMIT = 5000


def _get_contact_name(args, required):
    """
    Force user to input contact name if one wasn't given in the args.
    Used for SEND, READ, and SETPREF commands.
    :param args: Command-line args to be checked for the contact name
    :param required: If the contact name must be specified, or it's optional
    :return: The contact name, or None
    """
    contact_name = ''
    # build the contact name (can span multiple words)
    for name in args.contact_name:
        contact_name += name + ' '

    contact_name = contact_name.strip()

    while not contact_name and required:
        print('You must specify a Contact Name for Send and Read and SetPref commands. ' +
              'Enter one now:')
        try:
            contact_name = input('Enter a new contact name (CTRL + C to give up): ').strip()
        except (EOFError, KeyboardInterrupt):
            # gave up
            print()
            return None

    return contact_name


def _get_message():
    """
    Used for SEND command. Get user to input the message to send.
    :return: The message, or None if the input was cancelled
    """
    print('Enter message (Press Enter twice to send, CTRL + C to cancel): ')
    try:
        msg_input = ""
        # TODO allow backspacing of newlines.
        first = True
        while True:
            line = input()
            if not line.strip() and not first:
                break
            first = False
            msg_input += "%s\n" % line

        return msg_input
    # exception occurs when sigint is sent, aka user cancelled
    except (EOFError, KeyboardInterrupt):
        return None


def _send_command(connectinfo, to_send, arg_send, arg_multi):
    """
    Do the send command - Get the message to send, send it, print the phone's response.
    Repeat if necessary (-m flag).
    :param connectinfo: Phone's connection info
    :param to_send: The request to send (lacking the actual message)
    :param arg_send: The message to send if it was specified using -s
    :param arg_multi: If multiple messages are to be sent in one command
    :return: The message to be output to the user.
    """

    msg = ''
    if arg_send is not None:
        msg = arg_send + '\n'

    output = ''
    first_send = True
    # send at least one message, but keep looping if -m was given
    while first_send or arg_multi:
        first_send = False
        # get msg if it wasn't given already
        if msg == '':
            msg = _get_message()
        # see if user input message
        if msg is None:
            output = 'Send cancelled.'
            break
        elif len(msg.strip()) == 0:
            output = 'Not sent: message body was empty.'
        elif len(msg.split('\n', 1)[0]) == 0:
            output = 'Not sent: first line cannot be blank (for now).'
        else:
            # add the message to to_send
            to_send_full = to_send + msg + '\n'
            output = contact_server(connectinfo, to_send_full)
            if arg_multi:
                print(output)
            msg = ''

    return output


def _handle_setpref_response(connectinfo, response):
    """
    If the specified contact has multiple numbers, handle the response by picking a number.
    :param connectinfo: Phone's connection info
    :param response: The server's response containing the possible phone numbers
    :return: The server's response, which is either the setpref confirmation or the original command's response.
    """

    response = response[len(SETPREF_NEEDED) + 1:]
    number_of_numbers = len(response.split('\n')) - 1
    if 'Current:' in response:
        number_of_numbers -= 1

    print(response)

    preferred = input('Select a number from the above, 1 to ' + str(number_of_numbers) + ': ')

    # Check that user input a valid digit, and that it is within the acceptable range.
    while not (preferred.isdigit() or (int(preferred) > number_of_numbers or int(preferred) < 1)):
        print('Not a valid selection: must be integer between 1 and ' + str(number_of_numbers))
        preferred = input('Select a number: ')

    preferred = int(preferred) - 1

    contact_name = response.split(' has', 1)[0]
    to_send = COMMAND_SETPREF + '\n' + contact_name + '\n' + str(preferred) + '\n\n'

    # Send the new pref to the phone. The phone will then perform the original request if needed.
    return contact_server(connectinfo, to_send)


def unread_command(connectinfo):
    to_send = COMMAND_UNRE + '\n' + get_tty_width() + '\n\n'
    response = contact_server(connectinfo, to_send)
    # Must match the phone's 'no unread' response
    # if response != 'No unread messages.':
    return response
    # else:
    #    return ''



def request(connectinfo, args):
    """
    From list of command-line args, build the beginning of the request to send.
    Get any missing info from the user (contact name) then, invoke the command and contact the server.
    :param connectinfo: Server's connection info
    :param args: Command-line arguments
    :return: The response from the server.
    """

    command = args.command.lower()

    # Print messages if user passes useless flags.
    if command != COMMAND_READ and args.count != DEFAULT_READ_COUNT:
        print('Ignoring -c flag: only valid for READ command.')

    if command != COMMAND_SEND:
        if args.multi:
            print('Ignoring -m flag: only valid for SEND command.')
        if args.send is not None:
            print('Ignoring -s flag: only valid for SEND command.')

    # If the user is doing a regular setpref (not one from read/send), they must start with a list
    # to determine which numbers can be chosen from.
    if command == COMMAND_SETPREF:
        command = COMMAND_SETPREF_LIST

    # Get the contact name if required, from the args or from the user if not provided.
    if args.number is None and (command == COMMAND_SEND or command == COMMAND_READ or command == COMMAND_SETPREF_LIST):
        contact_name = _get_contact_name(args, True)
        if contact_name is None:
            return None
    else:
        contact_name = _get_contact_name(args, False)

    # Build server request
    to_send = command + '\n'
    # Contact name/number
    if args.number is not None:
        to_send += NUMBER_FLAG + '\n' + args.number + '\n'
    else:
        to_send += contact_name + '\n'

    # For read commands, include the number of messages requested
    if command == COMMAND_READ:
        if args.count > READ_COUNT_LIMIT and command:
            print('Retrieving the maximum number of messages: ' + str(READ_COUNT_LIMIT))
            args.count = READ_COUNT_LIMIT

        to_send += str(args.count) + '\n'

    # These commands provide output width.
    if command == COMMAND_UNRE or command == COMMAND_SETPREF_LIST or command == COMMAND_READ:
        to_send += get_tty_width() + '\n\n'

    # Request is assembled (except for send)
    # Contact the server
    response = ''
    if command == COMMAND_SEND:
        response = _send_command(connectinfo, to_send, args.send, args.multi)
    elif command == COMMAND_READ or command == COMMAND_SETPREF_LIST or command == COMMAND_GETCONTACTS:
        response = contact_server(connectinfo, to_send)
    elif command == COMMAND_UNRE:
        response = unread_command(connectinfo)
    else:
        print('Command \"{}\" not recognized.'.format(command))

    if response and response.startswith(SETPREF_NEEDED):
        response = _handle_setpref_response(connectinfo, response)

    return response

import errno
import socket
from select import select
from sys import stdout


''' This file performs network operations. '''


PORT_MIN = 23456
PORT_MAX = 23460
DISCOVER_REQUEST = 'shexter-discover'
DISCOVER_CONFIRM = 'shexter-confirm'
ENCODING = 'utf-8'


def port_str_to_int(port):
    """
    Accepts a string port, validates it is a valid port, and returns it as an int.
    :param port: A string representing a port
    :return: The port as an int, or None if it was not valid.
    """
    try:
        port = int(port)
        if port is None or port < 1024 or port > 49151:
            raise ValueError
        return port
    except ValueError:
        print('"' + str(port) + '" is not a valid port. Must be an integer between 1025 and 49150.')
        return None


def _get_broadcast_addrs():
    """
    :return: List of broadcast addresses the host can use. We will broadcast to each of these.
    """

    try:
        # This library is only used by this one function, which the user can choose to not use.
        import netifaces
    except ImportError:
        print('***** You must install netifaces to use the phone finder: "pip3 install netifaces"')
        return []

    broadcast_addresses = []

    for iface in netifaces.interfaces():
        #print('iface ' + iface)
        addrs = netifaces.ifaddresses(iface)

        inet_ifaces = []
        try:
            inet_ifaces = addrs[netifaces.AF_INET]
        except KeyError:
            pass
        for i in inet_ifaces:
            bcast = None
            try:
                bcast = i['broadcast']
            except KeyError:
                pass

            if bcast is not None and bcast != '127.255.255.255':    # Sometimes it picks up lo
                #print('broadcast address: ' + bcast)
                broadcast_addresses.append(bcast)

    print('Broadcast addresses: ' + str(broadcast_addresses))
    return broadcast_addresses


def find_phones():
    """
    This function broadcasts on the LAN to the Shexter ports, and looks for a reply from a phone.
    :return: (IP, Port) tuple representing the phone the user selects. None if no phone found.
    """
    sock_sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # IP, Port tuple representing the phone
    phone = None
    rejected_hosts = []

    broadcast_addrs = _get_broadcast_addrs()
    if not broadcast_addrs:
        print('There was a problem running the phone finder. You will have to configure manually.')
        return None

    print('Ready to search for phones.')
    input('Press Enter when the app is open on your phone.\n')

    for port in range(PORT_MIN, PORT_MAX+1):
        count = 0

        # Search more on the earlier ports which are much more likely to be the right one
        #if port == PORT_MIN:
        #    tries = 4
        #else:
        #    tries = 2
        tries = 2

        print('Searching on port ' + str(port), end="")
        while not phone and count < tries:
            count += 1
            print('.', end='')
            stdout.flush()

            # Send on ALL the interfaces (required by Windows!)
            for broadcast_addr in broadcast_addrs:
                #print('\nbroadcasting on ' + broadcast_addr + ' to ' + str(port))
                discover_bytes = bytes(DISCOVER_REQUEST, ENCODING)
                sock_sender.sendto(discover_bytes, (broadcast_addr, port))

                sock_recvr = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock_recvr.bind(('', port))

                # Wait for phone to respond
                # I don't know what an appropriate timeout for this would be - shorter is better but how short
                # is too short?
                ready = select([sock_recvr], [], [sock_sender, sock_recvr], 0.25)
                if ready[0]:
                    # Buffsize must match ConnectionInitThread.BUFFSIZE
                    data, other_host = sock_recvr.recvfrom(256)
                    data = data.decode(ENCODING).rstrip(' \0')
                    if not data.startswith(DISCOVER_CONFIRM):
                        print('Received a strange response: ' + data)
                        continue

                    # Skip over rejected hosts
                    if not other_host[0] in rejected_hosts:
                        print()
                        print('Got a response from ' + str(other_host))
                        # The first line of the response is a confirm, the second is phone info, the third is port#
                        # Print out the phone info received, and get the user to confirm
                        print('Phone info: ' + data.splitlines()[1])
                        confirm = input('Is this your phone? y/N: ')
                        if confirm.lower() == 'y':
                            # Get the port the TCP Socket is listening for from the third line of the request
                            tcp_port_str = data.splitlines()[2]
                            # Convert to an int
                            tcp_port = port_str_to_int(tcp_port_str)
                            if not tcp_port:
                                # Cannot recover from this; it's a server bug. Manual config only workaround.
                                print('Received invalid port from phone; cannot continue.'.format(tcp_port_str))
                                return None

                            return other_host[0], tcp_port
                        else:
                            rejected_hosts.append(other_host[0])

                if ready[2]:
                    print('There was an error selecting ' + ready[2])

                sock_recvr.close()

        print()

    return None


def _connect_tcp(connectinfo):
    """
    Connect to the phone using the given IP, port pairing
    :return: The created TCP socket.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.settimeout(120)
    sock.settimeout(10)
    try:
        sock.connect(connectinfo)
    except OSError as e:
        restart_msg = ('\n\nTry restarting the Shexter app, then run "shexter config" to change the IP address '
                       'to the one displayed on the app.\n'
                       'Also ensure your phone and computer are connected to the same network.')
        errorcode = e.errno
        if errorcode == errno.ECONNREFUSED:
            print('Connection refused: Likely Shexter is not running on your phone.'
                  + restart_msg)
            return None
        elif errorcode == errno.ETIMEDOUT or 'time' in str(e):
            print('Connection timeout: Likely your phone is not on the same network as your '
                  'computer or the connection info ' + str(connectinfo) + ' is not correct.' + restart_msg)
            return None
        else:
            print('Unexpected error occurred: ')
            print(str(e))
            print(restart_msg)
            return None
    except (EOFError, KeyboardInterrupt):
        print('Connect cancelled')
        return None

    return sock


HEADER_LEN = 32
BUFFSIZE = 4096


def _receive_all(sock):
    """
    Read all bytes from the given TCP socket.
    :param sock:
    :return: The decoded string, using ENCODING
    """
    data = b''
    # receive the header to determine how long the message will be
    header = 0
    try:
        header = sock.recvfrom(HEADER_LEN)
        header = header[0].decode(ENCODING, 'strict')
        if not header:
            raise ConnectionResetError
    except ConnectionResetError:
        print('Connection forcibly reset; this means the server crashed. Restart the app '
              + 'on your phone and try again.')
        quit()
    except OSError as e:
        if e.errno == errno.ETIMEDOUT:
            print('Connection timeout: Server is frozen. Restart the app on your phone.')
            quit()
        else:
            raise

    header = int(header)
    recvd_len = 0
    while recvd_len < header:
        response = sock.recv(BUFFSIZE)
        data += response
        recvd_len += len(response)

    decoded = data.decode(ENCODING, 'strict')
    # decoded = data.decode('ascii', 'ignore')
    # remove first newline
    decoded = decoded[1:]

    return decoded


# Helper for sending requests to the server
def contact_server(connectinfo, to_send):
    # print('sending:\n' + to_send)
    # print("...")
    sock = _connect_tcp(connectinfo)
    # print("Connected!")
    if sock is None:
        return None
    sock.send(bytes(to_send, ENCODING))
    response = _receive_all(sock)
    sock.close()

    return response

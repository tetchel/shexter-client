# Shexter - Shell Texter

Send and read texts from your Android phone using your \*nix or Windows command line. 
Sets up in seconds, and provides you with sending, reading and checking for unread messages on your phone!

[Get command-line client here](https://github.com/tetchel/shexter-client/raw/master/shexter_client.zip)

[Get apk here.](https://github.com/tetchel/tetchel.github.io/raw/master/app-release.apk) Source is private for now.

Or, download everything: `git clone https://github.com/tetchel/shexter.git`

## Demo
```
[ /shexter_client/installers/nix ] $ shexter help
usage: command [contact_name] [options]
You can also run "shexter help" to see commands and their options.

positional arguments:
  command               Possible commands: Send $ContactName, Read
                        $ContactName, Unread, Contacts, SetPref $ContactName,
                        Config. Not case sensitive.
  contact_name          Specify contact for SEND and READ commands.

optional arguments:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        Specify how many messages to retrieve with the READ
                        command. 20 by default.
  -m, --multi           Keep entering new messages to SEND until cancel signal
                        is given. Useful for sending multiple texts in
                        succession.
  -s SEND, --send SEND  Allows sending messages as a one-liner. Put your
                        message after the flag. Must be in quotes
  -n NUMBER, --number NUMBER
                        Specify a phone number instead of a contact name for
                        applicable commands.
[ /shexter_client/installers/nix ] $ shexter read dave
Error parsing /home/tim/.config/shexter/shexter.ini. Making a new one.
Broadcast addresses: ['192.168.1.255']
Searching for phones, can take a few seconds...
Searching on port 23456.
Got a response from ('192.168.1.198', 23456)
Phone info: SAMSUNG SM-G930W8 Android v7.0
Is this your phone? y/N: y

Dave has 2 numbers: 
1: Mobile: (226) 378-8862
2: Work: 1 231-231-234
Select a number from the above, 1 to 2: 1
--- September 02 ---
[15:53] You:   Hey how's it going
[15:53] Dave:  Hey how's it going
--- Saturday ---
[17:43] You:  Hey here's a test message
[17:43] Dave: Hey here's a test message
--- Yesterday ---
[15:53] You:  Hey here's another test message
[16:00] Dave: Hey here's another test message

[ /shexter_client/installers/nix ] $ shexter send dave
Enter message (Press Enter twice to send, CTRL + C to cancel): 
Hey Dave buddy how's it going

Successfully sent 1 message to Dave, Mobile: (226) 378-8862.
[ /shexter_client/installers/nix ] $ shexter unread
Unread Messages:
[00:31] Dave: Hey Dave buddy how's it going

[ /shexter_client/installers/nix ] $ shexter read dave -c 5
--- Saturday ---
[17:43] Dave: Hey here's a test message
--- Yesterday ---
[15:53] You:   Hey here's another test message
[16:00] Dave:  Hey here's another test message
--- Today ---
[00:31] You:  Hey Dave buddy how's it going
[00:31] Dave: Hey Dave buddy how's it going
```

## Client Setup

**Dependencies:** Python 3. On Linux, you must also have either 'ifconfig' or 'ip' installed (most systems will have these installed by default).

To install, extract the client archive, navigate to the installer for your platform, and run the installer (using `python .\installer_windows.py` or `sudo ./install_linux.sh`) through the command line. 
If the install is successful, after restarting your terminal, you should be able to run 'shexter' from anywhere, and consult the help `shexter help` to learn how to `shexter send` and `shexter read`.

### Contacting your Phone
Your phone and computer must be on the same LAN for the app to work. You can check if it is working with `shexter send -n $YourPhoneNumber`.

By default, the client will try and find your phone automatically by scanning your local network. 
If this fails, you can also configure the location of your phone manually using the IP address and Port presented in the app.
However, this will need to be updated every time you change WiFi networks, or reset your router. 
Your phone's network location is stored in a configuration file (eg. `C:\Users\You\AppData\Local\shexter\shexter.ini` or `/home/you/.config/shexter/shexter.ini`) which you are free to edit manually or use `shexter config` which will also display the config file location.

Note that, for now, Shexter ignores MMS messages altogether. Bear in mind that some normal-looking messages (such as group messages) are MMS.

### Fonts (Linux, Optional)

You are probably going to want Unicode font support in your terminal so your Unicode characters do not show as blocks.

[Arch Wiki page on Font Config](https://wiki.archlinux.org/index.php/font_configuration)

As an example:

For `rxvt-unicode`, a popular terminal emulator, you can set the following line in your `.Xresources` :
`URxvt*font: -xos4-terminus-medium-r-normal--14-140-72-72-c-80-iso10646-1, xft:WenQuanYi Micro Hei Mono,style=Regular, xft:Symbola`

The first font is a bitmap font in XLFD format. The other two are Xft format. The order depicts the glyph priority if there is overlap.

So this setting would show Terminus for ASCII, WenQuanYi Micro Hei Mono for Chinese, and Symbola for remaining Unicode characters such as emoji.

## App Setup

You must [enable installation from unknown sources](http://www.androidcentral.com/allow-app-installs-unknown-sources) in order to be able to install the apk.

Requires Contacts and SMS permissions. The app will refuse to operate without these permissions.

You may want to check your Security settings for your SMS message limit setting, which can prevent Shexter from sending frequent messages.

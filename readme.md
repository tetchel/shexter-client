# Shexter - Shell Texter

Send and read texts from your Android phone using your Linux or Windows command line. 
Sets up in seconds, and provides you with sending, reading and checking for unread messages, all with extreme ease!

[Get command-line client here](https://github.com/tetchel/shexter-client/raw/master/shexter_client.zip)

[Get apk here.](https://github.com/tetchel/tetchel.github.io/raw/master/app-release.apk) Source is private for now.

Or, download everything: `git clone https://github.com/tetchel/shexter.git` or `git clone ssh://git@github.com/tetchel/shexter.git`

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

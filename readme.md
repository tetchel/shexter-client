# Shexter - Shell Texter

Send and read SMS text messages from your Android phone using your \*nix or Windows command line. 

## Features
- Sets up in seconds with installation scripts
- Get desktop notifications when you receive a message
- Send messages to one of your contacts or to an arbitrary phone number
- View your contacts
- Read any of your text conversations in your terminal
- Ring your phone so you can find it, regardless of your volume setting
- Can easily be called from a cmdlet or script

- Fully supported on Windows and Linux. Some features are not supported on MacOS.

[Get command-line client here](https://github.com/tetchel/shexter-client/raw/master/shexter_client.zip)

[Get the app here](https://github.com/tetchel/shexter-client/raw/master/shexter.apk)

[Read a demo here](https://github.com/tetchel/shexter-client/blob/master/demo.md)

## Client Setup

**Dependencies:** Python 3. For automatic phone-finding, you need to `pip install netifaces`.

To install, extract the client archive, navigate to the installer for your platform, and run the installer:

**Windows**:   `python .\installer_windows.py` 

**Mac/Linux**: `sudo ./install_linux.sh`

If the install is successful, after restarting your terminal, you should be able to run 'shexter' from anywhere, and consult the `shexter help` to learn how to `shexter send` and `shexter read`.

### Contacting your Phone
Your phone and computer must be on the same LAN for the app to work.

By default, the client will try and find your phone automatically by scanning your local network. Make sure the app is open and visible (ie, your screen is on) when the client is searching for your phone.

If this fails, you can also configure the location of your phone manually using the IP address and Port presented in the app. Update this info by running `shexter config`.

Note that, for now, Shexter ignores MMS messages altogether. Bear in mind that some normal-looking messages (such as group messages) are MMS.

### Daemon Mode
On Windows and Linux, there is a daemon available `shexterd` to display notifications on your computer whenever you get a text.

See [the daemon readme](https://github.com/tetchel/shexter-client/blob/master/shexter_client/daemon-readme.md) for more.

## App Setup

You must [enable installation from unknown sources](http://www.androidcentral.com/allow-app-installs-unknown-sources) in order to be able to install the apk.

Requires Contacts and SMS permissions. The app will refuse to operate without these permissions.

You may want to check your Security settings for your SMS message limit setting, which can prevent Shexter from sending frequent messages.


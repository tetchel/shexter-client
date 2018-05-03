# ShexterD

The Shexter daemon notifies you whenever you get a new text message! It is supported on Windows and Linux. The daemon will work on MacOS and Bash for Windows, but it will just print to the console (no notifications).

On Windows, it requires you to `pip install win10toast`. On Linux, it requires you to have `notify-send` installed, which is included on many systems.

## How to Use
Just run `shexterd` after installation.

### How to run the daemon persistantly on LINUX using BASH:
```
$ shexterd & >/dev/null 2>&1         # NOTE: Logging is still done to shexterd.log even if you redirect output.

# Disown the job so you can close the terminal without killing the daemon.
$ disown -a         

# How to kill it:
# Get the PID
$ ps -ax | grep shexterd.py | grep -v grep
12862 pts/1    S      0:00 python3 ./shexterd.py

$ kill 12862

# Or, in one line:
$ kill $(ps -ax | grep shexterd.py | grep -v grep | awk "{ print $1 }" )
```

### How to run the daemon on LINUX as a SYSTEMD SERVICE:
```
# Copy the .service file to your systemd directory
sudo cp shexterd.service /lib/systemd/system/

# Use --user because shexter will check your $HOME variable
systemctl --user start shexterd.service

# To have it autostart on boot:
systemctl --user enable shexterd.service

```

### How to run the daemon persistantly on WINDOWS using Powershell:

```
PS C:\Users\you\AppData\Local\shexter\> Start-Process shexterd -WindowStyle hidden

# How to kill it: 

# First get the PID ("Id" column below)
PS E:\...\shexter_client> Get-Process -Name python

Handles  NPM(K)    PM(K)      WS(K)     CPU(s)     Id  SI ProcessName
-------  ------    -----      -----     ------     --  -- -----------
    198      19    15564      25228       0.23 240796   1 python

# Then stop that PID.
PS E:\...\shexter_client> stop-process 240796
```

### How to run the daemon on startup on WINDOWS
After running the installer, go to the directory shexter was installed to, eg. `C:\Users\you\AppData\Local\shexter` and right-click `shexterd.bat`, then select `Create Shortcut`.

Then copy the `shexterd` link to `C:\Users\you\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup` to install for your user.

After logging out and back in, shexter should start automatically. You do not need to repeat this process after upgrading shexter.
## How to run the daemon on LINUX using BASH:
```
# Make sure you are in the shexter_client directory
./shexterd.py & >/dev/null 2>&1         # NOTE: Logging is still done to shexterd.log even if you redirect output.

# Disown the job so you can close the terminal without killing the daemon.
disown -a         

# How to kill it:
# Get the PID
$ ps -ax | grep shexterd.py | grep -v grep
12862 pts/1    S      0:00 python3 ./shexterd.py

$ kill 12862

# Or, in one line:
kill $(ps -ax | grep shexterd.py | grep -v grep | awk "{ print $1 }" )
```

## How to run the daemon on LINUX as a SYSTEMD SERVICE:
```
# Copy the .service file to your systemd directory
sudo cp shexterd.service /lib/systemd/system/

# Use --user because shexter will check your $HOME variable
sudo systemctl --user start shexterd.service

# To have it autostart on boot:
sudo systemctl --user enable shexterd.service

```

## How to run the daemon on WINDOWS using Powershell:

```
# Make sure you are in the shexter_client directory
PS E:\...\shexter_client> Start-Process python -ArgumentList 'shexterd.py' -WindowStyle hidden

# How to kill it: 

# First get the PID ("Id" column below)
PS E:\...\shexter_client> Get-Process -Name python

Handles  NPM(K)    PM(K)      WS(K)     CPU(s)     Id  SI ProcessName
-------  ------    -----      -----     ------     --  -- -----------
    198      19    15564      25228       0.23 240796   1 python

# Then stop that PID.
PS E:\...\shexter_client> stop-process 240796
```

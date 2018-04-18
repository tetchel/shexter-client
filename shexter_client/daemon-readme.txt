# How to run the daemon on windows using Powershell:

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
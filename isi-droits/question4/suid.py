#!/usr/bin/env python3

import os 

# Get the current process’s  
# effective user id. 
euid = os.geteuid() 

# Get the current process’s  
# effective group id. 
egid = os.getegid() 

ruid = os.getuid() 
rgid = os.getgid() 

print("EUID", euid) 
print("EGID", egid) 
print("RUID", ruid) 
print("RGID", rgid) 


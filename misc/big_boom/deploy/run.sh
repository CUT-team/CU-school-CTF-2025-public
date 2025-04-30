#!/bin/bash
set -e
exec socat TCP-LISTEN:31337,reuseaddr,fork EXEC:"/opt/python3.7-custom/bin/python3 app.py",pty,stderr
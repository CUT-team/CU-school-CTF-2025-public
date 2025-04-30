#!/bin/sh

set -eux

apk update && apk add --no-cache openssh shadow coreutils bash

useradd -m -s /usr/local/bin/shell_wrapper.sh cuctf
echo "cuctf:cuctf" | chpasswd

chmod +x /usr/local/bin/shell_wrapper.sh

mkdir -p /home/cuctf
chown -R root:root /home/cuctf
chmod -R 755 /home/cuctf
chmod 444 /home/cuctf/flag.png

chmod o-rx /dev /media /mnt /opt /proc /root /run /sbin /srv /tmp /var

ssh-keygen -A
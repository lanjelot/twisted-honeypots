#!/bin/bash

export PYTHONPATH=/opt/honeypot/twisted/python
touch /var/log/{ssh,ftp,telnet}-pot.log
chown 1:1 /var/log/{ssh,ftp,telnet}-pot.log
twistd --uid=1 --gid=1 --logfile=/var/log/twistd-pot.log --pidfile=/var/run/twistd-pot.pid -y $PYTHONPATH/start-all-pot.tac

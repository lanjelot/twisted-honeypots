#!/bin/bash

source $(dirname $0)/vars.sh

touch /var/log/{ssh,ftp,telnet}-pot.log
chown 1:1 /var/log/{ssh,ftp,telnet}-pot.log
twistd --uid=1 --gid=1 --logfile=${TWISTED_LOG} --pidfile=${TWISTED_PID} -y ${PYTHONPATH}/start-all-pot.tac

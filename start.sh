#!/bin/bash

source $(dirname $0)/vars.sh

TAC_FILE="$(dirname $0)/python/start-all-pot.tac"
touch /var/log/{ssh,ftp,telnet}-pot.log
chown 1:1 /var/log/{ssh,ftp,telnet}-pot.log
twistd --uid=1 --gid=1 --logfile=${TWISTED_LOG} --pidfile=${TWISTED_PID} --python=${TAC_FILE}

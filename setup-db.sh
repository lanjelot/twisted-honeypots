#!/bin/bash

source $(dirname $0)/vars.sh

mysql -rs -uroot -p ${MYSQL_DB} <<EOF

CREATE DATABASE ${MYSQL_DB};
GRANT SELECT,INSERT,DELETE,UPDATE on ${MYSQL_DB}.* to '${MYSQL_USER}'@'localhost' identified by '${MYSQL_PWD}';
USE ${MYSQL_DB};
CREATE TABLE IF NOT EXISTS `pot` (
   `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
   `type` enum('ftp', 'ssh', 'telnet') NOT NULL,
   `login` varchar(255) NOT NULL,
   `password` varchar(255) NOT NULL,
   `host` varchar(255) NOT NULL,
   `timestamp` DATETIME(6),
   PRIMARY KEY (`id`)
);
EOF

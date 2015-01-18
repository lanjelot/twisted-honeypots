# twisted-honeypots
SSH, FTP and Telnet honeypot services based on the [Twisted](http://twistedmatrix.com/) engine.

The only reason I wrote these was to collect usernames and passwords from zombies scanning the Internet.

These honeypots only capture passwords, they cannot provide a shell.

## usage
```
$ sudo ./start.sh
$ sudo ./stop.sh
$ sudo ./restart.sh
```

## Pre-requisites
```
CREATE DATABASE pot_db;
GRANT SELECT,INSERT,DELETE,UPDATE on pot_db.* to 'pot_user'@'localhost' identified by 'password';
USE pot_db;
CREATE TABLE IF NOT EXISTS `pot` (
   `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
   `type` enum('ftp', 'ssh', 'telnet') NOT NULL,
   `login` varchar(255) NOT NULL,
   `password` varchar(255) NOT NULL,
   `host` varchar(255) NOT NULL,
PRIMARY KEY (`id`)
);
```

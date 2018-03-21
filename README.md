# twisted-honeypots

SSH, FTP and Telnet honeypot services based on the [Twisted](http://twistedmatrix.com/) engine for Python 3.
All credentials are stored on a local MySQL database.

This will create easily (and painlessly) very good dictionaries to use for pentesting.


## Install ##

```bash
$ git clone https://github.com/lanjelot/twisted-honeypots /opt/twisted-honeypots
$ cd /opt/twisted-honeypots
$ ./install.sh && ./setup.sh
```

## Usage ##

To start/stop the services:

```bash
$ sudo ./start.sh
$ sudo ./stop.sh
```


To monitor the current execution:

```bash
$ ./monitor.sh
```

![preview](https://i.imgur.com/5p4GR5z.png)


To extract the login/passwords in a wordlist sorted by best popularity:

```bash
$ source vars.sh
# logins
$ echo "select count(2),login from pot group by 2 order by count(2) desc" | mysql -rs -u${MYSQL_USER} ${MYSQL_DB}
# password
$ echo "select count(2),password from pot group by 2 order by count(2) desc" | mysql -rs -u${MYSQL_USER} ${MYSQL_DB}
```

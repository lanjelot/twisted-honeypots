# twisted-honeypots

SSH, FTP and Telnet honeypot services based on the [Twisted](http://twistedmatrix.com/) engine for Python 3.
All credentials are stored on a local MySQL database.


## Install ##

```bash
$ git clone https://github.com/lanjelot/twisted-honeypots /opt
$ cd /opt/twisted-honeypots
$ ./install.sh && ./setup.sh
```

## Usage ##

To start/stop the services:

```
$ sudo ./start.sh
$ sudo ./stop.sh
```


To monitor the current execution:

```
$ ./monitor.sh
```

![preview](https://i.imgur.com/5V2Kw4j.png)


To extract the login/passwords in a wordlist sorted by best popularity:

```
$ source vars.sh
# logins
$ echo "select count(2),login from pot group by 2 order by count(2) desc" | mysql -rs -u${MYSQL_USER} ${MYSQL_DB}
# password
$ echo "select count(2),password from pot group by 2 order by count(2) desc" | mysql -rs -u${MYSQL_USER} ${MYSQL_DB}
```

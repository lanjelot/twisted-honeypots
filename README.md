# twisted-honeypots

SSH, FTP and Telnet honeypot services based on the [Twisted](http://twistedmatrix.com/) engine for Python 3.
All credentials are stored on a local MySQL database.

This will create easily (and painlessly) very good dictionaries to use for pentesting.


## Install ##

```bash
$ git clone https://github.com/lanjelot/twisted-honeypots /opt/twisted-honeypots
$ cd /opt/twisted-honeypots
$ sudo ./install.sh && ./setup-db.sh
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
$ echo "select distinct login from pot group by login order by count(login) desc" | mysql -rs -u${MYSQL_USER} -p${MYSQL_PWD} ${MYSQL_DB}
# passwords
$ echo "select distinct password from pot group by password order by count(password) desc" | mysql -rs -u${MYSQL_USER} -p${MYSQL_PWD} ${MYSQL_DB}
```

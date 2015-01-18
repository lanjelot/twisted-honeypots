from twisted.application import service, internet
from ftppot import PotFTPFactory
from sshpot import PotSSHFactory
from telnetpot import PotTelnetFactory

dburl = 'pot_user:password@127.0.0.1:3306/pot_db'

application = service.Application('allpot')
serviceCollection = service.IServiceCollection(application)

internet.TCPServer(21, PotFTPFactory('/var/log/ftp-pot.log', dburl)).setServiceParent(serviceCollection)
internet.TCPServer(22, PotSSHFactory('/var/log/ssh-pot.log', dburl)).setServiceParent(serviceCollection)
internet.TCPServer(23, PotTelnetFactory('/var/log/telnet-pot.log', dburl)).setServiceParent(serviceCollection)

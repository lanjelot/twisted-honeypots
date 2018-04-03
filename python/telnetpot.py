from twisted.conch.insults import insults
from twisted.conch.telnet import TelnetTransport, StatefulTelnetProtocol
from twisted.internet import protocol
from common import PotFactory

class TelnetPotProtocol(StatefulTelnetProtocol):
    state = 'User'

    def telnet_Password(self, line):
        username, password = self.username, line
        del self.username
        self.factory.updatePot(username, password, self.transport.getPeer().host)
        self.transport.write(b"\nAuthentication failed\n")
        self.transport.write(b"Username: ")
        self.state = "User"
        return 'Discard'

    def connectionMade(self):
        self.transport.write(b"Username: ")

    def telnet_User(self, line):
        self.username = line
        self.transport.write(b"Password: ")
        return 'Password'

    def enableRemote(self, option):
        return False

    def disableRemote(self, option):
        pass

    def enableLocal(self, option):
        return False

    def disableLocal(self, option):
        pass

class PotTelnetFactory(protocol.ServerFactory, PotFactory):
    protocol = lambda a: TelnetTransport(TelnetPotProtocol)
    #welcomeMessage = 'Debian GNU/Linux 6.0'
    proto = 'telnet'

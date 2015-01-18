from twisted.conch.insults import insults
from twisted.conch.telnet import TelnetTransport, StatefulTelnetProtocol
from twisted.internet import protocol
from common import PotFactory

# I probably suck as I just could not get to use AuthenticatingTelnetProtocol
class TelnetPotProtocol(StatefulTelnetProtocol):
    state = 'User'

    def telnet_Password(self, line):
        username, password = self.username, line
        del self.username
        self.factory.updatePot(username, password, self.transport.getPeer().host)
        self.transport.write("\nAuthentication failed\n")
        self.transport.write("Username: ")
        self.state = "User"
        return 'Discard'

    def connectionMade(self):
        self.transport.write("Username: ")
 
    def telnet_User(self, line):
        self.username = line
        self.transport.write("Password: ")
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

# vim: ts=4 sw=4 sts=4 et

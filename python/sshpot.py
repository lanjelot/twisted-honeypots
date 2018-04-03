from twisted.application import internet
from zope.interface import implementer
from twisted.python import log

from twisted.cred import portal, checkers, error, credentials
from twisted.internet import reactor
from twisted.conch.ssh import factory, keys, transport, userauth, connection
from twisted.conch.ssh.common import getNS
from twisted.conch import unix, interfaces
from twisted.internet import defer
from common import PotFactory

import random

publicKey = b'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAwRDx36H79uAlt4aGFonJvm7V8cUttqShwg9eYHZnFNc/Sb5L+ERf1TnMx/eqcnFesBzbltdBfXfQkaRHNA1GHBGec0OcaDwGGXGMGWGyyUB8hB+7ftpyWbsCnN3qBSoGfIo1JnEUXpsQ0B0EnMiQqHo7TImG7LVSiV6tsUuhSWX8s3zXPLLcL/CCS+p6wK6Y7EmF+YylcOPkvG05Kvzzb6WWFFGop7/mqOLL9lrgYbjjsSQkQXR2NC2QunWkiB0/r2MaaeLamv4HUmPUw2lPgPlibpmnu1BkLayIXEOJiFEsDSCXm81IKj0aMez0f6FY8sDpd9lLnsFbjyOhzTmJ6w=='

privateKey = b'''-----BEGIN RSA PRIVATE KEY-----
MIIEoQIBAAKCAQEAwRDx36H79uAlt4aGFonJvm7V8cUttqShwg9eYHZnFNc/Sb5L
+ERf1TnMx/eqcnFesBzbltdBfXfQkaRHNA1GHBGec0OcaDwGGXGMGWGyyUB8hB+7
ftpyWbsCnN3qBSoGfIo1JnEUXpsQ0B0EnMiQqHo7TImG7LVSiV6tsUuhSWX8s3zX
PLLcL/CCS+p6wK6Y7EmF+YylcOPkvG05Kvzzb6WWFFGop7/mqOLL9lrgYbjjsSQk
QXR2NC2QunWkiB0/r2MaaeLamv4HUmPUw2lPgPlibpmnu1BkLayIXEOJiFEsDSCX
m81IKj0aMez0f6FY8sDpd9lLnsFbjyOhzTmJ6wIBIwKCAQB+3z/cGf1ZFvQ2xh2Z
yEK++GC00ggY79gDLqu7u4WRWj+IOzk8vzepYH9BlB+NCKvwEvazlMSi6FXcDN5V
Z878gJtTDyxEfzc1Sp3kyyxYXZOnSA1/Pxfx0qnyDiwSBax9uehpuAYSSKSmBHC+
zPFYxVoq+0oJQ/Ro5nIkDSDYdRFZpua+A17LBwzHtvYW2AdpajB5OpEH7KlFSmKk
MIPKmgNneEwzA1T8T8QahUu4rXpDz7l324E0142JQ1MBL5EZkcHnfM0ZqGW/gS7r
IQd5dT/88+HCi8BVs9KeR4JZ6UllBzRLE1e1lopP2crHPecViunrR97Uv9yfzLNI
CYxzAoGBAP9ZReMG7vX408OW6Jojp3soefTjfsLNhYoAm0JQL4ENdFKBQCBeXkTk
/cvqIwmc9yTWi50UKOzW11dNTC2InVqP4BYKLn2ay7jIMyn7A1Bsjn1A95KMmJuN
HU2ybnA/w5FHb/tIFf7BFJ0sSxTffI/r1lQliiYam7YKoeefCE1XAoGBAMGPAVJM
RFX3BuLpRIBkASi/ORrM4Ui4s29oo41FH3It4rjUORRUy92oHbQ8526rucIEGaSY
S2uz4a/1U7Xnbym10bvpLhnC5CMCmJsJjMcvEYPOGLKBGsVVy3+4+PnhH3j/bf7W
VxHaZMvwS1IBpTG5nMINqiBWqKOyuYf4OPeNAoGAQak920rs/WverqMl3n4yYX9v
0UHQI3atT1893doa2ArGI9gXzc8fjg7/bvMQUu3ZJrrTcYjXUtgovq15/RSAO9va
iVMTRN6pageYILzjmFZtyG/KogbladPUVc7L8Pp0HgsOKqwi6bye5pZccxTlhBgS
iqqRPP+HIC6eqUYmtM0CgYBH5Ki4KvTPeQKOy6u6qM07BTJ3qy8bAsZN86p2TN/L
Ut8utTnFuRiFh5YBHe+PgZzEZ+xEcxSy+auZIJtvczfq68LuBicQ4fz3D5fEjoS/
Atqeq6LF9XBX7KqryFx6EcncfCGKiiBXFpp3omUedaPCAxz3nqzncKUJmieniBUo
vwKBgQC8OmAPoKip8A7lULQLvoh89YfzKyNHKdALUNxvnkIOA6H7WsvZdXf4X1ZI
QtQxVFRL0Sku0RkCYhrERVHh3qRggMJS1fVPKXpyF0fwx4B1cY45eI8TiMOj/RFw
sjkxOmqTu1e8ukszRCMO4z/BOpkZisT2nELtXcZFtOJcyxpODg==
-----END RSA PRIVATE KEY-----'''

@implementer(portal.IRealm)
class MockRealm:

    def requestAvatar(self, avatarId, mind, *interfaces):
        return defer.succeed((interfaces[0], None, lambda: None))

class MockChecker(checkers.InMemoryUsernamePasswordDatabaseDontUse):
    def requestAvatarId(self, credentials):
        return defer.fail(error.UnauthorizedLogin())

class PotSSHServerTransport(transport.SSHServerTransport):
    ''' if I support any other ciphers here, I get "bad packet length" errors
    with ssh-bots based on early libssh versions (0.1 or 0.2).
    '''
    supportedCiphers = [b'aes128-cbc', ]

    # marche avec twisted 11.0.0
    def connectionMade(self):
        ''' Same as parent except that we do not call self.sendKexInit()
        because we do not want to send anything on the wire other than the
        banner after a CONNECT (ie. behave like a genuine OpenSSH server).
        '''
        self.transport.write(b'%s\r\n' % (self.ourVersionString,))
        self.currentEncryptions = transport.SSHCiphers(b'none', b'none', b'none', b'none')
        self.currentEncryptions.setKeys(b'', b'', b'', b'', b'', b'')

    def dataReceived(self, data):
        ''' Same as parent except that we need to call self.sendKexInit()
        after checking the client version because I have seen ssh-bots based on early
        libssh versions (0.1 or 0.2) that expect us to initiate the Key Exchange Init,
        otherwise they timeout and close the TCP connection.
        '''
        self.buf = self.buf + data
        if not self.gotVersion:
            if self.buf.find(b'\n', self.buf.find(b'SSH-')) == -1:
                return
            lines = self.buf.split(b'\n')
            for p in lines:
                if p.startswith(b'SSH-'):
                    self.gotVersion = True
                    self.otherVersionString = p.strip()
                    remoteVersion = p.split(b'-')[1]
                    if remoteVersion not in self.supportedVersions:
                        self._unsupportedVersionReceived(remoteVersion)
                        return
                    i = lines.index(p)
                    self.buf = b'\n'.join(lines[i + 1:])

                    log.msg('Client version: %s' % self.otherVersionString) # stats
                    self.sendKexInit() # dirty workaround for buggy ssh-bots

        packet = self.getPacket()
        while packet:
            messageNum = packet[0]
            self.dispatchMessage(messageNum, packet[1:])
            packet = self.getPacket()

class PotSSHUserAuthServer(userauth.SSHUserAuthServer):
    attemptsBeforeDisconnect = 3 # same as OpenSSH

    def auth_password(self, packet):
        password = getNS(packet[1:])[0]
        host = self.transport.transport.getPeer().host
        self.transport.factory.updatePot(self.user, password, host)
        return None

class PotSSHFactory(factory.SSHFactory, PotFactory):
    proto = 'ssh'

    protocol = PotSSHServerTransport
    services = {b'ssh-userauth': PotSSHUserAuthServer}

    publicKeys = {b'ssh-rsa': keys.Key.fromString(publicKey)}
    privateKeys = {b'ssh-rsa': keys.Key.fromString(privateKey)}

    def __init__(self, logfile=None, dburl=None):
        PotFactory.__init__(self, logfile, dburl)

        self.portal = portal.Portal(MockRealm(), (MockChecker(),))
        self.protocol.ourVersionString = random.choice([b'SSH-2.0-OpenSSH_5.5p1 Debian-6',
                                                        b'SSH-2.0-OpenSSH_6.4p1-hpn14v2 FreeBSD-openssh-portable-6.4.p1,1',
                                                        b'SSH-2.0-OpenSSH',
                                                        b'SSH-2.0-OpenSSH_6.7p1 Raspbian-5+deb8u4',
                                                        b'SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.10',
                                                        b'SSH-2.0-dropbear_0.52',
                                                        b'SSH-1.99-Cisco-1.25',])

if __name__ == '__main__':
    t = PotSSHFactory()

    reactor.listenTCP(2222, t)
    reactor.run()

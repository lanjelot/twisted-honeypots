from zope.interface import Interface, implements
from twisted.application import internet
from twisted.protocols import basic, policies
from twisted.internet import protocol, reactor, defer
from twisted.python import log
from re import match
from common import PotFactory


WELCOME_MSG                   = b'220'
GOODBYE_MSG                   = b'221'

USER_OK_NEED_PASS             = b'331'

PLEASE_LOGIN                  = b'503'
UNKNOWN_COMMAND               = b'500'
LOGIN_WITH_USER_FIRST         = b'503'
LOGIN_FAIL                    = b'530'
REQ_ACTN_NOT_TAKEN            = b'550'

RESPONSE = {
    WELCOME_MSG:              b'220 %s',
    GOODBYE_MSG:              b'221 Goodbye.',

    USER_OK_NEED_PASS:        b'331 Please specify the password.',

    PLEASE_LOGIN:             b'530 Please login with USER and PASS.',
    UNKNOWN_COMMAND:          b'500 Unknown command.',
    LOGIN_WITH_USER_FIRST:    b'503 Login with USER first.',
    LOGIN_FAIL:               b'530 Login incorrect.',
    REQ_ACTN_NOT_TAKEN:       b'550 Requested action not taken: %s',
}

class FTPpot(basic.LineOnlyReceiver, policies.TimeoutMixin):

    delimiter = b'\n'
    disconnected = False
    UNAUTH, INAUTH = range(2)

    ''' So that FTP clients that use '\n' instead of '\r\n'
        receive responses anyway '''
    def sendLine(self, msg):
      basic.LineOnlyReceiver.sendLine(self, msg+b'\r')

    def reply(self, key, *args):
        msg = RESPONSE[key] % args
        self.sendLine(msg)

    def connectionMade(self):
        self.state = self.UNAUTH
        self.reply(WELCOME_MSG, self.factory.welcomeMessage)

    def connectionLost(self, reason):
        self.setTimeout(None)
        self.transport = None

    def timeoutConnection(self):
        self.transport.loseConnection()

    def lineReceived(self, line):
        self.resetTimeout()

        def processFailed(err):
            #if err.check(FTPCmdError):
            #    self.sendLine(err.value.response())
            #else:
            log.msg("Unexpected FTP error")
            log.err(err)

        def processSucceeded(result):
            if isinstance(result, tuple):
                self.reply(*result)
            elif result is not None:
                self.reply(result)

        d = defer.maybeDeferred(self.processCommand, line)
        d.addCallbacks(processSucceeded, processFailed)
        d.addErrback(log.err)

    def processCommand(self, line):
        if not line: return
        cmd, args = match(b'(\S+)\s*(.*)$', line.rstrip()).groups()
        cmd = cmd.upper()

        if cmd == b'USER':
            if self.state != self.UNAUTH:
                return PLEASE_LOGIN
            else:
                return self.ftp_USER(args)

        elif cmd == b'PASS':
            if self.state != self.INAUTH:
                return LOGIN_WITH_USER_FIRST
            else:
                return self.ftp_PASS(args)

        else:
            method = getattr(self, "ftp_" + cmd.decode("utf8"), None)
            if method is not None:
                return method(line)
            else:
                return PLEASE_LOGIN

    def ftp_USER(self, username):
        self.username = username
        self.state = self.INAUTH
        return USER_OK_NEED_PASS

    def ftp_PASS(self, password):
        self.factory.updatePot(self.username, password, self.transport.getPeer().host)
        self.state = self.UNAUTH
        del self.username
        return LOGIN_FAIL

    def ftp_FEAT(self, line):
        self.sendLine(b'211-Features:')
        for i in b'EPRT,EPSV,MDTM,PASV,REST STREAM,SIZE,TVFS,UTF8'.split(b','):
            self.sendLine(b' %s' % i)
        self.sendLine(b'211 End')

    def ftp_QUIT(self, line):
        self.reply(GOODBYE_MSG)
        self.transport.loseConnection()
        self.disconnected = True

class FTPCmdError(Exception):
    """
    Generic exception for FTP commands.
    """
    def __init__(self, *msg):
        Exception.__init__(self, *msg)
        self.errorMessage = msg

    def response(self):
        """
        Generate a FTP response message for this error.
        """
        return RESPONSE[self.errorCode] % self.errorMessage

class PotFTPFactory(protocol.ServerFactory, PotFactory):
    protocol = FTPpot
    welcomeMessage = b'vsFTPd 2.3.4'
    proto = 'ftp'

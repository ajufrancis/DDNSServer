import dns.query
import dns.tsigkeyring
import dns.update
from ddnsserver.Config import DNS_SERVER, DNS_ZONE, DNS_KEYRING, DNS_TTL


class DNSupdater(object):

    __host = None
    __keyring = None
    __update = None
    
    def __init__(self):
        
        self.__keyring = dns.tsigkeyring.from_text(DNS_KEYRING)
        self.__update = dns.update.Update(DNS_ZONE, keyring=self.__keyring)

    def performUpdate(self, hostname, newIP):
        
        try:
            hostname = hostname.replace('.%s' % DNS_ZONE[0:-1], '')
            self.__update.replace(hostname, DNS_TTL, 'A', newIP)
            response = dns.query.tcp(self.__update, DNS_SERVER)
            
            if response.rcode() == 0:
                return True
            else:
                return False

        except:
            return False
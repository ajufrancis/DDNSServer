import ConfigParser


class Account(object):
    
    __abuse = 0
    __username = None
    __hostnames = {}
    __password = None
    
    # Abuse
    def getAbuse(self):
        return self.__abuse
    
    def incrementAbuse(self):
        self.__abuse += 1
        return self.getAbuse()
    
    def resetAbuse(self):
        self.__abuse = 0
        return self.getAbuse()
    
    # Username
    def getUsername(self):
        return self.__username
    
    def updateUsername(self, newUsername):
        self.__username = newUsername
        return self.getUsername()
    
    # Hostname
    def getHostnames(self):
        return self.__hostnames
    
    def hostnameAvailable(self, hostname):
        if hostname in self.__hostnames.keys():
            return True
        else:
            return False
    
    def addHostname(self, hostname, ip):
        self.__hostnames.update( { hostname : ip } )
        return True
    
    def updateHostname(self, hostname, ip):
        if self.hostnameAvailable(hostname):
            self.__hostnames[hostname] = ip
            return True
        else:
            return False  
    
    # Password
    def passwordMatch(self, password):
        if self.__password == password:
            return True
        else:
            return False
        
class DBHandler(object):
    pass
    

from configparser import ConfigParser
from ddnsserver.Config import DB_PATH
from os.path import isfile
from time import strftime

class DBHandler(object):
    
    parser = None
    
    def __init__(self):
        try:
            self.parser = ConfigParser()
            
            if isfile(DB_PATH):
                self.parser.read(DB_PATH, encoding='utf-8')
                print('DB wurde eingelesen: %s' % DB_PATH)
            else:
                print('%s kann nicht gelsen werden oder exsistiert nicht.' % DB_PATH) 
        except Exception as ex:
            print('Fehler beim einlesen der DB! >> %s' % str(ex))
    
    def commit(self):
        with open(DB_PATH, 'w') as configfile:
            self.parser.write(configfile)
    
    def userExists(self, username):
        if username in self.parser.sections():
            return True
        else:
            raise UserWarning('badauth')
    
    def valueExists(self, username, argument):
        if self.userExists(username):
            if self.parser.has_option(username, argument):
                return True
            else:
                return False
        else:
            return False
    
    def passwordMatch(self, username, password):
        if self.valueExists(username, 'password'):
            storedPassword = self.parser.get(username, 'password')
        else:
            raise UserWarning('badauth')
        
        if  storedPassword == password:
            return True
        else:
            raise UserWarning('badauth')
    
    # Abuse
    def checkAbuse(self, username):
                
        if self.valueExists(username, 'abuse'):
            abuse = self.parser.getint(username, 'abuse')
            
            if abuse > 3:
                raise UserWarning('abuse')
            else:
                return True
            
        else:
            try:
                self.parser.set(username, 'abuse', '0')
            except:
                raise UserWarning('configerror')
            return self.checkAbuse(username)
    
    def incrementAbuse(self, username):
        if self.valueExists(username, 'abuse'):
            value = self.parser.getint(username, 'abuse')
            value += 1

            self.parser.set(username, 'abuse', str(value))
            self.updateLastEdit(username)
            return True                             
        else:
            raise UserWarning('911')      
        
    def getHostname(self, username):
        if self.valueExists(username, 'hostname'):
            return self.parser.get(username, 'hostname')
        else:
            raise UserWarning('configerror')
    
    def getIP(self, username):
        if self.valueExists(username, 'myip'):
            return self.parser.get(username, 'myip')
        else:
            raise UserWarning('noip')
        
    def updateIP(self, username, newIP):
        try:
            self.parser.set(username, 'myip', newIP)
            self.updateLastEdit(username)
            return True
        except Exception as ex:
            raise UserWarning('911')
    
    def updateLastEdit(self, username):
        ''' 
            ist latte ob es die Value nicht gibt...
            gesetzt wird diese hier dann auf jeden fall!
        '''
        if self.userExists(username):
            try:
                self.parser.set(username, 'lastupdate', strftime("%d.%m.%Y - %H:%M:%S"))
                self.commit()
            except:
                raise UserWarning('911')
        
        
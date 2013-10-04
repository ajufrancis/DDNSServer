from http.server import BaseHTTPRequestHandler
from base64 import b64decode
from hashlib import md5
from ddnsserver import DBHandler, DNSupdater
from urllib.parse import parse_qs

class RequestHandler(BaseHTTPRequestHandler):
    
    db = DBHandler()
    dns = DNSupdater()
                
    def response(self, code, msg):
        # header setzen
        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        # Antwort geben
        self.wfile.write(msg.encode())
    
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"eBIS_DDNS\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        
        if self.path == '/':
            self.response(200, 'Current IP Address: ' + self.client_address[0])
        elif '/update?' in self.path:

            if self.headers.get('Authorization') == None:
                self.do_AUTHHEAD()
            elif self.headers.get('Authorization') != None:
                auth = self.headers.get('Authorization')
                auth = auth.replace('Basic ', '')
                auth = b64decode(auth).decode()  
                           
                username, password = auth.split(':')
                password = md5(password.encode()).hexdigest()
                                
                # AbfrageHORRORRRRRRRRRRR
                try:
                    ''' 
                        Erste Hürde
                        
                        * gibts den User?
                        * stimmt das Passwort?
                        * Abuse-Status in Ordnung?
                    '''
                    
                    self.db.userExists(username)
                    self.db.passwordMatch(username, password)
                    self.db.checkAbuse(username)
                    
                    '''
                        Zweite Hürde
                    '''
                    vars = parse_qs(self.path.replace('/update?', ''))
                    
                    if 'hostname' and 'myip' not in vars:
                        raise UserWarning('badparam')
                   
                    # @TODO REGEX HOSTNAME
                    # @TODO REGEX IP 
                    
                    hostname = vars['hostname'][0]
                    ip = vars['myip'][0]
                    
                    if hostname != self.db.getHostname(username):
                        raise UserWarning('nohost')
                    
                    oldIP = self.db.getIP(username)
                    
                    if ip == oldIP:
                        self.db.incrementAbuse(username)
                        raise UserWarning('abuse')
                    
                    if self.db.updateIP(username, ip):
                        if self.dns.performUpdate(hostname, ip):
                            self.response(200, 'good')
                        else:
                            self.db.updateIP(username, oldIP)
                            raise UserWarning('dnserror')
                    else:
                        raise UserWarning('dberror')
                    
                    ''' Änderrungen speichern '''
                    self.db.commit()

                except UserWarning as uw:
                    self.response(400, str(uw))
                except Exception as ex:
                    print(str(ex))
                    self.response(400, '911')

        else:
            self.response(400, 'badauth')
            return False
        
        return True
from http.server import BaseHTTPRequestHandler
from base64 import b64decode
from hashlib import md5
from ddnsserver import DBHandler

class RequestHandler(BaseHTTPRequestHandler):
                
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
                                
                # 'DB' abfragen
                try:
                    
                    pass
                      
                except IOError as ioerr:
                    print(str(ioerr))
                    self.response(400, '911')
                except Exception as ex:
                    print(str(ex))
                    self.response(400, '4711')
                
            '''vars = parse.parse_qs(self.path.replace('/update?', ''))
            print(vars)'''

        else:
            self.response(400, 'badauth')
            return False
        
        return True
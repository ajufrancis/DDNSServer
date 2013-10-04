#!/usr/bin/python3

import signal
from ddnsserver import RequestHandler
from ddnsserver.Config import SCRIPT_NAME, HTTP_SERVER, HTTP_PORT, PID_FILE
from http.server import HTTPServer
from sys import exit
from os import getpid, unlink
from os.path import isfile, exists

class Server(object):
    
    server = None
    pid = None
    
    def reload(self, signal, frame):
        print('Führe Neustart durch ...')
        self.__del__() # HTTP-Server beenden
        self.__init__() # HTTP-Server neu initialisieren
    
    def __init__(self):
        
        # Signalhandler
        signal.signal(signal.SIGCONT, self.reload)
        signal.signal(signal.SIGHUP, self.__del__)
        
        try:       

            # Lockfile
            if(isfile(PID_FILE)):
                print('Lockfile %s exsistiert bereits' % PID_FILE)
                
                currentPid = open(PID_FILE, mode='r').read()
                
                if exists('/proc/%s' % currentPid):
                    exit(1)
                else:
                    print('Kein laufender Prozess mit PID %s gefunden!' % currentPid)
                    print('Lösche Lockfile %s' % PID_FILE)
                    
                    unlink(PID_FILE)
            
            print('Starte %s' % SCRIPT_NAME)
            
            self.pid = str(getpid())
            open(PID_FILE, mode='w+').write(self.pid)
            
            print('Lockfile unter %s erstellt. PID: %s' % (PID_FILE, self.pid))

            serverSettings = (HTTP_SERVER, HTTP_PORT)
            self.server = HTTPServer(serverSettings, RequestHandler)
            
            print('HTTP-Server wird gestartet [%s:%s]' % serverSettings)
            
            self.server.serve_forever()
            
        except KeyboardInterrupt:
            print(' Interrupt empfangen, HTTP-Server wird beendet.')
            exit(0)
    
    def __del__(self, signal=None, frame=None):
        
        if self.server != None:
            print('Beende %s' % SCRIPT_NAME)
            self.server.socket.close()
        
        if isfile(PID_FILE) and self.pid != None:
            print('Entferne Lockfile %s' % PID_FILE)
            unlink(PID_FILE)

if __name__ == "__main__":
        
    server = Server()
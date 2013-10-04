
# Allgemeines
SCRIPT_NAME='DDNS-HTTPServer'
PID_FILE='/tmp/%s' % SCRIPT_NAME

# HTTP-Server Settings
HTTP_SERVER='192.168.2.124'
HTTP_PORT=8000

# DBHANDLER
DB_PATH='/usr/local/etc/ddns.db'

# DNSHANDLER
DNS_SERVER='192.168.x.x'
DNS_ZONE='zone.foo.com.'
DNS_TTL=60
DNS_KEYNAME = 'ddns-key'
DNS_KEY='abcdef=='
DNS_KEYRING = { DNS_KEYNAME : DNS_KEY }

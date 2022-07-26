import pymysql
from sshtunnel import SSHTunnelForwarder

def Siapdb():
    port = 3307
    s = 'localhost'
    d = 'siap'
    u = 'root'
    p = 'apaajadeh123'
    connS = pymysql.connect(host=s, port=port, user=u, password=p, database=d)
    return connS


def iteungDB():
    global tunnel
    tunnel = SSHTunnelForwarder(('croot.ypbpi.or.id', 60606), ssh_password='u>|0w66@$1L =4z', ssh_username='osdep',
    remote_bind_address=('10.14.200.20', 42136)) 
    tunnel.start()
    port = 42136
    s = 'localhost'
    d = 'wanda'
    u = 'root'
    p = 'rollyganteng'
    conni = pymysql.connect(host=s, port=tunnel.local_bind_port, user=u, password=p, database=d)
    return conni


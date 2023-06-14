from OpenSSL import crypto, SSL
def cert_gen(
        emailAddress="emailAddress",
        commonName="commonName",
        countryName="NT",
        localityName="localityName",
        stateOrProvinceName="stateOrProvinceName",
        organizationName="organizationName",
        organizationUnitName="organizationUnitName",
        serialNumber=0,
        validityStartInSeconds=0,
        validityEndInSeconds=10 * 365 * 24 * 60 * 60,
        KEY_FILE="server.key",
        CERT_FILE="server.crt"):
    # can look at generated file using openssl:
    # openssl x509 -inform pem -in selfsigned.crt -noout -text
    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)
    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = countryName
    cert.get_subject().ST = stateOrProvinceName
    cert.get_subject().L = localityName
    cert.get_subject().O = organizationName
    cert.get_subject().OU = organizationUnitName
    cert.get_subject().CN = commonName
    cert.get_subject().emailAddress = emailAddress
    cert.set_serial_number(serialNumber)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(validityEndInSeconds)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha512')
    with open(CERT_FILE, "wt") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
    with open(KEY_FILE, "wt") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))
import ssl
import socket
import select
import json
from clients import cli
from clients import group
from hashlib import sha256
from users import user_saver
f=user_saver()
def hashs(pas):
    return sha256(pas.encode('utf-8')).hexdigest()
passs=hashs("passwordpoiu")
cert_gen()
server = socket.socket()
server=ssl.wrap_socket(server,cert_reqs=ssl.CERT_NONE,server_side=True,keyfile="server.key",certfile="server.crt")
hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
server.bind((IPAddr, 1729))
server.listen()
clients = group("all",[],None)
groups=[]
messages = []
model=None
def groupss(gr=groups):
    grp=""
    for g in gr:
        grp+=g.name+", "
    return grp
def find_g_by_name(u,gr=groups):
    for grps in gr:
        if u==grps.name:
            return grps
    return None
def find_u_by_name(u,gr=clients):
    for clin in gr.cli_l:
        if clin.name==u:
            return clin
    return None
def find_name_by_clnt(u,gr=clients):
    for clin in gr.cli_l:
        if clin.clnt==u:
            return clin
    return None
while True:
    #rlist - לקוחות שמהם קוראים מידע (read)
    #wlist - לקוחות שאליהם שולחים מידע (write)
    #xlist - לקוחות שהחיבור איתם כשל (exception)
    rlist, wlist, xlist = select.select([server] + clients.clnt(), clients.clnt(), [])
    for client in rlist:
        if client is server: #אם אין client
            print('new client joined')
            clnt, address = client.accept()
            u= cli("plh",clnt,address)
            clients.cli_l.append(u)
        else:
            n=find_name_by_clnt(client)
            if n.name=="plh":
                message =client.recv(1024).decode().split(",")
                print(message)
                if message==[''] or message==['leave']:
                    print(n.name + " exit")
                    clients.kick(n)
                elif message[0] == "model" and len(message)==1:
                    n.name=message[0]
                    model=n
                elif message[1] == passs and message[0] == "1":
                    print("admin")
                    client.send(("admin").encode())
                    n.name = message[0]
                    admin=n
                elif [(message[1],)]==f.get_wh("id", "pass", "name = '"+message[0]+"'"):
                    n.name = message[0]
                    client.send(("rejoin").encode())
                elif message[0] == 1 or [(message[0],)]==f.get_wh("id", "name", "name = '"+message[0]+"'"):
                    client.send(("rename").encode())
                else:
                    f.add("id",message[0],message[1])
                    n.name = message[0]
                    client.send(("join").encode())
            elif n.name=="model":
                try:
                    message = client.recv(1024).decode().split(",")
                    n = find_u_by_name(message[1])
                    n.clnt.send(message[0].encode())
                except IndexError:
                    print(n.name + " exit")
                    clients.kick(n)

            elif n.name=="1":
                message = client.recv(1024).decode().split(",")
                print(n.name,f.get_wh("id", "*", "name = '"+message[0]+"'"))
                if message[0] == "exit":
                    print(n.name + "exit")
                    n.name = "plh"
                elif f.get_wh("id", "*", "name = '"+message[0]+"'") !=[]:
                    al = "False"
                    if message[2] == "allow":
                        al = "True"
                    print(message)
                    f.update("id","name='"+message[0]+"'",message[1]+"='"+al+"'")
                    client.send("True".encode())
                else:
                    try:
                        client.send("False".encode())
                        print(n.name, " no such client")
                    except ssl.SSLEOFError:
                        print(n.name + " exit")
                        clients.kick(n)


            else:
                message = client.recv(16384).decode()

                if message=="leave":
                    print(n.name + "exit")
                    clients.kick(n)
                elif message=="exit":
                    print(n.name+"exit")
                    n.name="plh"
                else:
                    #print(message)
                    try:
                        messag=json.loads(message)
                        if (messag.get("name")=="ask" and f.get_wh("id", "ask", "name = '"+n.name+"'")[0][0])=="True" or (not messag.get("name")=="ask" and f.get_wh("id", "tell", "name = '"+n.name+"'")[0][0]=="True"):
                            model.clnt.send((message + "@" + n.name).encode())
                        else:
                            print(n.name," not alowed")
                            client.send("False".encode())
                    except json.decoder.JSONDecodeError:
                        print(n.name + " exit")
                        clients.kick(n)

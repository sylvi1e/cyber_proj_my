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
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import socket, json
from hashlib import sha256
from draw import draw as dr
from draw import show
import ssl
from sys import getsizeof
cert_gen(KEY_FILE="cli.key",CERT_FILE="cli.crt")
client = socket.socket()
client=ssl.wrap_socket(client,cert_reqs=ssl.CERT_NONE,server_side=False,keyfile="cli.key",certfile="cli.crt")
hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
client.connect((IPAddr, 1729))
'''context = ssl.create_default_context()

with socket.create_connection((hostname, 443)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        print(ssock.version())'''
def hash(pas):
    return sha256(pas.encode('utf-8')).hexdigest()

def hashs(pas):
    return sha256(pas.encode('utf-8')).hexdigest()
class Root(tk.Tk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = tk.Label(self)
        self.page.grid()
        self.change_page(page_1)
        self.geometry("1000x500")
        self.state('zoomed')
    def change_page(self,other):
        self.page.destroy()
        self.page = other(self)
        self.page.grid()

class page_1(tk.Frame):
    def __init__(self,root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        def printInput():
            inp=inputuser.get(1.0, "end-1c")+","+ hashs(inputtxt.get(1.0, "end-1c")+"poiu")
            if inputuser.get(1.0, "end-1c")== "" or  inputtxt.get(1.0, "end-1c")=="":
                messagebox.showwarning("change_name", "change_name")
                return False
            client.send(inp.encode())
            message =client.recv(1024).decode()
            print(message)
            if message=="join":
                messagebox.showinfo("join", "welcome")
                root.change_page(page_2)
            elif message=="rejoin":
                messagebox.showinfo("rejoin", "welcomeback")
                root.change_page(page_2)
            elif message=="rename":
                messagebox.showwarning("change_name", "change_name")
            elif message=="admin":
                messagebox.showinfo("admin", "welcome")
                root.change_page(page_3)
            else:
                messagebox.showerror("error", "server failed please disconect")
                root.change_page(page_e)
        inputuser = tk.Text(self,height=1,width=20)
        inputuser.grid()
        lbl = tk.Label(self, text="username")
        lbl.grid()
        inputtxt = tk.Text(self, height=1, width=20)
        inputtxt.grid()
        lbl2 = tk.Label(self, text="password")
        lbl2.grid()
        printButton = tk.Button(self,text="submit",command=printInput)
        printButton.grid()

        '''self.my_button = tk.Button(self, text = 'hi', command=lambda: root.change_page(page_2))
        self.my_button.grid()'''
class page_e(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.shape = []
        def disc():
            quit()
        lbl = tk.Label(self, text="server failed please disconect")
        lbl.grid()
        my_button = tk.Button(self, text='exit', command=lambda: disc())
        my_button.grid()
class page_3(tk.Frame):
    def __init__(self,root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.shape=[]
        def ret():
            client.send("exit".encode())
            root.change_page(page_1)
        def send_a():
            inp = input.get(1.0, "end-1c")
            if (current_var.get()!="ask" and  current_var.get()!="tell") or (current_var0.get()!="allow" and  current_var0.get()!="disallow"):
                messagebox.showwarning("shape", "can't recive properly")
                return False
            client.send((inp+","+current_var.get()+","+current_var0.get()).encode())
            responde = client.recv(1024).decode()
            print(responde)
            if responde=="True":
                messagebox.showinfo("passed succesfully", "passed succesfully")
            else:
                messagebox.showerror("no such user", "no such user")
        my_button = tk.Button(self, text='exit', command=lambda: ret())
        my_button.grid()
        input = tk.Text(self, height=1, width=20)
        input.grid()
        lbl = tk.Label(self, text="client_username")
        lbl.grid()
        current_var = tk.StringVar()
        combobox = ttk.Combobox(self, textvariable=current_var, values=("ask", "tell"), state='normal')
        combobox.current(0)
        combobox.grid()
        current_var0 = tk.StringVar()
        combobox0 = ttk.Combobox(self, textvariable=current_var0, values=("allow", "disallow"), state='normal')
        combobox0.current(0)
        combobox0.grid()
        my_button = tk.Button(self, text='send', command=lambda: send_a())
        my_button.grid()
        lbl0 = tk.Label(self, text="_")
        lbl0.grid()

class page_2(tk.Frame):
    def __init__(self,root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.shape=[]
        def ret():
            client.send("exit".encode())
            root.change_page(page_1)
        def draws():
            self.shape = dr()
            if getsizeof(self.shape)>16384:
                messagebox.showerror("Not Allowed", "shape too big")
                draws()
        def tell_arr():
            data = json.dumps({"shape": self.shape, "name": current_var.get()})
            print(current_var.get())
            if not current_var.get() in shapes:
                messagebox.showwarning("shape", "choose a shape")
                return False
            client.send(data.encode())
            responde=client.recv(1024).decode()
            print(responde)
            if responde=="False":
                messagebox.showerror("Not Allowed", "Not Allowed")
            else:
                messagebox.showinfo("Thanks For Sending", "Thanks For Sending")
        def ask_arr():
            data = json.dumps({"shape": self.shape, "name": "ask"})
            print("ask")
            client.send(data.encode())
            responde=client.recv(1024).decode()
            print(responde)
            if responde=="False":
                lbl.config(text="Not Allowed")
            else:
                messagebox.showinfo("Last Shape Input", responde)
                lbl.config(text="Last Shape Input: " + responde)

        shapes=("circle", "tri","square")
        my_button = tk.Button(self, text = 'exit', command=lambda: ret())
        my_button.grid()
        my_button2 = tk.Button(self, text='draw', command=lambda:draws())
        my_button2.grid()
        my_button3 = tk.Button(self, text='print shp', command=lambda: print(self.shape))
        my_button3.grid()
        my_button4 = tk.Button(self, text='ask shp', command=lambda: ask_arr())
        my_button4.grid()
        my_button5 = tk.Button(self, text='tell shp', command=lambda: tell_arr())
        my_button5.grid()
        current_var = tk.StringVar()
        combobox = ttk.Combobox(self, textvariable=current_var ,values=shapes,state='normal')
        combobox.current(0)
        combobox.grid()
        my_button6 = tk.Button(self, text='show shp', command=lambda: show(self.shape))
        my_button6.grid()
        lbl = tk.Label(self, text="shape")
        lbl.grid()

a = Root()
a.mainloop()
client.send("leave".encode())


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
from tensorflow import keras as tf
import socket
import numpy as np
import json
import threading
from q import shape_saver
import random
f= shape_saver()
def shape_to_mat(POINTS):
    def crop(line):
        miny, minx = 501, 501
        maxx, maxy = 0, 0
        #print(line[0])
        for j in line:
            #print(j)
            if j[0] > maxx:
                maxx = j[0]
            elif j[0] < minx:
                minx = j[0]
            if j[1] > maxy:
                maxy = j[1]
            elif j[1] < miny:
                miny = j[1]
        return (minx, miny, maxx - minx, maxy - miny)
    minx, miny, maxx, maxy = crop(POINTS)
    #print(minx, miny, maxx, maxy)
    #print(POINTS[0][0])
    POINTS2=[]
    for P in POINTS:
        #print(P)
        POO2=[(int(P[0] - minx), int(P[1] - miny))]
        POINTS2.append(POO2)
    spread=[[0 for i in range(28)] for j in range(28)]
    #print(POINTS2)
    for i in POINTS2:
        spread[int(28 * (i[0][0] - 1) / maxx)][int(28 * (i[0][1] - 1) / maxy)] += 1
    max=spread[0][0]
    min=spread[0][0]
    for i in spread:
        for j in i:
            if j > max:
                max = j
            elif j < min:
                min = j
    def standarise(n):
        return (n - min) / max

    for i in range(28):
        for j in range(28):
            spread[i][j] = standarise(spread[i][j])
    return spread
def guess(po,name):
    class_name = ["circle", "tri","square",]
    model = tf.models.load_model('shasaver.model')
    po = np.asarray(shape_to_mat(po)).reshape((1, 28, 28))
    #print(po)
    pred = model.predict(po)
    index = np.argmax(pred)
    r = class_name[index]
    print(r)
    client.send((r+ "," + name).encode())
def add_shape(po,shape_name,name):
    po=np.asarray([(i[0],i[1]) for i in po])
    f.add("id",po,shape_name)
    client.send(("added" + "," + name).encode())
def fit():
    class_name = {"circle": 0, "tri": 1, "square":2,}
    tr_mat, tr_lable, ts_mat, ts_lable = [], [], [], []

    def rotate(vector, theta, rotation_around=None) -> np.ndarray:
        vector = np.array(vector)
        if vector.ndim == 1:
            vector = vector[np.newaxis, :]
        if rotation_around is not None:
            vector = vector - rotation_around
        vector = vector.T
        theta = np.radians(theta)
        rotation_matrix = np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]])
        output: np.ndarray = (rotation_matrix @ vector).T
        if rotation_around is not None:
            output = output + rotation_around
        return output.squeeze()

    def shape_muls(POINTS):
        muls = []
        for i in range(31):
            rnd = random.randint(i, i * 12)
            if i == 21:
                rnd = 0
            POINTS2 = []
            for j in POINTS:
                # print(j)
                x, y = rotate((j[0] - 250, j[1] - 250), rnd)
                POINTS2.append(np.array([(int(x + 250), int(y + 250))]))
            muls.append(POINTS2)
        muls2 = []
        for i in muls:
            po = shape_to_mat(i)
            muls2.append(po)
            muls2.append(np.rot90(po, 1))
            muls2.append(np.rot90(po, 2))
            muls2.append(np.rot90(po, 3))
            po = np.flip(po, 0)
            muls2.append(po)
            muls2.append(np.rot90(po, 1))
            muls2.append(np.rot90(po, 2))
            muls2.append(np.rot90(po, 3))
        return muls2

    # class_name=["circle", "tri","square",]
    def shape_to_mat(POINTS):
        def crop(line):
            miny, minx = 501, 501
            maxx, maxy = 0, 0
            # print(line[0])
            for j in line:
                i = j[0]
                if i[0] > maxx:
                    maxx = i[0]
                elif i[0] < minx:
                    minx = i[0]
                if i[1] > maxy:
                    maxy = i[1]
                elif i[1] < miny:
                    miny = i[1]
            return (minx, miny, maxx - minx, maxy - miny)

        minx, miny, maxx, maxy = crop(POINTS)
        # print(minx, miny, maxx, maxy)
        # print(POINTS[0][0])
        POINTS2 = []
        for P in POINTS:
            POO2 = [(int(P[0][0] - minx), int(P[0][1] - miny))]
            POINTS2.append(POO2)
        spread = [[0 for i in range(28)] for j in range(28)]
        # print(POINTS2[0])
        for i in POINTS2[0]:
            spread[int(28 * (i[0] - 1) / maxx)][int(28 * (i[1] - 1) / maxy)] += 1
        max = spread[0][0]
        min = spread[0][0]
        for i in spread:
            for j in i:
                if j > max:
                    max = j
                elif j < min:
                    min = j

        def standarise(n):
            return (n - min) / max

        for i in range(28):
            for j in range(28):
                spread[i][j] = standarise(spread[i][j])
        return spread

    # class_name=["circle","tri"]
    shuffle_g = []
    for i in class_name:
        shps = f.get_wh("id", "arr", "shape='" + i + "'")
        shps=random.sample(shps,50)
        for j in shps:
            # print(j[0][1])
            spraeds = shape_muls(j[0])
            for q in spraeds:
                shuffle_g.append([q, class_name[i]])
    np.random.shuffle(shuffle_g)
    tr_mat = np.asarray([i[0] for i in shuffle_g])
    tr_lable = np.asarray([i[1] for i in shuffle_g])
    #print(tr_lable[:20])
    #print(len(tr_mat), len(tr_lable))
    tr_mat = np.asarray(tr_mat)
    tr_lable = np.asarray(tr_lable)
    # ts_lable = np.where(ts_lable == 'circle', 0, 1).astype(int)

    ts_mat = tr_mat[:2000]
    ts_lable = tr_lable[:2000]
    model = tf.models.load_model('shasaver.model')
    model.fit(tr_mat, tr_lable, epochs=2, validation_split=0.2)
    loss, accuracy = model.evaluate(ts_mat, ts_lable)
    print(loss, accuracy)
    print(f"loss {loss}")
    print(f"accuracy {accuracy}")
    model.save('shasaver.model')
cert_gen(KEY_FILE="resp.key",CERT_FILE="resp.crt")
import ssl
client = socket.socket()
client=ssl.wrap_socket(client,cert_reqs=ssl.CERT_NONE,server_side=False,keyfile="resp.key",certfile="resp.crt")
hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
client.connect((IPAddr, 1729))
client.send("model".encode())

i=0
while True:
    message = client.recv(16384).decode().split("@")
    #print(message)
    messag = json.loads(message[0])
    if messag.get("name")=="ask":
        threading.Thread(target=guess, args=(messag.get("shape"),message[1])).run()
    else:
        threading.Thread(target=add_shape, args=(messag.get("shape"),messag.get("name"),message[1])).run()
        i+=1
    if i==10:
        i=0
        threading.Thread(target=fit,)

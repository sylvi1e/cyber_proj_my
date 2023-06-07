import numpy as np
import random
from tensorflow import keras as tf
from q import shape_saver
f=shape_saver()
#(tr_mat,tr_lable),(ts_mat,ts_lable)=tf.datasets.cifar10.load_data()
class_name={"circle":0,"tri":1,"square":2}
tr_mat,tr_lable,ts_mat,ts_lable=[],[],[],[]

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
    muls=[]
    for i in range(30):
        rnd=random.randint(1,89)
        if i==0:
            rnd=0
        POINTS2=[]
        for j in POINTS:
            #print(j)
            x, y = rotate((j[0] - 250, j[1] - 250), rnd)
            POINTS2.append(np.array([(int(x + 250), int(y + 250))]))
        muls.append(POINTS2)
    muls2=[]
    for i in muls:
        po=shape_to_mat(i)
        muls2.append(po)
        muls2.append(np.rot90(po,1))
        muls2.append(np.rot90(po, 2))
        muls2.append(np.rot90(po, 3))
        po=np.flip(po, 0)
        muls2.append(po)
        muls2.append(np.rot90(po, 1))
        muls2.append(np.rot90(po, 2))
        muls2.append(np.rot90(po, 3))
    return muls2
#class_name=["circle","tri"]
def shape_to_mat(POINTS):
    def crop(line):
        miny, minx = 501, 501
        maxx, maxy = 0, 0
        #print(line[0])
        for j in line:
            i=j[0]
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
    #print(minx, miny, maxx, maxy)
    #print(POINTS[0][0])
    POINTS2=[]
    for P in POINTS:
        POO2=[(int(P[0][0] - minx), int(P[0][1] - miny))]
        POINTS2.append(POO2)
    spread=[[0 for i in range(28)] for j in range(28)]
    #print("po2",POINTS2[0])
    try:
        for i in POINTS2:
            spread[int(28 * (i[0][0] - 1) / maxx)][int(28 * (i[0][1] - 1) / maxy)] =spread[int(28 * (i[0][0] - 1) / maxx)][int(28 * (i[0][1] - 1) / maxy)]+ 1
    except IndexError:
        print(spread)
    #for i in POINTS2[0]:
        #spread[int(28 * (i[0] - 1) / maxx)][int(28 * (i[1] - 1) / maxy)] += 1

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
#class_name=["circle","tri"]
shuffle_g = []
for i in class_name:
    print(i)
    shps=f.get_wh("id","arr","shape='"+i+"'")
    l=0
    for j in shps:
        print(l)
        l+=1
        #print(j[0][1])
        spraeds=shape_muls(j[0])
        for q in spraeds:
            shuffle_g.append([q, class_name[i]])
np.random.shuffle(shuffle_g)
tr_mat = np.asarray([i[0] for i in shuffle_g])
tr_lable = np.asarray([i[1] for i in shuffle_g])

#print(tr_mat[:20])
print(len(tr_mat),len(tr_lable))
tr_mat = np.asarray(tr_mat)
tr_lable = np.asarray(tr_lable)
#ts_lable = np.where(ts_lable == 'circle', 0, 1).astype(int)

ts_mat = tr_mat[:2000]
ts_lable = tr_lable[:2000]
# class_name=["circle", "tri"]

model = tf.models.Sequential([
  tf.layers.Conv2D(28, (3,3), activation="relu", input_shape=(28,28,1)),
  tf.layers.MaxPooling2D((2,2)),
  tf.layers.Conv2D(64, (3,3), activation="relu"),
  tf.layers.MaxPooling2D((2,2)),
  tf.layers.Conv2D(64, (3,3), activation="relu"),
  tf.layers.Flatten(),
  tf.layers.Dense(64, activation="relu"),
  tf.layers.Dense(3, activation="softmax")
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(tr_mat, tr_lable, epochs=10, validation_split=0.2)

loss,accuracy=model.evaluate(ts_mat,ts_lable)

print(f"loss {loss}")
print(f"accuracy {accuracy}")
model.save('shasaver.model')
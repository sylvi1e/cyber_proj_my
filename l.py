from q import shape_saver
from users import  user_saver
import random
f=shape_saver()
f1=user_saver()
l=[0,5,6,2,4,5,6,87,3,5,34,65,346,52]
print(random.sample(l,7))
#f1.drop("id")
#f1.create("id")
#f1.add("id","2","pass")
shapes=("circle", "tri","square")
for i in shapes:
    print(i,len(f.get_wh("id", "*", "shape='"+i+"'")))
#print(f.get_wh("id", "*", "shape='"+"line"+"'"))
#print("tri", len(f.get_wh("id", "*", "shape='tri'")), "circle", len(f.get_wh("id", "*", "shape='circle'")))
#message=["2","pass"]
#f1.update("id","name=2","ask='True'")
#print(message[1]==f1.get_wh("id", "pass", "name = '"+message[0]+"'")[0][0])

print("ALL: " + str(f1.get_all("id")))
print([("2",)],f1.get_wh("id", "name", "name = '"+"2"+"'"),[("2",)]==f1.get_wh("id", "name", "name = '"+"2"+"'"))



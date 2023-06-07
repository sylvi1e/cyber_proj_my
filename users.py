import sqlite3
import numpy as np
import io


class user_saver:
    def __init__(self):
        def adapt_array(arr):
            out = io.BytesIO()
            np.save(out, arr)
            out.seek(0)
            return sqlite3.Binary(out.read())
        def convert_array(text):
            out = io.BytesIO(text)
            out.seek(0)
            return np.load(out)
        sqlite3.register_adapter(np.ndarray, adapt_array)
        sqlite3.register_converter("array", convert_array)
        self.con = sqlite3.connect('users.bd', detect_types=sqlite3.PARSE_DECLTYPES, isolation_level=None)
        self.cur=self.con.cursor()
    def drop(self,name):
        self.cur.execute("drop table "+name)
    def create(self,name):
        self.cur.execute("create table " + name + " (name TEXT PRIMARY KEY, pass text, ask text, tell text)")
    def add(self,name,u_name, password ,ask = "False", tell ="False"):
        self.cur.execute("insert into "+name+ " values (?,?,?,?)", (u_name, password,ask,tell))
    def get(self,name,num):
        self.cur.execute("select name from "+name)
        data = self.cur.fetchall()[num]
        self.cur.execute("select pass from "+name)
        data2 = self.cur.fetchall()[num]
        self.cur.execute("select ask from " + name)
        data3 = self.cur.fetchall()[num]
        self.cur.execute("select tell from " + name)
        return (data,data2,data3, self.cur.fetchall()[num])
    def update(self,name,u_name,c):
        p= "UPDATE "+name+" set "+c+" where "+u_name
        print("UPDATE "+name+" set "+c+" where "+u_name)
        self.con.execute(p)
        self.con.commit()
    def get_all(self,name):
        self.cur.execute("select * from " + name)
        return self.cur.fetchall()
    def get_wh(self,name,c,q):
        self.cur.execute("select "+c+" from " + name+" where "+q)
        return self.cur.fetchall()
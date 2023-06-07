import sqlite3
import numpy as np
import io


class shape_saver:
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
        self.con = sqlite3.connect('shape.bd', detect_types=sqlite3.PARSE_DECLTYPES, isolation_level=None)
        self.cur=self.con.cursor()
    def drop(self,name):
        self.cur.execute("drop table "+name)
    def create(self,name):
        self.cur.execute("create table " + name + " (shape,arr array)")
    def add(self,name,npa,shp):
        self.cur.execute("insert into "+name+ " values (?,?)", (shp, npa))
    def get(self,name,num):
        self.cur.execute("select arr from "+name)
        data = self.cur.fetchall()[num]
        self.cur.execute("select shape from "+name)
        data2 = self.cur.fetchall()[num]
        return (data2,data)
    def get_all(self,name):
        self.cur.execute("select * from " + name)
        return self.cur.fetchall()
    def get_wh(self,name,c,q):
        self.cur.execute("select "+c+" from " + name+" where "+q)
        return self.cur.fetchall()
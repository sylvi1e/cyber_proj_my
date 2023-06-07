class cli:
    def __init__(self,name,clnt, addres):
        self.name = name
        self.clnt =clnt
        self.addres = addres
class group:
    def __init__(self,name,cli_l,admin):
        self.name = name
        self.cli_l = cli_l
        self.admin = admin
        self.mute=[]
    def add(self,u):
        self.cli_l.append(u)
    def mute(self,u):
        self.mute.append(u)

    def clnt(self):
        clnts=[]
        for c in self.cli_l:
            clnts.append(c.clnt)
        return clnts
    def people_l(self):
        n = []
        for c in self.cli_l:
            n .append(c.name)
        return n
    def people(self):
        n = ""
        for c in self.cli_l:
            n+=c.name +", "
        return n
    def part(self,u):
        for c in self.cli_l:
            if c==u:
                return True
        return False
    def kick(self,u):
        self.cli_l.remove(u)
        if u in self.mute:
            self.mute.remove(u)
    def new_admin(self):
        self.kick(self.admin)
        for c in self.cli_l:
            mut=False
            for cli in self.mute:
                if c==cli:
                    mut=True
            if not mut:
                self.admin =c
                return c
        self.admin = self.cli_l[0]
        return self.cli_l[0]
    def mut(self,u):
        if u in self.cli_l and not self.ismut(u):
            self.mute.append(u)
    def unmut(self,u):
        for i in range(len(self.mute)):
            if self.mute[i] == u:
                self.mute.pop(i)

    def ismut(self,u):
        for n in self.mute:
            if n==u:
                return True
        return False
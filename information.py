class Information:
    def __init__(self):
        self.num_query=0
        self.num_lack=0
        self.time=1
        self.algorithm=2
        self.addr_used=0
    def query(self,flag):
        self.num_lack+=0 if flag else 1
        self.num_query+=1
        return (self.num_lack,self.num_query)
    def timecounter(self,time=None):
        self.time=time if time else self.time+1
    def change_alg(self,alg):
        self.algorithm=alg
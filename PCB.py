import numpy as np
import pandas as pd

class PCBs:
    def __init__(self):
        self.pcb=pd.DataFrame(columns=['id','need_time','arr_time','resp_ratio','priority','rest_time'])
        self.now_time=0
    def importdata(self,path):
        self.pcb=pd.read_csv(path)
    def exportdata(self,path):
        self.pcb.to_csv(path,index=False)
    def add(self,id,nt,at,rr,pr):
        if id in self.pcb['id']:
            return False 
        self.pcb.loc[self.pcb.shape]=[id,nt,at,rr,pr,nt]
        return True
    def dele(self):
        self.pcb=self.pcb.drop(0)
        self.pcb.index=[i for i in range(self.pcb.shape[0])]
    def updata(self):
        self.pcb['resp_ratio']=(self.pcb['need_time']+self.now_time-self.pcb['arr_time'])/self.pcb['need_time']
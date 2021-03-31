import numpy as np
import pandas as pd

class PCBs:
    def __init__(self):
        self.pcb=[pd.DataFrame(columns=['id','wait_time','rest_time','response_ratio','priority'],dtype=np.int32),
                pd.DataFrame(columns=['id','wait_time','rest_time','response_ratio','priority'],dtype=np.int32)]
        self.alg=1;
    def timepass(self):
        self.pcb[0]['wait_time']+=1
        try:
            self.pcb[0].loc[0,'rest_time']-=1
            if self.pcb[0].loc[0,'rest_time']==0:
                self.pcb[0]=self.pcb[0].drop(0)
                self.pcb[0].index=[i for i in range(self.pcb[0].shape[0])]
        except :
            pass
        self.pcb[1]['wait_time']-=1
        self.updata()
    def updata(self):
        for j in range(2):
            self.pcb[j].index=[i for i in range(self.pcb[j].shape[0])]
        self.push()
        for i in range(2):
            self.pcb[i]['response_ratio']=(self.pcb[i]['rest_time']+self.pcb[i]['wait_time'])/self.pcb[i]['rest_time']
        self.pcb[0]=self.pcb[0].sort_values(by=self.pcb[0].columns[self.alg],ascending=True if self.alg==2 else False)
        self.pcb[1]=self.pcb[1].sort_values(by='wait_time',ascending=True)
        for j in range(2):
            self.pcb[j].index=[i for i in range(self.pcb[j].shape[0])]

    def push(self):
        try:
            while self.pcb[1].loc[0,'wait_time']==0:
                self.pcb[0].loc[self.pcb[0].shape[0]]=self.pcb[1].loc[0]
                self.pcb[1]=self.pcb[1].drop(0)
                self.pcb[1].index=[i for i in range(self.pcb[1].shape[0])]
        except :
            pass
        try:
            if self.pcb[0].loc[0,'rest_time']==0:
                self.pcb[0].drop(0)
                self.pcb[0].index=[i for i in range(self.pcb[0].shape[0])]
        except :
            pass

    def add(self,id,wt,rt,pr):
        self.pcb[1].loc[self.pcb[1].shape[0]]=[id,wt,rt,0,pr]
        self.updata()
    def impdata(self,fname):
        self.pcb[1].append(pd.read_csv(fname))
    def save_status(self,fname):
        self.pcb[1].to_csv(fname)
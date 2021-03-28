import pandas as pd
import numpy as np
import os
from information import Information
class page:
    def __init__(self,page_num=8,page_size=8,page_num_have=1<<4):
        self.pn=page_num
        self.ps=page_size
        self.ph=page_num_have
        idx=np.arange(1<<self.pn).reshape(1,-1)
        add=np.zeros(1<<self.pn).reshape(1,-1)
        last_use_time=np.zeros(1<<self.pn).reshape(1,-1)
        enter_time=np.zeros(1<<self.pn).reshape(1,-1)
        self.list=pd.DataFrame(np.concatenate((idx,add,enter_time,last_use_time)).T,columns=['page_idx','addr_idx','enter_time','last_use_time'],dtype=np.int32)
    def impdata(self,path):
        self.list=pd.read_csv(path,dtype=np.int32)
    def save_status(self,path):
        self.list.to_csv(path,index=False)
    def get_one_page(self,addr):
        page_idx=addr>>self.ps
        if page_idx<(1<<self.pn):
            return self.list.iloc[page_idx]
        else:
            return None
    def query(self,addr,info):
        flag=False
        alg=info.algorithm
        time=info.time
        num_use=info.addr_used
        page_idx=addr
        if page_idx<(1<<self.pn):
            addr_ph=0
            if self.list.iloc[page_idx,1]:
                self.list.iloc[page_idx,3]=time
                flag=True
            else:
                flag=False
                if num_use==self.ph:
                    list=self.list[self.list['addr_idx']]
                    idx=self.swap(list,alg)
                    idx_min=list.idxmin()
                    addr_ph=list.iloc[idx,'addr_idx']
                    list.iloc[idx,'addr_idx']=0
                else :
                    info.addr_used+=1
                    addr_ph=info.addr_used
                self.list.iloc[page_idx,3]=self.list.iloc[page_idx,2]=time
                self.list.iloc[page_idx,1]=addr_ph
        info.time+=1
        info.query(flag)
        return flag

        def swap(self,,list,alg):
            idx=0
            if alg<=3:
                idx=self.list.astype(float).idxmax()[alg]
            return idx




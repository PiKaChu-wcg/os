import pandas as pd
import numpy as np
import os
from information import Information


class page:
    def __init__(self, page_num=8, page_size=8, page_num_have=2):
        self.pn = page_num
        self.ps = page_size
        self.ph = page_num_have
        idx = np.arange(1 << self.pn).reshape(1, -1)
        add = np.zeros(1 << self.pn).reshape(1, -1)
        last_use_time = np.zeros(1 << self.pn).reshape(1, -1)
        enter_time = np.zeros(1 << self.pn).reshape(1, -1)
        self.list = pd.DataFrame(np.concatenate((idx, add, enter_time, last_use_time)).T,
                                 columns=['page_idx', 'addr_idx', 'enter_time', 'last_use_time'], dtype=np.int32)

    def impdata(self, path):
        self.list = pd.read_csv(path, dtype=np.int32)

    def save_status(self, path):
        self.list.to_csv(path, index=False)

    def get_one_page(self, addr):
        page_idx = addr >> self.ps
        if page_idx < (1 << self.pn):
            return 1
        else:
            return 0

    def query(self, addr, info):
        flag = False
        alg = info.algorithm
        time = info.time
        num_use = info.addr_used
        page_idx = addr
        if page_idx < (1 << self.pn):
            addr_ph = 0
            if self.list.iloc[page_idx, 1]:
                self.list.iloc[page_idx, 3] = time
                flag = True
            else:
                flag = False
                if num_use == self.ph:
                    print(1)
                    list = self.list.loc[self.list['addr_idx'] != 0]
                    idx = self.swap(list, alg)
                    print(list)
                    print(list.loc[list['addr_idx'] == idx]['addr_idx'])
                    addr_ph += list.loc[list['addr_idx'] == idx].iloc[0,1]
                    print('addr{}'.format(addr_ph))
                    self.list.loc[self.list['addr_idx'] == addr_ph, 'addr_idx'] = 0
                    print(1)
                else:
                    info.addr_used += 1
                    addr_ph += info.addr_used
                self.list.iloc[page_idx, 3] = self.list.iloc[page_idx, 2] = time
                self.list.iloc[page_idx, 1] = addr_ph
        info.time += 1
        info.query(flag)

    def swap(self, list, alg):
        idx = 0
        if alg <= 3:
            idx = list.astype(float).idxmin()[alg]
            print(list.astype(float).idxmin(), list.iloc[idx, 1])
        return list.iloc[idx, 1]

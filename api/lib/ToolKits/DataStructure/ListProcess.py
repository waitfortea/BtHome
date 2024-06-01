import pandas as pd
import numpy as np
from dataclasses import dataclass
from ..FileProcess import PathProcessor
from ..CustomException import *
from ..CustomType import Type

def isLenAlign(list1,list2):
    if len(list1) == len(list2):
        return True
    return False

def concatList(list1):
    result=[]
    for list in list1:
        result+=list
    return result
def listMatchByDict(list1,list2):
    if isLenAlign(list1,list2):
        match_Dict = {key: [] for key in set(list1)}
        match_List = list(zip(list1,list2))
        for match in match_List:
            match_Dict[match[0]].append(match[1])
        return match_Dict

class ListProcessor:
    def __init__(self,data):
        self.init(data)
        self.nextIndex=0
    def init(self,data):
        if "__len__" not in dir(data):
            self.list=[data]
            return
        else:
            if Type(data).type==list:
                self.list=data
                return
            elif Type(data).type in (tuple,set):
                self.list = [data for i in data]
                return
        raise InitFailedError

    def isInerTypeAlign(self):
        if all(Type(i).isList for i in self.list):
            return True
        else:
            return False
    def __iter__(self):
        return self

    def __next__(self):
        if self.nextIndex<self.len:
            result=self.list[self.nextIndex]
            self.nextIndex+=1
            return result
        else:
            self.nextIndex=0
            raise StopIteration

    def __getitem__(self, item):
        return self.list[item]

    @property
    def len(self):
        return len(self.list)

    @property
    def shape(self):
        pass

    @property
    def isLenInnerAlign(self):
        if len(set([len(i) for i in self.list]))==1:
            return True
        else:
            return False

    @property
    def innerLen(self):
        if self.isLenInnerAlign:
            return len(self.list[0])
        else:
            raise LenAlignError

    def toStr(self):
        return [str(i) for i in self.list]

    @property
    def strip_List(self):
        return




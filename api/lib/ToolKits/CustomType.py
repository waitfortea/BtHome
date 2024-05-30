from CustomException import *
import pandas as pd
import numpy as np
class Type:
    def __init__(self,obj):
        self.obj=obj

    @property
    def type(self):
        return type(self.obj)

    @property
    def innerType_Set(self):
        if self.isGenerated:
            print(list(set([Type(i).type for i in self.obj])))
            return list(set([Type(i).type for i in self.obj]))
        else:
            raise GeneratedError

    @property
    def isBool(self):
        return self.type==bool

    @property
    def isInt(self):
        return self.type==int

    @property
    def isStr(self):
        return self.type==str

    @property
    def isList(self):
        return self.type==list

    @property
    def isGenerated(self):
        if any(self.type==i for i in [list, set, tuple]):
            return True
        else:
            return False

    @property
    def isInnerTypeAlign(self):
        if self.isGenerated:
            if len(set([type(i) for i in self.obj]))==1:
                return True
            else:
                return False
        else :
            return False

    @property
    def uniqueInnerType(self):
        if self.isGenerated:
            if self.isInnerTypeAlign:
                return set([type(i) for i in self.obj])[0]
        else:
            raise GeneratedError

    @property
    def isDict(self):
        return self.type==dict

    @property
    def isTuple(self):
        return self.type == tuple
    @property
    def isFloat(self):
        return self.type == float

    @property
    def isNumerical(self):
        return self.isInt or self.isFloat

    @property
    def isDataFrame(self):
        return self.type==pd.DataFrame

    @property
    def isSeries(self):
        return self.type==pd.Series

    @property
    def isNumpyArray(self):
        return self.type==np.array
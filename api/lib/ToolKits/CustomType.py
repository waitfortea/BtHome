
from .CustomException import *
from collections import Iterable

class Type:
    def __init__(self,obj):
        self.obj=obj

    @property
    def type(self):
        return type(self.obj)

    def isInnerType(self,data):
        if self.isGenerated:
            if all(type(i)==data for i in self.obj):
                return True
            else:
                return False
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
        if isinstance(self,Iterable):
            return True
        return False

    @property
    def isInnerTypeAlign(self):
        if self.isGenerated:
            if len(set([type(i) for i in self.obj]))==1:
                return True
            else:
                return False
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



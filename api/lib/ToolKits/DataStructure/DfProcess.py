import pandas as pd
import numpy as np
from dataclasses import dataclass
from FileProcess import PathProcessor
from CustomException import *
from CustomType import Type

@dataclass
class DfProcessor:
    def __init__(self,rawData=None,fieldName_List=None):
        if Type(rawData).isDataFrame:
            self.df=rawData
        elif Type(rawData).isList:
            if ListProcessor(rawData).innerLen==len(fieldName_List):
                self.df=self.init(rawData)
                self.rename(fieldName_List)
            else:
                raise LenAlignError

    def init(self,rows_List):
        if ListProcessor(rows_List).isLenInnerAlign:
            data_List = [list(range(len(rows_List))) for row in range(len(rows_List[0]))]
            for i,row in enumerate(rows_List):
                for j,element in enumerate(row):
                    data_List[j][i] = rows_List[i][j]
            data_Dict={index:column for index,column in enumerate(data_List)}
            df=pd.DataFrame(data_Dict)
        else:
            data_Dict={index:column for index,column in enumerate(rows_List)}
            df=pd.DataFrame(data_Dict,fillna=0)
        return df

    def getColumnIndex(self,index):
        if Type(index).isStr:
            return self.df.columns.get_loc(index)
        if Type(index).isInt:
            return self.df.columns[index]

    def getRowIndex(self,index):
        if Type(index).isStr:
            return self.df.index.get_loc(index)
        if Type(index).isInt:
            return self.df.index[index]

    #对象属性
    @property
    def type(self):
        return Type(self.df)

    @property
    def columnNames(self):
        return self.df.columns

    @property
    def len(self):
        return {'rowLen': len(self.df), 'columnLen': len(self.data.columns)}

    #对象操作
    def rename(self,field_List):
        self.df.columns=field_List

    def show(self):
        print(self.df.to_string())

    def __getitem__(self, item):
        return DfProcessor(self.df[item])

    #对象清洗
    #删除缺失值所在行
    @property
    def NAReomveData(self):
        self.df = self.df.dropna().reset_index(drop=True)
        return self

    #对象转格式
    @property
    def toRows_List(self):
        return [row.tolist() for index,row in self.df.iterrows()]

    @property
    def toSql_List(self):
        return self.columnNames,self.toRows_List

    @property
    def toColumns_List(self):
        return [column.tolist() for index,column in self.df.iteritems()]

    @property
    def toNpColumnVector(self):
        return Matrix(np.matrix(self.df).T)

    @property
    def print(self):
        print(self.data)

    @classmethod
    def read(cls,type,filePath):
        type_Dict={
            'csv':pd.read_csv
            ,'json':pd.read_json
            ,'excel':pd.read_excel
        }
        if not PathProcessor(filePath).isFile:
            raise FileNotFound

        elif type in type_Dict.keys():
            return DfProcessor(type_Dict[type](filePath))

    def dropBytarget(self,column_List,target_List):
        for column in column_List:
            for target in target_List:
                if Type(column).isStr:
                    index_List=np.where(self.df[column]==target)[0].tolist()
                    if index_List!=[]:
                        self.df.drop(index_List,inplace=True)
                        self.df.reset_index(drop=True)
                elif Type(column).isInt:
                    index_List=np.where(self.data[column]==target)[0].tolist()
                    if index_List != []:
                        self.df.drop(index_List, inplace=True)
                        self.df.reset_index(drop=True)

    def simpleShow(self):
        print(self.data.head())
        print(self.data.tail())


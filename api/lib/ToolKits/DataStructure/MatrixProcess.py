
@dataclass
class Matrix:
    data:object=None
    columnIndex:list=None
    rowIndex:list=None

    def setIndexSeperately(self,columnIndex_List=None,rowIndex_List=None):
        if columnIndex_List:
            self.columnIndex=columnIndex_List
        if rowIndex_List:
            self.rowIndex=rowIndex_List

    def setIndex(self,index_List):
        self.columnIndex=index_List
        self.rowIndex=index_List

    @property
    def print(self):
        if self.columnIndex is not None and self.rowIndex is not None:
            print(end='\t')
            for columnIndex in self.columnIndex:
                print(columnIndex,end='\t')
            print('\n')
            for i in range(len(self.data)):
                print(f'{self.rowIndex[i]}',end='\t')
                for column in self.data[i]:
                    print(column,end='\t')
                print('\n')
        else:
            print(self.data)

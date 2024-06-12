import math
import pymysql as mysql
from dataclasses import dataclass
from ToolKits.GeneralObject import StrProcessor
from ToolKits.DataStructure import Type,DfSet
import re
class NotFoundTable(Exception):
    def __init__(self):
        self.message='数据表不存在'

class NotFoundDataBase(Exception):
    def __init__(self):
        self.message='数据库不存在'

class SqlClient:
    def __init__(self,host="127.0.0.1",user="root",password="Aprivilege7"):
        self.session = mysql.connect(
            host=host
            ,user=user
            ,password=password
        )

    def getDataBases(self,dataBase):
        if dataBase.lower() in self.dataBases:
            cursor=self.session.cursor()
            cursor.execute(f'use {dataBase}')
            return DataBase(cursor)
        else:
            raise NotFoundDataBase

    def createDataBase(self,dataBaseName):
        try:
            return self.getDataBases(dataBaseName)
        except NotFoundDataBase:
            print(f'create datebase {dataBaseName}')
            self.session.cursor().execute(f'create database {dataBaseName}')
            return self.getDataBases(dataBaseName)

    @property
    def dataBases(self):
        cursor=self.session.cursor()
        cursor.execute('show databases')
        return [dataBase[0] for dataBase in list(cursor.fetchall())]

    def commit(self):
        self.session.commit()

class DataBase:
    def __init__(self,cursor):
        self.cursor=cursor

    def checkTable(self,tableName):
        if tableName.lower() in self.tables:
            return True
        else:
            return False

    @property
    def tables(self):
        self.cursor.execute('show tables')
        return [table[0] for table in list(self.cursor.fetchall())]

    def getTable(self,table):
        if table.lower() in self.tables:
            cursor=self.cursor
            return Table(table,cursor)
        else:
            raise NotFoundTable

    def createTable(self,tableName,field):
        if not self.checkTable(tableName):
            print(field.createProgrammar.format(tableName))
            self.cursor.execute(field.createProgrammar.format(tableName))
            return self.getTable(tableName)
        else:
            print(f'{tableName} exists')
            return self.getTable(tableName)

    def modifyTable(self,tableName,field):
        if not self.checkTable(tableName):
            raise NotFoundTable
        else:
            print(field.modifyFieldProgrammar.format(tableName))
            self.cursor.execute(field.modifyFieldProgrammar.format(tableName))

    def dropTable(self,tableName):
        if not self.checkTable(tableName):
            raise NotFoundTable
        else:
            print(f"drop table if exists {tableName}")
            self.cursor.execute(f'drop table if exists {tableName}')

    def renameTable(self,tableName,newName):
        if self.checkTable(tableName):
            print(f"altet table {tableName} rename to {newName}")
            self.cursor.execute(f"altet table {tableName} rename to {newName}")
        else:
            raise NotFoundTable

    def query(self,queryText):
        print(queryText)
        self.cursor.execute(queryText)
        queryResult=Query(self.cursor)
        queryResult.show()
        return queryResult


class FieldDict:
    def __init__(self,fieldInfo):
        if Type(fieldInfo).isStr:
            self.field_Dict = self.parse(fieldInfo)
        elif Type(fieldInfo).isList:
            self.field_Dict = self.parseTable(fieldInfo)

    @property
    def createProgrammar(self):
        prefix='create table if not exists {} '
        body=f'({",".join([field.createProgrammar for field in self.field_Dict.values()])})'
        createText=prefix+body
        return createText

    @property
    def addFieldProgrammar(self):
        return f'{",".join([field.addFieldProgrammar for field in self.field_Dict.values()])}'

    @property
    def changeFieldProgrammar(self):
        return f'{",".join([field.changeFieldProgrammar for field in self.field_Dict.values()])}'

    @property
    def modifyFieldProgrammar(self):
        prefix = 'alter table {} '
        body = f'{",".join([field.modifyFieldProgrammar for field in self.field_Dict.values()])}'
        createText = prefix + body
        return createText

    @property
    def dropFieldProgrammar(self):
        return  f'{",".join([field.dropFiedlProgrammar for field in self.field_Dict.values()])}'

    def parseTable(self,tableDesc):
        field_Dict = {}
        for index, field in enumerate(tableDesc):
            field_Dict[f'field{index + 1}'] = Field(field)
        return field_Dict

    def parse(self,fieldText):
        field_Dict = {}
        fieldText_List = fieldText.split('\n')
        for index, field in enumerate(fieldText_List):
            field_Dict[f'field{index + 1}'] = Field(field.strip())
        return field_Dict


class Field:
    def __init__(self,fieldInfo):
        if Type(fieldInfo).isStr:
            self.field=self.parse(fieldInfo)
        elif Type(fieldInfo).isList:
            self.field=self.parseTable(fieldInfo)

    @property
    def createProgrammar(self):
        createTabelText = ''
        createTabelText += f'`{self.name}` {self.type} {self.constrain}'
        return createTabelText

    @property
    def addFieldProgrammar(self):
        return f'add `{self.name}` {self.type} {self.constrain}'

    @property
    def changeFieldProgrammar(self):
        return 'change {} '+f'`{self.name}` {self.type} {self.constrain}'

    @property
    def modifyFieldProgrammar(self):
        return f'modify `{self.name}` {self.type} {self.constrain}'

    @property
    def dropFiedlProgrammar(self):
        return f'drop `{self.name}`'

    @property
    def name(self):
        return self.field['name']

    @property
    def type(self):
        return self.field['type']


    @property
    def constrain(self):
        constrainText = ""
        for key, value in self.field.items():
            if Type(value).isBool and value:
                constrainText += key+' '

        return constrainText.strip()

    @classmethod
    def parseTable(cls,tableDesc):
        field = {
            'name': None
            , 'type': None
            , 'not null': None
            , 'unique': None
            , 'comment': None
            , 'auto_increment': None
            , 'primary key': None
        }
        field['name'] = tableDesc[0]
        field['type'] = tableDesc[1]
        if tableDesc[2]=='NO':
            field['not null']=True
        if tableDesc[3]=='PRI':
            field['primary key']=True
        if 'auto_increment' in tableDesc:
            field['auto_increment']=True
        return field

    def parse(self, fieldText):
        field = {
            'name': None
            , 'type': None
            , 'not null': None
            , 'unique': None
            , 'comment': None
            , 'auto_increment': None
            ,'primary key':None
        }
        field['name'] = fieldText.split(" ")[0]
        field['type'] = fieldText.split(" ")[1]
        constrain_List = ['not null', 'unique', 'auto_increment', 'comment','primary key']
        constrainValue_List = [True if constrain in fieldText else False for constrain in constrain_List]
        for constrain in zip(constrain_List, constrainValue_List):
            field[constrain[0]] = constrain[1]
        return field


class Table:
    def __init__(self,tableName,cursor=None):
        self.name=tableName
        self.cursor=cursor

    @property
    def info(self):
        self.cursor.execute(f'desc {self.name}')
        return Query(self.cursor)

    @property
    def fieldDict(self):
        self.cursor.execute(f'desc {self.name}')
        filedInfo=[list(tuple) for tuple in list(self.cursor.fetchall())]
        return FieldDict(filedInfo)

    @property
    def field_List(self):
        return [field.name for field in self.fieldDict.field_Dict.values()]

    @property
    def index(self):
        self.cursor.execute(f'show index from {self.name}')
        return Index(Query(self.cursor).data)

    def insert(self,row):
        insertText=f'insert into {self.name} {row.insertProgrammar}'
        print(insertText)
        self.cursor.execute(insertText)

    def replace(self,row):
        replaceText = f'replace into {self.name} {row.replaceProgrammar}'
        print(replaceText)
        self.cursor.execute(replaceText)

    def addField(self,field):
        addText=f'alter table {self.name} {field.addFieldProgrammar}'
        print(addText)
        self.cursor.execute(addText)

    def chagneField(self,field,field_List):
        changeText=f'alter table {self.name} {field.changeFieldProgrammar}'
        changeText=changeText.format(*field_List)
        print(changeText)
        self.cursor.execute(changeText)

    def dropField(self,field):
        dropText=f'alter table {self.name} {field.dropFieldProgrammar}'
        print(dropText)
        self.cursor.execute(dropText)

    def modifyField(self,field):
        modifyText=f'alter table {self.name} {field.modifyFieldProgrammar}'
        print(modifyText)
        self.cursor.execute(modifyText)

    def dropPrimaryKey(self):
        print(f'alter table {self.name} drop primary key')
        self.cursor.execute(f'alter table {self.name} drop primary key')

    def query(self,queryText):
        print(queryText)
        self.cursor.execute(queryText)
        queryResult=Query(self.cursor)
        queryResult.show()
        return queryResult

def sqlTreatMapStrategy(value):
    if value is None:
        return str(0)
    elif value in ['-','#DIV/0!']:
        return 'NULL'
    elif Type(value).isStr:
        if '%' in value:
            try:
                return str(float(value.strip('%'))/100)
            except:
                print(value)
                raise Exception
        return StrProcessor(re.sub(r'[\'\‘\’]','\"',value)).quotation
    elif Type(value).isNumerical:
        return str(value)
    elif math.isnan(value):
        return str(0)


class Row:
    def __init__(self,field_List,row_List):
        self.field_List=field_List
        self.row_List=row_List
    def fieldNameTreatStrategy(self,fieldName):
        return fieldName.replace(" ","_")

    @property
    def insertProgrammar(self):
        fieldText=f'({",".join([f"`{self.fieldNameTreatStrategy(field)}`" for field in self.field_List])})'
        value_List=[f'({",".join(list(map(sqlTreatMapStrategy,row)))})' for row in self.row_List if row is not None]
        valueText=f'values{",".join(value_List)}'
        insertText=fieldText+' '+valueText
        return insertText

    @property
    def replaceProgrammar(self):
        fieldText = f'({",".join([f"`{self.fieldNameTreatStrategy(field)}`" for field in self.field_List])})'
        value_List = [f'({",".join(list(map(sqlTreatMapStrategy, row)))})' for row in self.row_List if row is not None]
        valueText = f'values{",".join(value_List)}'
        replaceText = fieldText + ' ' + valueText
        return replaceText

    def dropProgrammar(self):
        pass

class Query:
    def __init__(self,cursor):
        self.queryData= self.parse(cursor)

    def parse(self,cursor):
        fieldName_List=[field[0] for field in cursor.description]
        row_List=[list(row) for row in cursor.fetchall()]
        print(fieldName_List)
        print(row_List)
        data=DfSet(row_List,fieldName_List)
        return data

    def show(self):
        self.queryData.show()


class Index:
    def __init__(self,indexDataFrame):
        self.data=indexDataFrame


if __name__=='__main__':
    sqlClient=SqlClient(host='127.0.0.1',user='root',password='Aprivilege7')
    print(sqlClient.dataBases)
    dyDataBase=sqlClient.getDataBases('dydatabase')
















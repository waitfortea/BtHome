import os
import re
import shutil
from dataclasses import dataclass
from .GeneralObject.StrProcess import StrProcessor
from .CustomException import *
@dataclass()
class FileProcessor:
    def __init__(self,filePath,valid=False):
        if not valid:
            if os.path.isfile(filePath):
                self.filePath=filePath
            else:
                raise FileNotFound
        else:
            self.filePath=filePath

    @property
    def absolutePath(self):
        if os.path.isfile(self.filePath):

            return os.path.abspath(self.filePath)
        else:
            raise FileNotFound

    @property
    def baseName(self):
        return ('').join(self.fileName.split('.')[0:-1])

    @property
    def fileName(self):
        return os.path.split(self.absolutePath)[-1]

    @property
    def suffix(self):
        return os.path.splitext(self.absolutePath)[-1]

    @property
    def parDir(self):
        return os.path.dirname(self.absolutePath)

    @property
    def validFilename(self):
        return StrProcessor(self.fileName).clearByList([':','\\','/','*','?','<','>','|'])

    def delete(self):
        os.remove(self.absolutePath)

    def copy(self,dir):
        shutil.copy(self.absolutePath,dir.absoluPath)

    def cut(self,dir):
        shutil.move(self.absolutePath,dir.absoluPath)

class DirProcessor:
    def __init__(self,dirPath,valid=False):
        if not valid:
                if os.path.isdir(dirPath):
                    self.dirPath=dirPath
                else:
                    raise DirNotFound
        else:
            self.dirPath=dirPath

    @property
    def absolutePath(self):
        if os.path.isdir(self.dirPath):
            return os.path.abspath(self.dirPath)
        else:
            raise DirNotFound

    @property
    def parDir(self):
        return os.path.dirname(self.absolutePath)

    @property
    def dirName(self):
        return os.path.basename(self.absolutePath)

    @property
    def directFiles(self):
        file_List = [PathProcessor.init(rf'{self.absolutePath}/{path}') for path in os.listdir(self.absolutePath) if
                     os.path.isfile(rf'{self.absolutePath}/{path}')]
        return file_List

    @property
    def directDirs(self):
        dir_List = [PathProcessor.init(rf'{self.absolutePath}/{path}') for path in os.listdir(self.absolutePath) if
                    os.path.isdir(rf'{self.absolutePath}/{path}')]
        return dir_List

    @property
    def allFiles(self):
        file_List=self.directFiles
        if self.directDirs==[]:
            return file_List
        for dir in self.directDirs:
            file_List+=dir.allFiles
        return file_List

    @property
    def allDirs(self):
        dir_List=self.directDirs
        if self.directDirs==[]:
            return dir_List
        for dir in self.directDirs:
            dir_List+=dir.allDirs
        return dir_List

    def getFileListBySuffix(self, suffix_List):
        return [file for file in self.directFiles if file.suffix in suffix_List]

    def delete(self):
        os.remove(self.absolutePath)

    def copy(self, dir):
        shutil.copy(self.absolutePath, dir.absoluPath)

    def cut(self, dir):
        shutil.move(self.absolutePath, dir.absoluPath)

class PathProcessor:
    @classmethod
    def init(cls,path,make=False):
        # 这里会判断文件和目录是否存在
        if os.path.isdir(path):
            return DirProcessor(path)
        elif os.path.isfile(path):
            return FileProcessor(path)
        else:
            if make:
                if '.' in os.path.basename(path):
                    with open(path,'w',encoding='utf-8') as f:
                        f.write("")
                    return PathProcessor.init(path)
                else:
                    os.makedirs(path,exist_ok=True)
                    return PathProcessor.init(path)
            else:
                raise PathNotFound

    @classmethod
    def makeDir(cls,path):
        if cls.isDir:
            return DirProcessor(path)
        else:
            os.makedirs(path)
            return DirProcessor(path)

    @classmethod
    def isDir(cls,path):
        return os.path.isdir(path)

    @classmethod
    def isFile(cls, path):
        return os.path.isfile(path)

    # os.path.isdir不仅会判断格式，同时也会判断目录是否存在
    @classmethod
    def validFilename(cls,fileName):
        return StrProcessor(fileName).clearByList([':', '\\', '/', '*', '?', '<', '>', '|'])
@dataclass
class UrlProcessor:
    url: str

    @property
    def protocal(self):
        return re.search('.+:',self.url).group()[:-1]

    @property
    def domain(self):
        return re.search('.+\..+?\/',self.url).group()[:-1]

    @property
    def path(self):
        return self.url.replace(self.domain,"")

    @property
    def params(self):
        pass

    def setDomain(self,domain):
        self.url.replace(self.domain,domain)

    def setPath(self,path):
        self.url.replace(self.path,path)


__all__='FileProcessor','DirProcessor','pathInit','_makePath','isFile','isDir'

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
        return DirProcessor(os.path.dirname(self.absolutePath))

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
        file_List = [pathInit(rf'{self.absolutePath}/{path}',flag="file") for path in os.listdir(self.absolutePath) if
                     isFile(rf'{self.absolutePath}/{path}')]
        return file_List

    @property
    def directDirs(self):
        dir_List = [pathInit(rf'{self.absolutePath}/{path}',flag="dir") for path in os.listdir(self.absolutePath) if
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

def isDir(path):
    return os.path.isdir(path)

def isFile(path):
    return os.path.isfile(path)

def _makePath(path,flag=None):
    """
    创建路径，返回自定义的文件对象
    :param path:
    :return:
    """
    if '.' in os.path.basename(path) and (flag=="file" or flag is None):
        with open(path, 'w', encoding='utf-8') as f:
            f.write("")
        return FileProcessor(path)
    elif flag=="dir" or flag is None :
        os.makedirs(path, exist_ok=True)
        return DirProcessor(path)
    raise TypeError

def pathInit(path,make=False,flag=None):
    # 这里会判断文件和目录是否存在
    if os.path.isdir(path) and (flag=="dir" or flag is None):
        return DirProcessor(path)
    elif os.path.isfile(path) and (flag=="file" or flag is None):
        return FileProcessor(path)
    else:
        if make:
            pathObj=_makePath(path,flag)
            return pathObj
    raise PathNotFound


def validFilename(fileName):
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


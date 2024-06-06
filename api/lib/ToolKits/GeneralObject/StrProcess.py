from dataclasses import dataclass
import re
from ..CustomType import *

def PercentageToDecimal(data):
    return float(data.split("%")[0]) / 100


@dataclass
class StrProcessor:
    def __init__(self,text):
        self.init(text)

    def init(self,text):
        if Type(text).isStr:
            self.text=text
            return

        raise InitFailedError(text)

    def contains(self,word_List,mode="all"):
        if mode == 'all':
            return all(word in self.text for word in word_List)
        if mode== "any":
            return any(word in self.text for word in word_List)
        if mode== 'exclude':
            return all(word not in self.text for word in word_List)
    @property
    def toStrip(self):

        def getPreIndex(index):
            if self.text[index] not in ['\t','\n',' ']:
                return index
            index+=1
            return getPreIndex(index)
        def getSuffixIndex(index):
            if self.text[index] not in ['\t','\n',' ']:
                return index
            index-=1
            return getSuffixIndex(index)
        preIndex=getPreIndex(0)
        suffixIndex=getSuffixIndex(len(self.text)-1)
        return self.text[preIndex:suffixIndex+1]


    # 这里j对应非检验字符的索引，但是切片对数字来说不包含结尾，所以要+1

    def clear(self,word_List):
        result=""
        for char in self. text:
            if char in word_List:
                result +=" "
                continue
            result += char
        return result

    @property
    def toStr(self):
        return str(self.text)

    @property
    def quotation(self):
        return f"'{self.text}'"

    @property
    def sqlQuotation(self):
        return f"`{self.text}`"

    @property
    def isalpha(self):
        is_alpha=True
        for char in self.text:
            if self.text.encode('utf-8').isalpha():
                is_alpha*=True
            else:
                is_alpha*=False
        return is_alpha

    @property
    def isChinese(self):
        is_Chinese=True
        for char in self.text:
            if not '\u4e00' <= char <= '\u9fff':
                is_Chinese*=False
            else:
                is_Chinese*=True
        return is_Chinese

    @property
    def raw_length(self):
        length=0
        for char in self.text:
            length+=wcwidth.wcwidth(char)
        return length

    def ljust(self,raw_length,filling_str=" "):
        #单个填充字符串长度
        filling_str_length=StrProcessor(filling_str).raw_length
        #字符串长度
        text_raw_length=StrProcessor(self.text).raw_length
        #设置长度=字符串长度+单个填充字符串长度*填充次数[+/-矫正长度]
        filling_length=raw_length-text_raw_length
        repeat_num=int(filling_length/filling_str_length)
        pair_length=raw_length-repeat_num*filling_str_length-text_raw_length
        ljust_str=self.text
        if pair_length==0:
            for i in range(repeat_num):
                ljust_str+=filling_str
            return ljust_str
        elif pair_length>0:
            for i in range(repeat_num):
                ljust_str+=filling_str
            for j in range(pair_length):
                ljust_str+=" "
            return ljust_str
        else:
            print("请增加设置长度")
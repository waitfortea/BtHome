from dataclasses import dataclass
import re

@dataclass
class StrProcessor:
    text: str

    @property
    def toDict(self):
        try:
            return {i.split(':')[0].strip():i.split(':')[-1].strip() for i in self.text.split('\n')}
        except:
            print('格式不符')

    @property
    def toStrip(self):
        return self.toStripByList(['\n',' ','\t'])

    def replaceByList(self,filter_List):
        return

    @property
    def PercentageToDecimal(self):
        return float(self.text.split("%")[0])/100

    def toStripByList(self,filter_List):
        order=None
        orderReverse=None
        for i in sorted(range(0, len(self.text)), reverse=True):
            if self.text[i] in filter_List:
                continue
            else:
                orderReverse=i
                break
        for i in range(0, len(self.text)):
            if self.text[i] in filter_List:
                continue
            else:
                order=i
                break
        result=self.text[order:orderReverse+1]
        return result
    # 这里j对应非检验字符的索引，但是切片对数字来说不包含结尾，所以要+1


    @property
    def toStr(self):
        return str(self.text)

    def clearByList(self,clear_List):
        for separator in clear_List:
            self.text=self.text.replace(separator,"")
        return self.text

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
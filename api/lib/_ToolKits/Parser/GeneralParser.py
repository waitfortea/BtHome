import re


def pageParser(data):
    start,end=data.split("-")
    page_List=list(range(int(start),int(end)+1))

    return page_List
    # 校验格式
    #采取策略

if __name__=="__main__":
    print(pageParser("1-2"))
    print(re.search("\d+-\d+", '1-20').group())
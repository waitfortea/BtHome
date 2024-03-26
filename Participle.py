import re

import jieba
from ToolKits.Sql import sqlClient
from collections import Counter

def CountFrequecy(word_List):
    wordFrequency_Dict=dict(Counter(word_List))
    with open('customDict.txt','w',encoding='utf-8') as f:
        for key,value in wordFrequency_Dict.items():
            f.write(f'{key}\n')

def writeCountDict():
    sql=sqlClient()
    queryText="""
use db_test
select title from torrentpage
"""
    result_List=sql.query(queryText)
    print(type(result_List))
    print(dir(result_List))
    title_List=[]
    for result in result_List:
        title_List.append(result[0])

    print(title_List)
    word_List=[]
    for title in title_List:
        try:
            word_List.append(list(re.findall('(?<=\[).*?(?=\])',title))[1])
            word_List.append(list(re.findall('(?<=\[).*?(?=\])',title))[2])
        except:
            continue

    CountFrequecy(word_List)


def cut():
    sql=sqlClient()

    queryText="""
use db_test
select title from torrentpage
"""
    result_List=sql.query(queryText)
    print(type(result_List))
    print(dir(result_List))

    title_List=[]
    for result in result_List:
        title_List.append(result[0])
        print(result[0])
    # for title in title_List:
    #     print("|".join(jieba.cut(title,cut_all=True)))
# writeCountDict()
if __name__=='__main__':
    # writeCountDict()
    jieba.load_userdict(r'H:\app\bt-video\BtHome_Core\customDict.txt')
    cut()
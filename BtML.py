import jieba
import Crawler as CL
import Listen
from ToolKits.GeneralStrategy import AsyncStrategy
from ToolKits.Filter import FilterPather,DataFrameFilter,StrFilterStrategyByAllInclude
import numpy as np
import pandas as pd
def jieba_List(text):
    list1=[word for word in list(jieba.cut(text))]
    return list1

def getCosineSimilarity(targetText,TestText):
    encode_List=jieba_List(TestText)
    compare_List=[1 for word in jieba_List(TestText) if word]

    for index,word in enumerate(jieba_List(TestText)):
        for code in jieba_List(targetText):
            if code in word:
                encode_List[index]=1
    encode_List=[0 if code!=1 else 1 for code in encode_List ]
    if len(encode_List)<8:
        compare_List=[1 for i in range(8)]
        x_List=[0 for i in range(8)]
        x_List[:len(encode_List)]=encode_List
        encode_List=x_List

    dot_product = np.dot(encode_List, compare_List)
    norm1 = np.linalg.norm(encode_List)
    norm2 = np.linalg.norm(compare_List)
    if norm1 and norm2:
        cosine_similarity = dot_product / (norm1 * norm2)
        cosine_distance = 1 - cosine_similarity
    else:
        cosine_distance=1
    return cosine_distance

def getMaxSimilarityText(compareText,comic_List):
    result_Dict=dict()
    for comic in comic_List:
        try:
            result_Dict[comic]=getCosineSimilarity(compareText,comic)
        except:
            continue
    return [(result_Dict[code],code) for code in sorted(result_Dict,key=result_Dict.get)]

if __name__=='__main__':
    Listen.setDomainListener()
    DF = AsyncStrategy().execute(CL.seasonalComicCrawl().asyncCrawler())
    seasonalComic_List=[]
    for i in range(5):
        seasonalComic_List.extend(DF.iloc[i, 1].values.flatten().tolist())
    seasonalComic_List = [comic for comic in seasonalComic_List if not pd.isna(comic)]
    print(seasonalComic_List)
    print(getMaxSimilarityText('我的幸福婚约', seasonalComic_List))
    # print(jieba_List('异世界归来的舅舅'))
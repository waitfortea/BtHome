import time
from abc import ABC, abstractmethod
import aiohttp
import requests
import re
import pandas as pd
import asyncio
from urllib.parse import quote, unquote

from api.lib.ToolKits.ElementProcess import *
from api.lib.ToolKits.Event import *
from api.lib.ToolKits.RequestsProcess import *
from api.lib.ToolKits.GeneralObject.StrProcess import *

import api.lib.BtHomeObject as BTO
from api.DomainCheck import *


def indexCrawl(keyword):
    while True:
       try:
            url = domain + "/" + f"search-index-keyword-{quote(keyword)}.htm"
            htmlText = RequestsProcessor(url,proxies=proxy_request).text()
            break
       except Exception as e:
            print(e)
            callEvent("domainCheck",data="")
            continue
    doc=ElementProcessor(htmlText)
    element_List =doc.xpath('//td[@class="subject"]//a[contains(text(),"BT")]')
    print(element_List)
    if element_List is None:
        print('搜索结果为空')
        return pd.DataFrame()

    torrentPage_List = [BTO.TorrentPage(
        url=domain + "/" + element.attrib('href')
        , title=element.text()) for element in element_List]

    torrentPageDf_List = [pd.DataFrame(torrentPage.torrentPage_Np) for torrentPage in torrentPage_List]
    torrentPageDf_raw = pd.concat(torrentPageDf_List, axis=1).transpose()
    torrentPage_DF = torrentPageDf_raw.reset_index(drop=True).rename(columns={0: 'title', 1: 'url'})
    torrentPage_DF['dom'] = torrentPage_List
    print(torrentPage_DF)
    return torrentPage_DF

def  seasonalComicCrawl():
    seasonalComic_DF = pd.DataFrame(columns=['season', 'seasonComic_DF'])
    JapanComicDom = ElementProcessor(RequestsProcessor(domain).text()).xpath('//a[contains(@class,"subject_link") and contains(text()(),"动漫")]')
    print(JapanComicDom.text())
    JapanComicUrl = JapanComicDom.attrib('href')
    print('日本动漫网址:' + domain + '/' + JapanComicUrl)
    seasonnalComicDom =ElementProcessor(RequestsProcessor(domain + '/' + JapanComicUrl).text()).xpath("//strong[contains(text(),'番组放映表')]/../..")
    singalSeasonalDom_List = seasonnalComicDom.xpath(".//a")
    for singalSeasonalDom in singalSeasonalDom_List:
        singalSeasonalComicDF_Dict = dict()
        singalSeasonalUrl = re.sub('http.*.com', domain, singalSeasonalDom.attrib('href'))
        print(singalSeasonalDom.text() + ':' + singalSeasonalUrl)
        singalSeasonalText = RequestsProcessor(singalSeasonalUrl).text()
        seasonalTitleDom =ElementProcessor(singalSeasonalText).xpath('//h2[1]')
        seansonalWeekDayDom_List = ElementProcessor(singalSeasonalText).xpath('//p[strong]')

        for weekdayDom in seansonalWeekDayDom_List:
            # print(weekdayDom.text())
            comicDom_List = ElementProcessor(singalSeasonalText).xpath('./following-sibling::*[1]//td[text() or .//text()]')
            comicName_List = [comic.text() for comic in comicDom_List]
            singalSeasonalComicDF_Dict[weekdayDom.text()] = comicName_List

        singalSeasonalComic_DF = pd.DataFrame(
            {key: pd.Series(value) for key, value in singalSeasonalComicDF_Dict.items()})
        # print(singalSeasonalComic_DF)
        seasonalComic_DF = seasonalComic_DF.append(
            {'season': StrProcessor(seasonalTitleDom[0].text()).toStrip, 'seasonComic_DF': singalSeasonalComic_DF},
            ignore_index=True)
    return seasonalComic_DF

async def asyncCrawler():
    seasonalComic_DF = pd.DataFrame(columns=['season', 'seasonComic_DF'])
    while True:
        try:
            htmlText = RequestsProcessor(domain, proxies=proxy_request).text()
            JapanComicDom = ElementProcessor(htmlText).xpath('//a[contains(@class,"subject_link") and contains(text(),"动漫")]')[0]
            print(JapanComicDom.text())
            break
        except Exception as e:
            print(e)
            await domainCheck()

    JapanComicUrl = JapanComicDom.attrib('href')
    print('日本动漫网址:' + domain + '/' + JapanComicUrl)
    while True:
        try:
            seasonnalComicDom = ElementProcessor(
                RequestsProcessor(domain + '/' + JapanComicUrl,proxies=proxy_request).text()).xpath("//strong[contains(text(),'番组放映表')]/../..")[0]
            break
        except Exception as e:
            print(e)
            await domainCheck()
    singalSeasonalDom_List = seasonnalComicDom.xpath(".//a")

    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(asyncSingalCrawlerTask(singalSeasonalDom,session)) for singalSeasonalDom in
                 singalSeasonalDom_List]
        result_List = await asyncio.gather(*tasks)


    for result in result_List:
        # seasonalComic_DF = seasonalComic_DF.append({'season': result[0], 'seasonComic_DF': result[1]},ignore_index=True)
        temp_DF = pd.DataFrame([{'season': result[0], 'seasonComic_DF': result[1]}])
        seasonalComic_DF = pd.concat([seasonalComic_DF, temp_DF])
    return seasonalComic_DF

async def asyncSingalCrawlerTask(singalSeasonalDom,session):
    singalSeasonalComicDF_Dict = dict()
    count=0
    while count<10:
        try:
            singalSeasonalUrl = re.sub('http.*.com', domain, singalSeasonalDom.attrib('href'))
            print(singalSeasonalDom.text() + ':' + singalSeasonalUrl)
            singalSeasonalText = await AsyncRequestsProcessor(singalSeasonalUrl,session=session,proxy=proxy_aiohttp).text()
            break
        except Exception as e:
            print(e)
            count+=1
            if count < 5:
                print(f'重新连接{count}')
                continue
            await domainCheck()

    seasonalTitleDom = ElementProcessor(singalSeasonalText).xpath('//h2[1]')
    seansonalWeekDayDom_List = ElementProcessor(singalSeasonalText).xpath('//p[strong]')

    for weekdayDom in seansonalWeekDayDom_List:
        comicDom_List = weekdayDom.xpath('./following-sibling::*[1]//td[text() or .//text()]')
        comicName_List = [comic.text() for comic in comicDom_List]
        singalSeasonalComicDF_Dict[weekdayDom.text()] = comicName_List

    singalSeasonalComic_DF = pd.DataFrame(
        {key: pd.Series(value, dtype='str') for key, value in singalSeasonalComicDF_Dict.items()})

    return StrProcessor(seasonalTitleDom[0].text()).toStrip, singalSeasonalComic_DF


if __name__ == '__main__':
    # keyword='欢笑老弄堂'
    # torrentPage_DF = indexCrawl(keyword)
    asyncStrategy(asyncCrawler())
    asyncStrategy(closeSession(aiohttpSession))


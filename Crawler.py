from abc import ABC, abstractmethod

import aiohttp
import requests
import re
import ToolKits.Parser as P
from urllib.parse import quote, unquote
import ToolKits.RequestsProcess as RP
import BtHomeObject as BTO
import pandas as pd
from Event import postEvent
import Listen
from ToolKits.GeneralObject import StrProcessor
import asyncio
from ToolKits.GeneralStrategy import AsyncStrategy
import DomainCheck
from DomainCheck import proxy_aiohttp,proxy_request


class Crawler(ABC):
    def __init__(self, pather: dict = None):
        self.pather = pather

    @abstractmethod
    def crawler(self):
        pass


class AsyncCrawler(Crawler):
    def crawler(self):
        pass

    @abstractmethod
    def asyncCrawler(self):
        pass

    @abstractmethod
    def asyncSingalCrawlerTask(self):
        pass


class IndexCrawler(Crawler):
    def crawler(self):
        domain = postEvent('getDomain')
        while True:
           try:
                url = domain + "/" + f"search-index-keyword-{quote(self.pather['keyWords'])}.htm"
                htmlText = RP.RequestsProcessor(url,proxies=proxy_request).text()
                break
           except:
               domain=AsyncStrategy().execute(DomainCheck.domain_check())
               continue
        text_Pather = P.TextPather(htmlText=htmlText, xpath='//td[@class="subject"]//a[contains(text(),"BT")]')
        elements_List = P.DomParser(text_Pather).parse(P.ListElementStrategyByText())

        if elements_List:
            torrentPage_List = [BTO.TorrentPage(
                url=domain + "/" + element.attrib('href')
                , title=element.text) for element in elements_List]
            torrentPageDf_List = [pd.DataFrame(torrentPage.torrentPage_Np) for torrentPage in torrentPage_List]
            torrentPageDf_raw = pd.concat(torrentPageDf_List, axis=1).transpose()
            torrentPage_DF = torrentPageDf_raw.reset_index(drop=True).rename(columns={0: 'title', 1: 'url'})
            torrentPage_DF['dom'] = torrentPage_List
            return torrentPage_DF
        else:
            print('搜索结果为空')
            return pd.DataFrame()


class seasonalComicCrawl(AsyncCrawler):
    def crawler(self):

        seasonalComic_DF = pd.DataFrame(columns=['season', 'seasonComic_DF'])

        domain = postEvent('getDomain')
        indexText_Pather = P.TextPather(htmlText=RP.RequestsProcessor(domain).text,
                                        xpath='//a[contains(@class,"subject_link") and contains(text(),"动漫")]')

        JapanComicDom = P.DomParser(indexText_Pather).parse(P.ListElementStrategyByText())[0]
        print(JapanComicDom.text)
        JapanComicUrl = JapanComicDom.attrib('href')
        print('日本动漫网址:' + domain + '/' + JapanComicUrl)
        seasonnalComicText_Patther = P.TextPather(htmlText=RP.RequestsProcessor(domain + '/' + JapanComicUrl).text,
                                                  xpath= \
                                                      "//strong[contains(text(),'番组放映表')]/../..")
        seasonnalComicDom = P.DomParser(seasonnalComicText_Patther).parse(P.ListElementStrategyByText())[0]
        singalSeasonalDom_List = seasonnalComicDom.xpath(".//a")
        for singalSeasonalDom in singalSeasonalDom_List:
            singalSeasonalComicDF_Dict = dict()
            singalSeasonalUrl = re.sub('http.*.com', domain, singalSeasonalDom.attrib('href'))
            print(singalSeasonalDom.text + ':' + singalSeasonalUrl)

            singalSeasonalText = RP.RequestsProcessor(singalSeasonalUrl).text

            seasonalTitle_Pather = P.TextPather(htmlText=singalSeasonalText, xpath='//h2[1]')
            seasonalTitleDom = P.DomParser(seasonalTitle_Pather).parse(P.ListElementStrategyByText())
            # print(seasonalTitleDom[0].text)

            seansonalWeekDay_Pather = P.TextPather(htmlText=singalSeasonalText, xpath='//p[strong]')
            seansonalWeekDayDom_List = (P.DomParser(seansonalWeekDay_Pather).parse(P.ListElementStrategyByText()))

            for weekdayDom in seansonalWeekDayDom_List:
                # print(weekdayDom.text)
                comic_Pather = P.DomPather(dom=weekdayDom, xpath='./following-sibling::*[1]//td[text() or .//text()]')
                comicDom_List = P.DomParser(comic_Pather).parse(P.ListElementStrategyByDom())
                comicName_List = [comic.text for comic in comicDom_List]
                singalSeasonalComicDF_Dict[weekdayDom.text] = comicName_List

            singalSeasonalComic_DF = pd.DataFrame(
                {key: pd.Series(value) for key, value in singalSeasonalComicDF_Dict.items()})
            # print(singalSeasonalComic_DF)
            seasonalComic_DF = seasonalComic_DF.append(
                {'season': StrProcessor(seasonalTitleDom[0].text).toStrip, 'seasonComic_DF': singalSeasonalComic_DF},
                ignore_index=True)
        return seasonalComic_DF

    async def asyncCrawler(self):
        seasonalComic_DF = pd.DataFrame(columns=['season', 'seasonComic_DF'])
        domain = postEvent('getDomain')
        print(domain)

        while True:
            try:
                htmlText = RP.RequestsProcessor(domain, proxies=proxy_request).text()
                indexText_Pather = P.TextPather(htmlText=htmlText,
                                                xpath='//a[contains(@class,"subject_link") and contains(text(),"动漫")]')
                JapanComicDom = P.DomParser(indexText_Pather).parse(P.ListElementStrategyByText())[0]
                print(JapanComicDom.text)
                break
            except Exception as e:
                print(e)
                domain = await DomainCheck.domain_check()
                continue
        JapanComicUrl = JapanComicDom.attrib('href')
        print('日本动漫网址:' + domain + '/' + JapanComicUrl)
        while True:
            try:
                seasonnalComicText_Pather = P.TextPather(
                    htmlText=RP.RequestsProcessor(domain + '/' + JapanComicUrl,proxies=proxy_request).text(),
                    xpath= \
                        "//strong[contains(text(),'番组放映表')]/../..")
                break
            except Exception as e:
                print(e)
                domain = await DomainCheck.domain_check()
        seasonnalComicDom = P.DomParser(seasonnalComicText_Pather).parse(P.ListElementStrategyByText())[0]
        singalSeasonalDom_List = seasonnalComicDom.xpath(".//a")

        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(self.asyncSingalCrawlerTask(singalSeasonalDom,session)) for singalSeasonalDom in
                     singalSeasonalDom_List]
            result_List = await asyncio.gather(*tasks)
        await session.close()
        await asyncio.sleep(0.5)

        for result in result_List:
            # seasonalComic_DF = seasonalComic_DF.append({'season': result[0], 'seasonComic_DF': result[1]},ignore_index=True)
            temp_DF = pd.DataFrame([{'season': result[0], 'seasonComic_DF': result[1]}])
            seasonalComic_DF = pd.concat([seasonalComic_DF, temp_DF])
        return seasonalComic_DF

    async def asyncSingalCrawlerTask(self, singalSeasonalDom,session):
        singalSeasonalComicDF_Dict = dict()
        domain=postEvent('getDomain')
        count=0
        while True and count<10:
            try:
                singalSeasonalUrl = re.sub('http.*.com', domain, singalSeasonalDom.attrib('href'))
                print(singalSeasonalDom.text + ':' + singalSeasonalUrl)
                singalSeasonalText = await RP.AsyncRequestsProcessor(singalSeasonalUrl,session=session,proxy=proxy_aiohttp).text()
                break
            except Exception as e:
                print(e)
                count+=1
                if count < 5:
                    print(f'重新连接{count}')
                if count>5:
                    domain= await DomainCheck.domain_check()
                    count=0
                continue
        seasonalTitle_Pather = P.TextPather(htmlText=singalSeasonalText, xpath='//h2[1]')
        seasonalTitleDom = P.DomParser(seasonalTitle_Pather).parse(P.ListElementStrategyByText())
        # print(seasonalTitleDom[0].text)

        seansonalWeekDay_Pather = P.TextPather(htmlText=singalSeasonalText, xpath='//p[strong]')
        seansonalWeekDayDom_List = (P.DomParser(seansonalWeekDay_Pather).parse(P.ListElementStrategyByText()))

        for weekdayDom in seansonalWeekDayDom_List:
            # print(weekdayDom.text)
            comic_Pather = P.DomPather(dom=weekdayDom, xpath='./following-sibling::*[1]//td[text() or .//text()]')
            comicDom_List = P.DomParser(comic_Pather).parse(P.ListElementStrategyByDom())
            comicName_List = [comic.text for comic in comicDom_List]
            singalSeasonalComicDF_Dict[weekdayDom.text] = comicName_List

        singalSeasonalComic_DF = pd.DataFrame(
            {key: pd.Series(value, dtype='str') for key, value in singalSeasonalComicDF_Dict.items()})

        return StrProcessor(seasonalTitleDom[0].text).toStrip, singalSeasonalComic_DF


if __name__ == '__main__':
    pd.set_option('display.max_colwidth', None)  # 显示所有列，不进行缩略
    Listen.setDomainListener()
    AsyncStrategy().execute(seasonalComicCrawl().asyncCrawler())
    # index_pather = {
    #         'keyWords': input("BTHOME\n请输入关键词:")
    #     }
    #
    # #获取索引目录
    # torrentPage_DF = IndexCrawler(index_pather).crawler()

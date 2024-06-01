from api.lib.ToolKits.ElementProcess import *
from api.lib.ToolKits.Event import *
from api.lib.ToolKits.RequestsProcess import *
from api.lib.ToolKits.GeneralObject.StrProcess import *

import api.BtHomeObject as BTO
from api.lib.DomainCheck import *

async def comicTimelineCrawl():
    seasonalComic_DF = pd.DataFrame(columns=['season', 'seasonComic_DF'])
    while True:
        try:
            htmlText = RequestsProcessor(domain, proxies=globalProxy.proxy_request).text()
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
                RequestsProcessor(domain + '/' + JapanComicUrl,proxies=globalProxy.proxy_request).text()).xpath("//strong[contains(text(),'番组放映表')]/../..")[0]
            break
        except Exception as e:
            print(e)
            await domainCheck()
    singalSeasonalDom_List = seasonnalComicDom.xpath(".//a")

    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(comicTimelineCrawlBySeason(singalSeasonalDom,session)) for singalSeasonalDom in
                 singalSeasonalDom_List]
        result_List = await asyncio.gather(*tasks)


    for result in result_List:
        # seasonalComic_DF = seasonalComic_DF.append({'season': result[0], 'seasonComic_DF': result[1]},ignore_index=True)
        temp_DF = pd.DataFrame([{'season': result[0], 'seasonComic_DF': result[1]}])
        seasonalComic_DF = pd.concat([seasonalComic_DF, temp_DF])
    return seasonalComic_DF

async def comicTimelineCrawlBySeason(singalSeasonalDom,session):
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
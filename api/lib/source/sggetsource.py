import asyncio
from api.crawlobject import *
from api.lib.ToolKits.parse.elementutils import *
from api.lib.ToolKits.coroutine.coroutineutils import *
from api.lib.ToolKits.general.strutils import *
from api.lib.ToolKits.request.requestutils import *
from api.lib.config import *
from api.bthomeutils import *


@BtHomeUtils.register_sourceplugin('bthome_sgget')
def bthome_sgparse(torrentpage):
    subtitlegroup_list=[]

    htmltext = RequestUitls.get_html(name='dp_one_tab', url=torrentpage.url, type='get')
    doc = ElementUtils.parse_html(htmltext)
    sgelement_list = doc.xpath('//fieldset[@class="fieldset"][.//a]')

    for index,sgelement in enumerate(sgelement_list):
        torrentelement_list= sgelement.xpath('.//a')
        sg_name = " ".join([ElementUtils.get_text(p).replace("\t", "").replace("\n", "").strip()
                                      for p in sgelement.xpath('./preceding-sibling::p')]) \
                                      if sgelement.xpath('./ancestor::div[@class="message mt-1 break-all"]') else "主页"
        subtitlegroup_list.append(SubtitleGroup(name=sg_name, id=index, torrentelement_list=torrentelement_list, torrentpage=torrentpage))

    return subtitlegroup_list

@BtHomeUtils.register_sourceplugin('bthome_batch_sgget')
def bthome_batch_sgparse(torrentpage_list):
    subtitlegroup_list=[]

    pageurl_list = [torrentpage.url for torrentpage in torrentpage_list]
    html_list = RequestUitls.get_html(name='dp_multi_tab', url=pageurl_list, type='get')

    torrentelement_list = []
    for html in html_list:
        doc = ElementUtils.parse_html(html)
        sgelement_list = doc.xpath('//fieldset[@class="fieldset"][.//a]')

        for index,sgelement in enumerate(sgelement_list):
            torrentelement_list.extend(sgelement.xpath('.//a'))

    sg_name = "主页"
    subtitlegroup_list.append(SubtitleGroup(name=sg_name, id=1, torrentelement_list=torrentelement_list, torrentpage=torrentpage_list))

    return subtitlegroup_list

@BtHomeUtils.register_sourceplugin('bthome_multi_sgget')
def bthome_multi_sgparse(torrentpage):
    return bthome_sgparse(torrentpage)

@BtHomeUtils.register_sourceplugin('comicgarden_sgget')
def comicgarden_sgparse(torrentpage):

    subtitlegroup_list = []
    subtitlegroup_dict = {}



    for html in torrentpage.htmltext:
        torrentele_list = ElementUtils.parse_html(html).xpath("//td[@class='title']/a")
        for torrentele in torrentele_list:
            torrenturl=torrentele.attrib["href"]
            sgele = '其他' if torrentele.xpath('./preceding-sibling::*[1]') == [] else torrentele.xpath('./preceding-sibling::*[1]')[0]
            sgname= StrUtils.simplestrip(ElementUtils.get_text(sgele)) if not isinstance(sgele,str) else '其他'
            if sgname not in subtitlegroup_dict:
                subtitlegroup_dict[sgname] = []
            subtitlegroup_dict[sgname].append(torrenturl)

    for sg_name, torrentpageurl_list in subtitlegroup_dict.items():
        subtitlegroup =SubtitleGroup(name=sg_name,torrenturl_list=torrentpageurl_list, torrentpage=torrentpage)
        subtitlegroup_list.append(subtitlegroup)
    return subtitlegroup_list

if __name__=="__main__":
    pass
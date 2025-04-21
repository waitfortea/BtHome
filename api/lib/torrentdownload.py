__all__ = "torrentFilterByKeyword", 'getDownloadContent', 'torrent_download_queue', 'queueDownload','torrent_group_add'

import aiofiles
from api.lib.ToolKits.coroutine.coroutineutils import *
from api.crawlobject import *
from api.lib.ToolKits.request.cfcheck import *

torrent_download_queue = []


def torrentFilterByKeyword(torrentGroup: TorrentGroup, word_List):
    result_List = [torrent for torrent in torrentGroup.torrent_List if
                   StrProcessor(torrent.name).contains(word_List, mode='all')]
    return TorrentGroup(torrent_List=result_List, subtitle_group=torrentGroup.subtitle_group)

def torrent_group_add(torrentGroup,download_path):
    global torrent_download_queue
    download_dir = pathinit(download_path, flag="dir", make=True)
    torrentName_List = [file.baseName for file in
                        download_dir.get_contain_files(['.torrent','.rar'],fitler_mode="extension")]

    ignore_torrentname_List = []
    download_torrent_List = []

    for torrent in torrentGroup.torrent_List:
        if os.path.splitext(torrent.name)[0] not in torrentName_List:
            download_torrent_List.append(torrent)
        else:
            ignore_torrentname_List.append(torrent.name)

    if ignore_torrentname_List != []:
        ignore_message = {
            '任务类型': '忽略已存在种子'
            , '字幕组名称': torrentGroup.superObj.name
            , '下载源': torrentGroup.superObj.superObj.url
            , '下载目录': download_dir.absolutePath
            , '种子列表': "\n".join(ignore_torrentname_List)
        }
        callEvent("logDownloadWork", ignore_message)

    [torrent_download_queue.append((torrent,download_dir.absolutePath))  for torrent in download_torrent_List]
    return

async def getDownloadContent(torrent: Torrent):
    headers = {

        'user-agent': config['user_agent'],
    }
    print(torrent.downloadURL)
    print(cf_cookies.cookies)

    while True:
        # content  = await AsyncRequestsProcessor(torrent.downloadURL, session=aiohttpSession,
        #                                    proxy=globalProxy.proxy_aiohttp,cookies=cf_cookies.cookies,headers=headers).content()
        res  = await AsyncHttpxProcessor(torrent.downloadURL, session=asyncHttpxSession,headers=headers).response()
        content = res.content
        file_type = get_application_type(content)
        if  file_type != "text/html":
            print(file_type)
            break
        else:
            callEvent("cf_check",{})
            continue
    return content

async def torrent_async_download(torrent,download_path):
    content = await getDownloadContent(torrent)
    suffix = ContentProcessor(content).extension_type
    file_path = rf'{download_path}\{os.path.splitext(torrent.name)[0]}{suffix}'
    async with aiofiles.open(file_path, 'wb') as file:
        await file.write(content)
    return file_path

def torrent_async_download_strategy(torrent_info_list):
    tasks = [asyncio.create_task(torrent_async_download(torrent,download_path)) for torrent,download_path in torrent_info_list]
    torrent_path_list = all_complete(tasks)
    return torrent_path_list

def torrent_browser_download_strategy(torrent_info_list):
    torrent_add_path_list = []
    source_url = torrent_info_list[0][0].subtitle_group.torrent_page.index.url
    tab = global_brower.create_tab(source_url)
    for torrent, download_path in torrent_info_list:
        download_task = tab.add_element_a(torrent.downloadURL,text=torrent.name).click.to_download(rename=os.path.splitext(torrent.name)[0],save_path=download_path)
        global_brower.browser.wait.downloads_done()
        file = pathinit(download_task.final_path,flag='file')
        file.rename(baseName=f'{os.path.splitext(torrent.name)[0]}',suffix = file.extension_type)
        torrent_add_path_list.append(file.absolutePath)
    return torrent_add_path_list

def torrent_download(torrent_info_list,strategy=torrent_browser_download_strategy):
    return async_strategy(strategy(torrent_info_list))

def queueDownload():
    print("------download------")
    if torrent_download_queue != []:
        for torrent,download_path in torrent_download_queue:
            download_message = {
                '任务类型': '开始下载'
                , '字幕组名称': torrent.subtitle_group.name
                , '下载源': torrent.subtitle_group.torrent_page.url
                , '下载目录': download_path
                , '种子列表': f'{torrent.name}'
            }
            callEvent("logDownloadWork", download_message)
        torrent_add_path_list = torrent_download(torrent_download_queue)
        torrent_download_queue.clear()
        print("下载完成")
        return torrent_add_path_list
    else:
        return []



from api.lib.ToolKits.event.evenutils import *
from dataclasses import dataclass
from api.lib.ToolKits.customexc import *
from api.lib.config import *


@dataclass()
class CfCookie:
    cookies : str = None
    headers = headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    }

cf_cookies = CfCookie()

def get_cf_token(rm_cache=False,**kwargs):
    page = DrissionPageProcessor(path=config["edge_exe_path"])
    connected  = page.get("https://www.1lou.info/",mode='d',retry=2,timeout=20)
    cf_cookies = page.pass_cf(**kwargs)
    if rm_cache:
        page.rm_cache(cookies=True)
    return cf_cookies

def doEvent_cfcheck(data={}):
    global cf_cookies
    cookie = get_cf_token(rm_cache=False,check_interval=3,**data)
    try:
        cf_cookies.cookies = {"cf_clearance":cookie['cf_clearance'],"bbs_sid":cookie['bbs_sid']}
        print(cf_cookies.cookies)
    except Exception as e:
        DictKeyError()



def setup_cfcheck():
    addEvent("cf_check",doEvent_cfcheck)


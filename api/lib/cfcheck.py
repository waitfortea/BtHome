
from api.lib.ToolKits.drissionpage_process import *
from api.lib.ToolKits.Event import *
from dataclasses import dataclass
from api.lib.ToolKits.CustomException import *
from api.lib.Config import *
import atexit
@dataclass()
class CfCookie:
    cookies : str

cf_cookies = CfCookie("")

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



from api.lib.ToolKits.drissionpage_process import *
from api.lib.ToolKits.Event import *
from dataclasses import dataclass

@dataclass()
class CfCookie:
    cookies : str

cf_cookies = CfCookie("")

def get_cf_token(rm_cache=False,**kwargs):
    page = DrissionPageProcessor()
    connected  = page.get("https://www.1lou.info/",mode='d',retry=2,timeout=20)
    cf_cookies = page.pass_cf(**kwargs)
    if rm_cache:
        page.rm_cache(cookies=True)
    return cf_cookies

def doEvent_cfcheck(data={}):
    global cf_cookies
    cf_cookies.cookies = get_cf_token(rm_cache=True,**data)
    print(cf_cookies.cookies)


def setup_cfcheck():
    addEvent("cf_check",doEvent_cfcheck)


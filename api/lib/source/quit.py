
from api.lib.ToolKits.request import *

from api.bthomeutils import *


@BtHomeUtils.register_sourceplugin('bthome_quit')
def bthome_quit(*args, **kwargs):
    RequestUitls.quit(name="dp")
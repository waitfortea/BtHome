
from threading import Thread
from api.lib.ToolKits.general.utils import *
from api.crawlobject import *
from api.lib.sql.sqlutils import *
from api.lib.config import *
from api.lib.ToolKits.parse.serializeutils import *
from api.lib.ToolKits.general.datetimeutils import *
from api.bthomeutils import *
from api.lib.log import *
@BtHomeUtils.register_sourceplugin('bthome_subscribe')
def subscribesql(info_dict, mysqlconfig=None, *args, **kwargs):
    if mysqlconfig is None:
        mysqlconfig = SerializeUtils.get_yamldict(f"{re.search(r'.*BtHome', os.path.dirname(sys.argv[0])).group()}/config/config.yaml")['mysql']
    sqlsession = SqlUtils(mysqlconfig, logfun=infolog)


    if not getattr(subscribesql, '_initialized', False):
        sqlsession.sql('create database if not exists bthome character set utf8mb4 collate utf8mb4_general_ci')
        sqlsession.sql('use bthome')
        createtable_sql = (
            'create table if not exists subscribe(id int auto_increment, create_time datetime, torrentpage_url varchar(100)'
            ', subtitlegroup_name varchar(100), subtitlegroup_id int, filterword varchar(100)'
            ', savepath varchar(100), in_use int'
            ', primary key (id, torrentpage_url, subtitlegroup_name))'
        )
        sqlsession.sql(createtable_sql)

        setattr(subscribesql, '_initialized', True)

    sqlsession.sql('use bthome')
    insert_sql = (f'insert ignore into subscribe(create_time, torrentpage_url, subtitlegroup_name, subtitlegroup_id'
                 f', filterword, savepath, in_use) values("{DatetimeUtils.now_format()}", "{info_dict["torrentpage_url"]}"'
                 f',"{info_dict["subtitlegroup_name"]}", "{info_dict["subtitlegroup_id"]}", "{info_dict["filterword"]}", {repr(info_dict["savepath"])}'
                  f', 1)'
                  )
    sqlsession.sql(insert_sql)

    sqlsession.commit()
    loginfo = (f'已订阅 源网页:{info_dict["torrentpage_url"]} 字幕组:{info_dict["subtitlegroup_name"]}'
              f' id:{info_dict["subtitlegroup_id"]} 筛选:{info_dict["filterword"]} 保存:{info_dict["savepath"]}')
    EventUtils.run('infolog', logdata=loginfo)




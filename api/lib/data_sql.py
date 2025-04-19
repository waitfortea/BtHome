
from api.lib.sql.sql_process import *
from api.lib.Config import *
from api.lib.ToolKits.eventplugin.eventregister import *


def do_event_bthome_sqlite_init(data):
    global_sqlite_cursor.connect(database_dir=config['sqlite3']['database_dir'],
                                 database_name=config['sqlite3']['database_name'])
    global_sqlite_cursor.create_table("torrentpage", 'url text,title text not null', index_text="unique (url)")

def do_event_insert_table_torrentpage(data:Dict[str,List[Union[str,List]]]):
    """

    :param data:
        data = {
                "field_name":[field_name1,.field_name2]
                ,"rows":[ [value1,value2] ]
                }
    :return:
    """
    global_sqlite_cursor.use_table('torrentpage')
    global_sqlite_cursor.replace_table_row(data['field_name'],data['rows'])
    global_sqlite_cursor.commit()


def setup_bthome_sql():
    addEvent("bthome_sqlite_init",do_event_bthome_sqlite_init)
    addEvent('bthome_insert_table_torrentpage',do_event_insert_table_torrentpage)


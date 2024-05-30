from datetime import datetime,timedelta
import time
from dateutil import parser
from dateutil.relativedelta import relativedelta
import calendar

def hourParse(text,out='hour',split_List=['小时','分钟','秒']):
    if len(text.split(split_List[0]))==2:
        hour, other = text.split(split_List[0])
    else:
        other=text.split(split_List[0])[-1]
        hour=0


    if len(other.split(split_List[1])) == 2:
        minute, other = other.split(split_List[1])
    else:
        other = other.split(split_List[1])[-1]
        minute=0

    if other !="":
        second=other.split(split_List[2])[0]
    else:
        second=0
    if out=='hour':
        return int(hour)+int(minute)/60
    elif out=='minute':
        return int(hour)*60+int(minute)+int(second)/60

class Date:
    def __init__(self,date,formatStr=None):
        if formatStr:
            self.dateTime=datetime.strptime(dateStr,formatStr)
        else:
            if isinstance(date,str):
                self.dateTime=parser.parse(date)
            elif isinstance(date,datetime):
                self.dateTime=date

    def formatStr(self,formatStr):
        return self.dateTime.strftime(formatStr)

    def getDateByFormatStr(self,dataStr,formatStr="%Y%m%d"):
        return Date(datetime.strptime(formatStr,formatStr))

    @property
    def date(self):
        return DateProcessor(self.dateTime.date())

    @property
    def time(self):
        return TimeProcessor(self.dateTime.time())

    @property
    def firstDayOfMonth(self):
        year, month = self.dateTime.year, self.dateTime.month
        _, days_in_month = calendar.monthrange(year, month)
        return Date(f'{int(year):04}{int(month):02}{int(1):02}')

    @property
    def endDayOfMonth(self):
        year, month = self.dateTime.year, self.dateTime.month
        _, days_in_month = calendar.monthrange(year, month)
        return Date(f'{int(year):04}{int(month):02}{int(days_in_month):02}')

    @property
    def unixTime(self):
        return int(self.dateTime.timestamp())
        # return  int((self.dateTime - datetime(1970, 1, 1, 8, 0, 0)).total_seconds())

    @property
    def dateTimeStr(self):
        return  self.dateTime.strftime('%Y/%#m/%#d %H:%M:%S')

    def add(self,days=0,months=0,years=0):
        dateResult=self.dateTime+DateTimeDelta(years=years,months=months,days=days).dateTimeDelta
        return Date(dateResult)


class DateProcessor:
    def __init__(self,date):
        self.date=date

    def formatStr(self,format):
        return self.data.strftime(format)

    def unixTime(self,suffixTime="00:00:00"):
        return Date(self.dateStr(seperator="-",prefix=True)+" "+suffixTime).unixTime

    def dateStr(self,seperator='/',prefix=False,suffixTime=False):
            dateStr= self.date.strftime(seperator.join(['%Y','%#m','%#d'])) if not prefix else self.date.strftime(seperator.join(['%Y','%m','%d']))
            return dateStr

    def datetimeStr(self,suffixTime="00:00:00"):
        return self.dateStr + "" + suffixTime

    def isLess(self,verseDate,isequl=False):
        if self.date<=Date(verseDate).date.date:
            return True
        else:
            return False

    def isMore(self,verseDate,isequal=False):
        if self.date >= Date(verseDate).date.date:
            return True
        else:
            return False

class TimeProcessor:
    def __init__(self,time):
        self.time=time

class DateTimeDelta:
    def __init__(self,days=0,months=0,years=0):
        self.dateTimeDelta=relativedelta(years=years,days=days,months=months)

class UnixTime:
    def __init__(self,unixInt):
        self.localTimeStruct = time.localtime(unixInt)

    @property
    def dateTime(self):
        return Date(datetime(
            year=self.localTimeStruct.tm_year,
            month=self.localTimeStruct.tm_mon,
            day=self.localTimeStruct.tm_mday,
            hour=self.localTimeStruct.tm_hour,
            minute=self.localTimeStruct.tm_min,
            second=self.localTimeStruct.tm_sec
        ))




if __name__=='__main__':
    # df=pd.read_excel(r'D:\桌面\test1.xlsx')
#     # df['时长MIN']=df.apply(lambda row:hourParse(row['时长'],out='minute') if row['时长']!="-" else 0,axis=1)
#     # df.to_excel(r'D:\桌面\test1_re    sult.xlsx')
    print(Date('20240101').date.isLess('20230101'))
    print(hourParse("-"))
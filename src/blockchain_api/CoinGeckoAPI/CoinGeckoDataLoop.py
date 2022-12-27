import calendar
import datetime

from datetime import datetime
from datetime import timedelta
daterun = '06-15-2021'  #MMDDYYYY

count=0
cs_list=[]
cs_list_id=[]
level =[]
hogerlevel=[]
start_dti =[]
end_dti =[]
scripts = ['CoinGeckoData.py','DefiLama.py','KPIFramework.py']

def listloopdateadd(mod):
    if mod > 0:
      welnietdateadd=-1
    else:
      welnietdateadd=0
    return welnietdateadd

def listloop(mod):
    if mod > 0:
      cs_list = "icon","ethereum","chainlink"
      cs_list_id = "1","2","3"
      level = "1","1","2"
      hogerlevel = "1", "1", "2"
    else:
      cs_list = "barnbridge","cardano","aave"
      cs_list_id = "4","5","6"
      level = "2", "1", "2"
      hogerlevel = "2","1","2"
    return cs_list,cs_list_id,level,hogerlevel

from time import time, sleep
while True:
    sleep(75 - time() % 75)
    count += 1
    mod = count % 2
    print('CoinGeckoDataLoop started')
    datestart = datetime.strptime(daterun,'%m-%d-%Y') + timedelta(days=listloopdateadd(mod)+count)
    dateend = datetime.strptime(daterun,'%m-%d-%Y') + timedelta(days=listloopdateadd(mod)+count+1)
    start_dti.append(datestart)
    end_dti.append(dateend)
    print(start_dti)
    print(end_dti)
    #datestart = date.replace(day=1)
    #dateend = date.replace(day=calendar.monthrange(date.year, date.month)[1])
    cs_list.clear()
    cs_list_id.clear()
    level.clear()
    hogerlevel.clear()
    cs_listtmp = list(listloop(mod)[0])
    cs_list_idtmp = list(listloop(mod)[1])
    leveltmp = list(listloop(mod)[2])
    hogerleveltmp = list(listloop(mod)[3])
    for x in cs_listtmp:
        cs_list.append(x)
    for x in cs_list_idtmp:
        cs_list_id.append(x)
    for x in leveltmp:
        level.append(x)
    for x in hogerleveltmp:
        hogerlevel.append(x)
    for i in scripts:
        exec(open(i).read())
    start_dti.clear()
    end_dti.clear()
    print('CoinGeckoDataLoop loaded')


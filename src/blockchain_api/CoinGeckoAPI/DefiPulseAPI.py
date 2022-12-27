from pycoingecko import CoinGeckoAPI
import json
import pandas as pd
import requests
from datetime import datetime
import numpy as np
#import CoinGeckoDataLoop.py as CoinGeckoDataLoop

parametersdefipulse = {
    "api-key": "6e3fdbcf6d4ece0f75fff42f19c30ffead066004d97d55999a9a78af222a",
    "project": "barnbridge",
}

parametersdefillama = {
     "slug": "barnbridge",
}
urldefillama = "https://api.llama.fi/protocol"

url = 'https://data-api.defipulse.com/api/v1/defipulse/api/GetHistory?'
# sending get request and saving the response as response object
r = requests.get(url-urldefillama,params=parametersdefillama)

# extracting data in json format
#data = r.json()
print(r.text)

#print(CoinGeckoDataLoop.daterun)
print('DefiPulseAPI started')

requestgroup = ['market_data','community_data','public_interest_stats']
kpi_request = {'market_data': ['current_price','total_volume'],
               'community_data': ['twitter_followers'],
               'public_interest_stats' : ['alexa_rank']}
kpi_id = {'market_data': ['17','18','19'],
              'community_data': ['20'],
              'public_interest_stats': ['21']}

#start_dti = '08/01/2021'
#end_dti = '08/01/2021'
index = pd.date_range(start_dti[0], end_dti[0])

appended_data = []
for t in requestgroup:
    #print(t)
    for d in index.strftime('%d-%m-%Y'):
        #print(d)
        for s, o in zip(kpi_id[t], list(kpi_request[t])):
            #print(s)
            #print(o)
            for a,g in zip(cs_listtj,cs_list_idtj):
                #print(a)
                #print(g)
                data = cg.get_coin_history_by_id(a, str(d))
                if t == 'market_data':
                    history = pd.DataFrame(data=[{'d_date_id' : str(d),
                                                 a: data[t][o]['eur']}]).set_index('d_date_id')
                else:
                    history = pd.DataFrame(data=[{'d_date_id': str(d),
                                              a: data[t][o]}]).set_index('d_date_id');
                history['d_level0_id'] = 1
                history['Denominator'] = 0
                history['d_kpi_id'] = s
                history['d_level1_id'] = str(g)
                history['d_level2_id'] = 1
              #  history['d_level3_id'] = 0
              #  history['d_level4_id'] = 0
                history['Numerator'] = ''
                appended_data.append(history)


appended_data = pd.concat(appended_data)

#df['DOB']=pd.to_datetime(df['DOB'].dt.strftime('%m/%d/%Y'))

f_kpi_CoinGecko = appended_data.reset_index('d_date_id') #rename(columns={"icon": "Numerator"}).
print(f_kpi_CoinGecko)

#f_kpi_CoinGecko['Numerator'] = f_kpi_CoinGecko['icon'] + f_kpi_CoinGecko['ethereum']
f_kpi_CoinGecko = f_kpi_CoinGecko.fillna(0)
f_kpi_CoinGecko["Numerator"] = (f_kpi_CoinGecko[cs_list[0]] + f_kpi_CoinGecko[cs_list[1]] + f_kpi_CoinGecko[cs_list[2]]).astype("float")

f_kpi_CoinGecko['d_date_id'] = pd.to_datetime(f_kpi_CoinGecko['d_date_id'],format='%d-%m-%Y')
f_kpi_CoinGecko['d_date_id'] =  f_kpi_CoinGecko.d_date_id.apply(lambda x: x.strftime('%Y%m%d')).astype(int)

f_kpi_CoinGecko = f_kpi_CoinGecko.drop(columns=cs_list,axis=1)

print(f_kpi_CoinGecko)

#tmp_d_level0_id           = pd.DataFrame(pd.read_excel("C:/Users/nickh/PycharmProjects/daopi2/assets/Attributes/Generic attributes/LEVEL0_Blockchain_Library.xlsx");

#d_level0_id           = tmp_d_level0_id[['d_level0_id','Calculation']];

f_kpi_CoinGecko.to_csv(r'C:\Users\nickh\PycharmProjects\daopi2\assets\Attributes\Blockchain industry\CoinGeckoData\f_kpi_CoinGecko.csv', index=False)
#Numerator,Denominator,d_kpi_id,d_level0_id,d_level1_id,d_level2_id,d_date_id

print('CoinGeckoAPI loaded')

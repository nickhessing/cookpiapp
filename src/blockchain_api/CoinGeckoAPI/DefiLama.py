from defillama import DefiLlama
import json
import pandas as pd
import requests
from datetime import datetime
import numpy as np
#import DefiLamaDataLoop.py as DefiLamaDataLoop
import json
import os

outname='f_kpi_DefiLama.csv'
outdir='C:/Users/nickh/PycharmProjects/daopi2/assets/Attributes/Blockchain industry/DefiLamaData'

if not os.path.exists(outdir):
    os.mkdir(outdir)

fullname=os.path.join(outdir,outname)


urldefillama = "https://api.llama.fi/protocol"

url = 'https://data-api.defipulse.com/api/v1/defipulse/api/GetHistory?'
# sending get request and saving the response as response object
#r = requests.get(url-urldefillama,params=parametersdefillama)

# extracting data in json format
#data = r.json()
#print(r.text)

cs_list = ["icon","ethereum","fantom","avalanche","solana"]
cs_list_id = ["1","2","7","8","9"]

print('DefiLamaAPI started')
llama = DefiLlama()
#from CoinGeckoDataLoop import cs_list
#from CoinGeckoDataLoop import cs_list_id
#from CoinGeckoDataLoop import start_dti
#from CoinGeckoDataLoop import end_dti


tvl_history = requests.get('https://api.llama.fi/charts/ethereum')
#print(tvl_history.json())
#tvl_history = positions.json()
#latest_tvl = float(positions['tvl'][-1]['totalLiquidityUSD'])
#response = llama.get_historical_tvl(name='uniswap')

#print(latest_tvl)


cs_listtj=[]
for x in cs_list:
    cs_listtj.append(x)

cs_list_idtj=[]
for x in cs_list_id:
    cs_list_idtj.append(x)

kpi_request = {'TVL'}
kpi_id = {'22'}

#start_dti = '08/01/2021'
#end_dti = '08/01/2021'
#index = pd.date_range(start_dti[0], end_dti[0])

appended_data = []

for a,g in zip(cs_listtj,cs_list_idtj):
    data = requests.get('https://api.llama.fi/charts/'+str(a)).json()
    #datatst = {str(a):data}
    dataframe = pd.json_normalize(data)
    dataframe.rename(columns={'date': 'd_date_id'}, inplace=True)
    dataframe.rename(columns={'totalLiquidityUSD': 'Numerator'}, inplace=True)
    dataframe['d_level0_id'] = 1
    dataframe['Denominator'] = 0
    dataframe['d_kpi_id'] = 22
    dataframe['d_level1_id'] = str(g)
    dataframe['d_level2_id'] = 1
    #  dataframe['d_level3_id'] = 0
    #  dataframe['d_level4_id'] = 0
    appended_data.append(dataframe)

appended_data = pd.concat(appended_data)


#df['DOB']=pd.to_datetime(df['DOB'].dt.strftime('%m/%d/%Y'))

#f_kpi_DefiLama = appended_data.reset_index('d_date_id') #rename(columns={"icon": "Numerator"}).
#print(f_kpi_DefiLama)

#f_kpi_DefiLama['Numerator'] = f_kpi_DefiLama['icon'] + f_kpi_DefiLama['ethereum']
f_kpi_DefiLama = appended_data.fillna(0)


f_kpi_DefiLama['d_date_id'] = pd.to_datetime(f_kpi_DefiLama['d_date_id'],unit='s')
f_kpi_DefiLama['d_date_id'] = pd.to_datetime(f_kpi_DefiLama['d_date_id'],format='%d-%m-%Y')
f_kpi_DefiLama['d_date_id'] = f_kpi_DefiLama.d_date_id.apply(lambda x: x.strftime('%Y%m%d')).astype(int)

print(f_kpi_DefiLama)
f_kpi_DefiLama.to_csv(fullname, index=False)
#f_kpi_DefiLama.to_csv(r'C:\Users\nickh\PycharmProjects\daopi2\assets\Attributes\Blockchain industry\DefiLamaData\f_kpi_DefiLama.csv', index=False)
#print('DefiLamaAPI loaded')

print('DefiLamaAPI test ended')

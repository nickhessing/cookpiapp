print('DefiLamaAPI started')

import pandas as pd
import requests

import os

outname='f_kpi_ICON.csv'
outdir='C:/Users/nickh/PycharmProjects/daopi2/assets/Attributes/Blockchain industry/ICONBlockchainData'


projectlist = ['balanced','omm']
projectlistid = [6,7]

if not os.path.exists(outdir):
    os.mkdir(outdir)

fullname=os.path.join(outdir,outname)


KPIFramework = []
for i,a in zip(projectlist,projectlistid):
    KPIFrameworktmp = pd.DataFrame(pd.read_csv(r'C:\Users\nickh\PycharmProjects\daopi2\assets\Attributes\Blockchain industry\ICONBlockchainData/'+str(i)+'.csv', sep=';',decimal='.',index_col = False))
    KPIFrameworktmp.rename(columns={'tvl': 'Numerator'}, inplace=True)
    pd.to_numeric(KPIFrameworktmp["Numerator"])
    KPIFrameworktmp.drop('timestamp', axis=1, inplace=True)
    KPIFrameworktmp['d_level0_id'] = 1
    KPIFrameworktmp['Denominator'] = 0
    KPIFrameworktmp['d_kpi_id'] = 22
    KPIFrameworktmp['d_level1_id'] = 1
    KPIFrameworktmp['d_level2_id'] = a
    #  dataframe['d_level3_id'] = 0
    #  dataframe['d_level4_id'] = 0
    KPIFramework.append(KPIFrameworktmp)
    print(KPIFrameworktmp)

KPIFramework = pd.concat(KPIFramework)
#print(KPIFramework)
f_kpi_ICON = KPIFramework.fillna(0)


f_kpi_ICON['d_date_id'] = pd.to_datetime(f_kpi_ICON['d_date_id'],format='%d/%m/%Y')
f_kpi_ICON['d_date_id'] = f_kpi_ICON.d_date_id.apply(lambda x: x.strftime('%Y%m%d')).astype(int)

print(f_kpi_ICON)
f_kpi_ICON.to_csv(fullname, index=False)
#f_kpi_DefiLama.to_csv(r'C:\Users\nickh\PycharmProjects\daopi2\assets\Attributes\Blockchain industry\ICONBlockchainData\f_kpi_ICON.csv', index=False)
#print('DefiLamaAPI loaded')

print('ICONBlockchain ended')


"""
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential

STORAGEACCOUNTURL= "DefaultEndpointsProtocol=https;AccountName=cookpiblob;AccountKey=xC6Vslgs0XuU5zLEyyaWv2IuQqbXLgcpfTtMlTXsuP8+hZWXBsGAagsWoxocqS5d2jX5XeIwETJ2+AStshqg+g==;EndpointSuffix=core.windows.net"
STORAGEACCOUNTNAME = "cookpiblob"
connection_string = "DefaultEndpointsProtocol=https;AccountName=cookpiblob;AccountKey=umLZxjua6ETzNaWbcMJB1ZY0Bpl+dTKJtRf7dQv8J1rgMmePN8y/TcJDTpwNt/cSwdA7Q13HvVzL+AStT4sl7g==;EndpointSuffix=core.windows.net"
STORAGEACCOUNTKEY= "umLZxjua6ETzNaWbcMJB1ZY0Bpl+dTKJtRf7dQv8J1rgMmePN8y/TcJDTpwNt/cSwdA7Q13HvVzL+AStT4sl7g=="
CREDENTIAL = {
            "account_name": "cookpiblob",
            "account_key": "umLZxjua6ETzNaWbcMJB1ZY0Bpl+dTKJtRf7dQv8J1rgMmePN8y/TcJDTpwNt/cSwdA7Q13HvVzL+AStT4sl7g=="
            }
LOCALFILENAME= "d_kpi_synthetix.csv"
CONTAINERNAME= "exampleproject"
BLOBNAME= "cookpiblob"

print('1')
#download from blob
t1=datetime.datetime.now()
print('2')
blob_service_client_instance = BlobServiceClient(account_url=STORAGEACCOUNTURL, credential=CREDENTIAL)
print('3')
blob_client_instance = blob_service_client_instance.get_blob_client(CONTAINERNAME, BLOBNAME, snapshot=None)
print('4')
print(blob_client_instance)
with open(LOCALFILENAME, "wb") as my_blob:
    print('5')
    print(my_blob)
    print('5-5')
    print(blob_client_instance)
    print('-6')
    blob_data = blob_client_instance.download_blob()
    print('6')
    blob_data.readinto(my_blob)
t2=datetime.datetime.now()
print(("It takes %s seconds to download "+BLOBNAME) % (t2 - t1))
print(pd.read_csv(LOCALFILENAME))

"""
import openpyxl
import pandas as pd
import datetime
#import "./constants2.css"
import dash
from dash import Dash, dcc, html, Input, Output, State, MATCH, ALL, ctx
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State 
import dash_daq as daq
import dash_trich_components as dtc
import glob
import os
import pandas as pd
import plotly.express as px
import plotly.io as pio
import numpy as np
from dash_breakpoints import WindowBreakpoints

#from dash_extensions.callback import CallbackCache, DiskCache

import base64
BeautifulSignalColor="#f3f6d0"
Highlightcardcolor="#f3f6d0"
graphcolor="#243b55" #8EC5FC #tbv export
fontcolor='rgb(247, 239, 213)'  #141e30
buttoncolor="#f3f6d0"
buttonlogocolor="#020b15"
slides_to_show_ifenough = 3
slides_to_scroll = 3
# to render in jupyterlab
pio.renderers.default = "plotly_mimetype"

#import MessageApp 
gapminder = px.data.gapminder()
gapminder.head()

image_directory = '/Users/chriddyp/Desktop/'
list_of_images = [os.path.basename(x) for x in glob.glob('{}*.png'.format(image_directory))]
static_image_route = '/static/'

today = datetime.datetime.now()
thisYear = today.year
firstDay = datetime.datetime(thisYear, 1, 1)
lastDay = datetime.datetime(thisYear, 12, 31)
firstDayStr = firstDay.strftime('%Y-%m-%d')
lastDayStr = lastDay.strftime('%Y-%m-%d')


#openimage = Image.open(r'/assets/Images/synthetix.png')


# engine = create_engine('mysql+pymysql://root:Handschoen92@localhost:3306/kpiframework')
# dbConnection    = engine.connect()

# SQL Retrieve data

KPIFrameworktmp = pd.DataFrame(
        pd.read_csv(r'assets/Attributes/dashboard_data/KPIFramework_Python.csv',low_memory=False))

# Dataframes
# f_kpi           = pd.read_sql("select * from kpiframework.f_kpi", dbConnection);
cookpi_attributestmp = pd.read_excel(open('assets/Attributes/dashboard_data/cookpi_per_pi.xlsx', 'rb'),
              sheet_name='linktable');

KPIIDList =  cookpi_attributestmp['d_kpi_id'].unique()

KPIFrameworklist =[]

for i in KPIIDList:
    KPIFrameworkloop = KPIFrameworktmp[(KPIFrameworktmp.d_kpi_id ==i)]
    cookpi_attributes = cookpi_attributestmp[(cookpi_attributestmp.d_kpi_id == i)]
    sheettmp = cookpi_attributes[(cookpi_attributes.Level_ID_present =="d_level0_id")] 
    sheettmpl1 = cookpi_attributes[(cookpi_attributes.Level_ID_present =="d_level1_id")] 
    sheettmpl2 = cookpi_attributes[(cookpi_attributes.Level_ID_present =="d_level2_id")] 
    rename = dict(sheettmp.set_index('Level_ID')['Level_ID_present'].to_dict()) 
    renamel1 = dict(sheettmpl1.set_index('Level_ID')['Level_ID_present'].to_dict()) 
    renamel2 = dict(sheettmpl2.set_index('Level_ID')['Level_ID_present'].to_dict()) 
    rename_dict = {}
    rename_dict.update(rename)
    rename_dict.update(renamel1)
    rename_dict.update(renamel2)
    KPIFrameworkloop.rename(columns=rename_dict, inplace = True)
    KPIFrameworklist.append(KPIFrameworkloop)

KPIFramework = pd.concat(KPIFrameworklist)
print(KPIFramework.dtypes)

KPIFramework['d_level0_id']=KPIFramework['d_level0_id'].astype(int)
KPIFramework['d_level1_id']=KPIFramework['d_level1_id'].astype(int)
KPIFramework['d_level2_id']=KPIFramework['d_level2_id'].astype(int)


columnsdf0 = KPIFramework.columns.tolist()
columnsdf0.remove('d_level1_id')
columnsdf0.remove('d_level2_id')
columnsdf0.remove('Numerator')
columnsdf0.remove('Denominator')
columnsdf0.remove('Numerator_LP')
columnsdf0.remove('Denominator_LP')
columnsdf0.remove('Period_int_lp')

columnsdf1 = KPIFramework.columns.tolist()
columnsdf1.remove('d_level2_id')
columnsdf1.remove('Numerator')
columnsdf1.remove('Denominator')
columnsdf1.remove('Numerator_LP')
columnsdf1.remove('Denominator_LP')
columnsdf1.remove('Period_int_lp')

columnsdf2 = KPIFramework.columns.tolist()
columnsdf2.remove('Numerator')
columnsdf2.remove('Denominator')
columnsdf2.remove('Numerator_LP')
columnsdf2.remove('Denominator_LP')
columnsdf2.remove('Period_int_lp')

#KPIFrameworkl0 = KPIFramework.groupby(columnsdf0, as_index=False).agg(
#    {'Denominator': 'sum', 'Numerator': 'sum', 'Denominator_LP': 'sum', 'Numerator_LP': 'sum'})
#
#KPIFrameworkl1 = KPIFramework.groupby(columnsdf1, as_index=False).agg(
#    {'Denominator': 'sum', 'Numerator': 'sum', 'Denominator_LP': 'sum', 'Numerator_LP': 'sum'})
#KPIFrameworkl2 = KPIFramework.groupby(columnsdf2, as_index=False).agg(
#    {'Denominator': 'sum', 'Numerator': 'sum', 'Denominator_LP': 'sum', 'Numerator_LP': 'sum'})
#
#KPIFrameworkl0.to_csv(r'assets/Attributes/dashboard_data/KPIFrameworkl0.csv',
#                      index=False)
#KPIFrameworkl1.to_csv(r'assets/Attributes/dashboard_data/KPIFrameworkl1.csv',
#                      index=False)
#KPIFrameworkl2.to_csv(r'assets/Attributes/dashboard_data/KPIFrameworkl2.csv',
#                      index=False)



d_kpi_tmp = pd.read_excel(open('assets/Attributes/dashboard_data/cookpi_per_pi.xlsx', 'rb'),
              sheet_name='d_kpi')
#d_kpi_tmp = pd.DataFrame(
#    pd.read_csv("assets/Attributes/dashboard_data/d_kpi_synthetix.csv", sep=';',
#                index_col=False));
kpilevelcount = cookpi_attributestmp.groupby(['d_kpi_id'])['d_kpi_id'].count().reset_index(name="kpilevelcount")
d_kpi = d_kpi_tmp[(d_kpi_tmp.live == 1)] #& (df.carrier == "B6")
d_kpi = d_kpi.merge(kpilevelcount)

d_kpi.sort_values(by=['Sorting'])

# use on_demand=True to avoid loading worksheet data into memory
#openpyxl.load_workbook
wb = openpyxl.load_workbook(r'assets/Attributes/dashboard_data/cookpi_per_pi.xlsx')
sheetcount = len(wb.sheetnames)
sheetnames = wb.sheetnames
sheetnames.remove('d_kpi')
sheetnames.remove('linktable')


#for i in KPIIDList:
#    sheet = dict(cookpi_attributes[(cookpi_attributes.d_kpi_id==i)].set_index('Join_ID')['Level_ID'].to_dict())


#d_level0 = pd.DataFrame(
#    pd.read_csv(r'assets/Attributes/dashboard_data/LEVEL0_Synthetix_Library.csv',
#                sep=';', index_col=False));
#
#d_level1 = pd.DataFrame(
#    pd.read_csv(r'assets/Attributes/dashboard_data/LEVEL1_Synthetix_Library.csv',
#                sep=';', index_col=False));
#d_level2 = pd.DataFrame(
#    pd.read_csv(r'assets/Attributes/dashboard_data/LEVEL2_Synthetix_Library.csv',
#                sep=';', index_col=False));

KPINumAgg = dict(d_kpi.set_index('KPIName')['AggregateNum'].to_dict())
KPIDenomAgg = dict(d_kpi.set_index('KPIName')['AggregateDenom'].to_dict())

KPINumAggid = dict(d_kpi.set_index('d_kpi_id')['AggregateNum'].to_dict())
KPIDenomAggid = dict(d_kpi.set_index('d_kpi_id')['AggregateDenom'].to_dict())

def AggregateNumDenom(Calculation):
    if Calculation == 1:
        CalculationString = "'sum'"
        return CalculationString
    elif Calculation == 2:
        CalculationString = "'mean'"
        return CalculationString
    elif Calculation == 3:
        CalculationString = "'max'"
        return CalculationString

keysl0 = ['d_kpi_id', 'd_level0_id']
keysl1 = ['d_kpi_id', 'd_level0_id', 'd_level1_id']
ListGrain = ['int_day', 'int_month', 'int_quarter', 'int_year']

dfl02 = []
dfl12 = []
dfl22 = []
dfl0Compare2 =[]
dfl1Compare2= []
dfl2Compare2= []

dfl02.clear()
dfl12.clear()
dfl22.clear()
dfl0Compare2.clear()
dfl1Compare2.clear()
dfl2Compare2.clear()

for i in KPIIDList:
    KPIFramework_iterate = KPIFramework[(KPIFramework.d_kpi_id ==i)]
    
    KPIFrameworkl0 = KPIFramework_iterate.groupby(columnsdf0, as_index=False).agg(
    {'Denominator': eval(AggregateNumDenom(KPIDenomAggid[i])), 'Numerator': eval(AggregateNumDenom(KPINumAggid[i])), 'Denominator_LP': eval(AggregateNumDenom(KPIDenomAggid[i])), 'Numerator_LP': eval(AggregateNumDenom(KPINumAggid[i]))})
    
    KPIFrameworkl1 = KPIFramework_iterate.groupby(columnsdf1, as_index=False).agg(
    {'Denominator': eval(AggregateNumDenom(KPIDenomAggid[i])), 'Numerator': eval(AggregateNumDenom(KPINumAggid[i])), 'Denominator_LP': eval(AggregateNumDenom(KPIDenomAggid[i])), 'Numerator_LP': eval(AggregateNumDenom(KPINumAggid[i]))})
    
    KPIFrameworkl2 = KPIFramework_iterate.groupby(columnsdf2, as_index=False).agg(
    {'Denominator': eval(AggregateNumDenom(KPIDenomAggid[i])), 'Numerator': eval(AggregateNumDenom(KPINumAggid[i])), 'Denominator_LP': eval(AggregateNumDenom(KPIDenomAggid[i])), 'Numerator_LP': eval(AggregateNumDenom(KPINumAggid[i]))})
    
    cookpi_attributes = cookpi_attributestmp[(cookpi_attributestmp.d_kpi_id == i)]
    if 'd_level0_id' not in cookpi_attributes['Level_ID_present'].unique().tolist():
        continue
    sheettmp = cookpi_attributes[(cookpi_attributes.Level_ID_present =="d_level0_id")] 
    
    #df.rename(columns={"A": "a", "B": "c"})
    sheet = dict(sheettmp.set_index('Level_ID_present')['Join_ID'].to_dict()) 
    sheetchangeback = dict(sheettmp.set_index('Join_ID')['Level_ID_present'].to_dict()) 
    keys = ['d_kpi_id']
    keyslist = list(sheet.values())
    cols =['LevelName', 'LevelNameShort', 'LevelDescription',
       'LevelEntitytype', 'LevelColor']
    for j in keyslist:
        keys.append(j)
    d_level0 = pd.read_excel(open('assets/Attributes/dashboard_data/cookpi_per_pi.xlsx', 'rb'),
              sheet_name=keyslist[0].split('_')[0])
    d_level0 = d_level0.rename(columns={c: c+'_0' for c in d_level0.columns if c in cols})
    d_level0[d_level0.columns[0]]=d_level0[d_level0.columns[0]].astype(np.int64)
    KPIFrameworkl0.rename(columns=sheet, inplace = True)  
    df_list_l0 = [KPIFrameworkl0, d_kpi, d_level0]
    dfl0 = df_list_l0[0]
    for i, x in zip(df_list_l0[1:], range(len(keys))):
        dfl0 = dfl0.merge(i, how='left', on=keys[x])#,suffixes=(f'', f'_{x-1}')

    KPIFrameworkl0.rename(columns=sheetchangeback, inplace = True) 
    dfl0.rename(columns=sheetchangeback, inplace = True)  

    dfl0["Period_int"] = pd.to_datetime(dfl0["Period_int"])
    dfl02.append(dfl0)
    dfl0Compare2.append(dfl0)
    if 'd_level1_id' not in cookpi_attributes['Level_ID_present'].unique().tolist():
        continue
    
    sheettmpl1 = cookpi_attributes[(cookpi_attributes.Level_ID_present =="d_level1_id")]
    sheetl1 = dict(sheettmpl1.set_index('Level_ID_present')['Join_ID'].to_dict())
    sheetchangebackl1 = dict(sheettmpl1.set_index('Join_ID')['Level_ID_present'].to_dict()) 
    keyslistl1 = list(sheetl1.values())
    for t in keyslistl1:
        keys.append(t)
    d_level1 = pd.read_excel(open('assets/Attributes/dashboard_data/cookpi_per_pi.xlsx', 'rb'),
              sheet_name=keyslistl1[0].split('_')[0])
    d_level1 = d_level1.rename(columns={c: c+'_1' for c in d_level1.columns if c in cols})
    d_level1[d_level1.columns[0]]=d_level1[d_level1.columns[0]].astype(np.int64)
    df_list_l1 = [KPIFrameworkl1, d_kpi, d_level0, d_level1]

    KPIFrameworkl1.rename(columns=sheet, inplace = True)  
    KPIFrameworkl1.rename(columns=sheetl1, inplace = True)  
    dfl1 = df_list_l1[0]
    for i, x in zip(df_list_l1[1:], range(len(keys))):
        dfl1 = dfl1.merge(i, how='left', on=keys[x])#,suffixes=(f'_{x-2}', f'_{x-1}')
    
    KPIFrameworkl1.rename(columns=sheetchangeback, inplace = True) 
    KPIFrameworkl1.rename(columns=sheetchangebackl1, inplace = True) 
    dfl1.rename(columns=sheetchangeback, inplace = True) 
    dfl1.rename(columns=sheetchangebackl1, inplace = True) 
   
    dfl1["Period_int"] = pd.to_datetime(dfl1["Period_int"])
    dfl12.append(dfl1)
    dfl1Compare2.append(dfl1)
    
    if 'd_level2_id' not in cookpi_attributes['Level_ID_present'].unique().tolist():
        continue
    sheettmpl2 = cookpi_attributes[(cookpi_attributes.Level_ID_present =="d_level2_id")]
    sheetl2 = dict(sheettmpl2.set_index('Level_ID_present')['Join_ID'].to_dict())   

    sheetchangebackl2 = dict(sheettmpl2.set_index('Join_ID')['Level_ID_present'].to_dict()) 
    keyslistl2 = list(sheetl2.values())
    for b in keyslistl2:
        keys.append(b)
    d_level2 = pd.read_excel(open('assets/Attributes/dashboard_data/cookpi_per_pi.xlsx', 'rb'),
              sheet_name=keyslistl2[0].split('_')[0])
    d_level2 = d_level2.rename(columns={c: c+'_2' for c in d_level2.columns if c in cols})
    d_level2[d_level2.columns[0]]=d_level2[d_level2.columns[0]].astype(np.int64)
    df_list_l2 = [KPIFrameworkl2, d_kpi, d_level0, d_level1, d_level2]
    KPIFrameworkl2.rename(columns=sheet, inplace = True)  
    KPIFrameworkl2.rename(columns=sheetl1, inplace = True)  
    KPIFrameworkl2.rename(columns=sheetl2, inplace = True) 

    dfl2 = df_list_l2[0]
    for p, o in zip(df_list_l2[1:], range(len(keys))):
        dfl2 = dfl2.merge(p, how='left', on=keys[o])#,suffixes=(f'', f'_{o-1}')
    KPIFrameworkl2.rename(columns=sheetchangeback, inplace = True) 
    KPIFrameworkl2.rename(columns=sheetchangebackl1, inplace = True) 
    KPIFrameworkl2.rename(columns=sheetchangebackl2, inplace = True) 

    dfl2.rename(columns=sheetchangeback, inplace = True) 
    dfl2.rename(columns=sheetchangebackl1, inplace = True) 
    dfl2.rename(columns=sheetchangebackl2, inplace = True) 
   
    dfl2["Period_int"] = pd.to_datetime(dfl2["Period_int"])
    dfl22.append(dfl2)
    dfl2Compare2.append(dfl2)

    keys.clear()



if len(dfl02)!=0:
    dfl0 = pd.concat(dfl02)
    dfl0Compare = pd.concat(dfl0Compare2)
    dfl0.to_csv(r'assets/Attributes/dashboard_data/dfl0.csv', index=False)

if len(dfl12)!=0:
    dfl1 = pd.concat(dfl12)
    dfl1.to_csv(r'assets/Attributes/dashboard_data/dfl1.csv', index=False)
    dfl1Compare = pd.concat(dfl1Compare2)

if len(dfl22)!=0:
    dfl2 = pd.concat(dfl22)
    dfl2.to_csv(r'assets/Attributes/dashboard_data/dfl2.csv', index=False)
    dfl2Compare = pd.concat(dfl2Compare2)


GrainNameList = dfl0['Grain'].unique()
Level1NameList = dfl1['LevelName_1'].unique()
Level2NameList = dfl2['LevelName_2'].unique().tolist()

Level0Name = dfl0[['LevelEntitytype_0','LevelName_0','LevelColor_0','KPIName']]
Level1Name = dfl1[['LevelEntitytype_1','LevelName_1','LevelColor_1','KPIName']]
Level2Name = dfl2[['LevelEntitytype_2','LevelName_2','LevelColor_2','KPIName']]
Level0Name = Level0Name.drop_duplicates()
Level1Name = Level1Name.drop_duplicates()
Level2Name = Level2Name.drop_duplicates()

GrainNameListCompare = dfl0Compare['Grain'].unique()
Level1NameListCompare = dfl1Compare['LevelName_1'].unique()
Level2NameListCompare = dfl2['LevelName_2'].unique().tolist()


Level0NameColor = dict(Level0Name.set_index('LevelName_0')['LevelColor_0'].to_dict())
Level1NameColor = dict(Level1Name.set_index('LevelName_1')['LevelColor_1'].to_dict())
Level2NameColor = dict(Level2Name.set_index('LevelName_2')['LevelColor_2'].to_dict())
Level0attr = dict(Level0Name.set_index('KPIName')['LevelEntitytype_0'].to_dict())
Level1attr = dict(Level1Name.set_index('KPIName')['LevelEntitytype_1'].to_dict())
Level2attr = dict(Level2Name.set_index('KPIName')['LevelEntitytype_2'].to_dict())


KPINameListCompare = d_kpi['KPIName'].unique()
KPINameColor = dict(d_kpi.set_index('d_kpi_id')['KPIName'].to_dict())
KPINameList =  d_kpi['KPIName'].unique()
KPIGroupList = d_kpi['KPIGroup'].unique()
HigherIs = dict(d_kpi.set_index('KPIName')['HigherIs(1=positive)'].to_dict())
KPINotation = dict(d_kpi.set_index('KPIName')['Notation'].to_dict())
KPICalculation = dict(d_kpi.set_index('KPIName')['Calculation'].to_dict())
KPICum = dict(d_kpi.set_index('KPIName')['IsCum'].to_dict())
KPIColor = dict(d_kpi.set_index('KPIName')['kpicolor'].to_dict())
visual = dict(d_kpi.set_index('KPIName')['visual'].to_dict())




KPIGroupImage = dict(d_kpi.set_index('KPIGroup')['GroupImage'].to_dict())
GroupImage = d_kpi['GroupImage'].unique()
KPICountPerGroup = dict(d_kpi.groupby('KPIGroup')['KPIName'].count().to_dict())
KPILevelCountList = dict(d_kpi.set_index('KPIName')['kpilevelcount'].to_dict())

columnsdftotal = KPIFramework.columns.tolist()
columnsdftotal.remove('d_level0_id')
columnsdftotal.remove('d_level1_id')
columnsdftotal.remove('d_level2_id')
columnsdftotal.remove('Numerator')
columnsdftotal.remove('Denominator')
columnsdftotal.remove('Numerator_LP')
columnsdftotal.remove('Denominator_LP')
columnsdftotal.remove('Period_int_lp')

kpicountout = [len(KPINameList)]
kpigroupcountout = [len(KPIGroupList)]

KPIattributes =[]

pd.set_option('display.expand_frame_repr', False)

template_theme1 = "stylesheet.css"
template_theme2 = "stylesheet2.css"

css_directory = os.getcwd()
stylesheets = ['stylesheet.css']
static_css_route = '/static/'

external_stylesheets = [
{
    'href': 'https://fonts.googleapis.com/icon?family=Material+Icons',
    'rel': 'stylesheet',
},
]

app = dash.Dash(__name__,external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)

server = app.server

app.css.config.serve_locally = True

bgcolor = "#f3f3f1"
template = {"layout": {"paper_bgcolor": bgcolor, "plot_bgcolor": bgcolor}}
row_heights = [150, 500, 300]


def blank_fig(height):
    """
    Build blank figure with the requested height
    """
    return {
        "data": [],
        "layout": {
            "height": height,
            "template": template,
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
        },
    }

KPIdropdown = html.Div([
    dbc.Select(
        id="KPISelect",
        options=[{'label': i, 'value': i} for i in KPINameList],
        value=KPINameList[0]
  ),
],
    className="pretty_container",
    id="KPIContainer",
)

KPIGroupdropdown = html.Div([
    dcc.Dropdown(
        id="KPIGroupSelect",
        value=KPIGroupList[0],
        multi=True,
        options=[{'label': i, 'value': i} for i in KPIGroupList],
        
  ),
],
    className="pretty_container",
    id="KPIGroupContainer",
)

mainlogo =   html.Div(html.Img(#src='data:image/png;base64,{}'.format(base64.b64encode(open('assets/attributes/Images/coa.png', 'rb').read()).decode())
            id='TopImage'
            ),
)

d_kpi_sorting = d_kpi

KPISorting = dict(d_kpi_sorting.set_index('Sorting')['KPIName'].to_dict())

Radiograin = html.Div([
  dbc.RadioItems(
      id="GrainSelect",
      options=[{'label': i, 'value': i} for i in GrainNameList],
      value="M",
      labelClassName="date-group-labels",
      labelCheckedClassName="date-group-labels-checked",
      inline=True
  )
 ],
),

Level1DD = html.Div([dcc.Dropdown(
    id="Level1NameSelect",
    options=[{'label': i, 'value': i} for i in Level1NameList],
    multi=True,
    optionHeight=1,
    placeholder="Select a value",
    value=Level1NameList,
),
],id="Level1DD"
)

Level2DD = html.Div([dcc.Dropdown(
        id="Level2NameSelect",
        options=[{'label': str(i), 'value': str(i)} for i in Level2NameList],
        multi=True,
        placeholder="Select a value",
        value=Level2NameList,
),
],id="Level2DD"
)

carousellist = []
carousellist3 = []

for i in range(len(KPINameList)):
    numbertmp= i+1
    number=str(numbertmp)
    carousellist.append(
    f"""html.Div(id='carddiv{number}')"""
    ) 
carousellist2=','.join(carousellist)
carousellist3.append(carousellist2)

kpigrouplistinput =[]
kpigrouplistinput3 =[]

kpigroupstyleoutput =[]
kpigroupstyleoutput3 =[]

kpigrouplistinput.append(
        f"""Input('kpigroup0', 'n_clicks')"""
)

kpigroupstyleoutput.append(
        f"""Output('kpigroup0', 'style')"""
)

for i in range(len(KPIGroupList)):
    numbertmp= i
    numberidtmp= i+1
    number=str(numbertmp)
    numberid=str(numberidtmp)
    kpigrouplistinput.append(
        f"""Input('kpigroup{numberidtmp}','n_clicks')"""
    )
    kpigroupstyleoutput.append(
        f"""Output('kpigroup{numberidtmp}','style')"""
    )

kpigrouplistinput2=','.join(kpigrouplistinput)
kpigrouplistinput3.append(kpigrouplistinput2)

kpigroupstyleoutput2=','.join(kpigroupstyleoutput)
kpigroupstyleoutput3.append(kpigroupstyleoutput2)

carddivnclicks=[]
carddivnclicks3= []

carddivnclicks.append(
        f"""Input("KPIGroupSelect","value")"""
    )
for i in range(kpicountout[0]):
    numbertmp=i
    numberidtmp= i+1
    number=str(numbertmp)
    numberid=str(numberidtmp)
    carddivnclicks.append(
        f"""Input("carddiv{numberidtmp}","n_clicks")"""
    )

carddivnclicks2=','.join(carddivnclicks)
carddivnclicks3.append(carddivnclicks2)


carddivstyle = []
carddivstyle3 =[]
carddivstylereturn = []
carddivstylereturn3 = []

for i in range(kpicountout[0]):
        numbertmp= i
        numberidtmp= i+1
        number=str(numbertmp)
        numberid=str(numberidtmp)
        carddivstyle.append(
            f"""Output('carddiv{numberidtmp}', 'style')"""
        )
        carddivstylereturn.append(f"""cardstyle[{numbertmp}]""")

carddivstyle2= ','.join(carddivstyle)
carddivstyle3.append(carddivstyle2)
carddivstylereturn2= ','.join(carddivstylereturn)
carddivstylereturn3.append(carddivstylereturn2)

KPIGroup =[]

@app.callback([
             Output("KPIGroupSelect", 'value'),
             ],
            eval(kpigrouplistinput3[0])
            )
def KPIgrouplighter(*args):
    print('execute KPIgrouplighter')
    kpicountout.clear() 
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    KPIGroupList = d_kpi['KPIGroup'].unique().tolist()
    if changed_id =='kpigroup0.n_clicks':
        KPIGrouptmp1 = []
        for i in range(len(KPIGroupList)):
            KPIGrouptmp1.append(KPIGroupList[i])
        KPIGroup.append(KPIGrouptmp1)
        kpicountout.append(len(KPINameList))
    elif changed_id[0:8] == 'kpigroup':
        listnumber = int(int(changed_id[8])-1)
        KPIGrouptmp2 = []
        KPIGrouptmp2.append(KPIGroupList[listnumber])
        KPIGroup.append(KPIGrouptmp2)
        kpicountout.append(KPICountPerGroup[KPIGroupList[listnumber]])
    if not KPIGroup:
        print('listisempty')
        KPIGrouptmp3 = []
        for i in range(len(KPIGroupList)):
            KPIGrouptmp3.append(KPIGroupList[i])
        KPIGroup.append(KPIGrouptmp3)
        kpicountout.append(len(KPINameList))
    KPIGroup2 = KPIGroup[-1]
    kpigrouparray = np.asarray(KPIGroup) 
    carddivnclicks.append(
        f"""Input("KPIGroupSelect","value")"""
    )
    for i in range(kpicountout[0]):
        numbertmp= i
        numberidtmp= i+1
        number=str(numbertmp)
        numberid=str(numberidtmp)
        carddivnclicks.append(
            f"""Input("carddiv{numberidtmp}","n_clicks")"""
        )
    carddivnclicks.clear()
    carddivnclicks3.clear()
    carddivnclicks2=','.join(carddivnclicks)
    carddivnclicks3.append(carddivnclicks2)
    carddivstyle.clear()
    carddivstyle3.clear()
    carddivstylereturn.clear()
    carddivstylereturn3.clear()
    for i in range(kpicountout[0]):
        numbertmp= i
        numberidtmp= i+1
        number=str(numbertmp)
        numberid=str(numberidtmp)
        carddivstyle.append(
            f"""Output('carddiv{numberidtmp}', 'style')"""
        )
        carddivstylereturn.append(f"""cardstyle[{numbertmp}]""")
    carddivstyle2= ','.join(carddivstyle)
    carddivstyle3.append(carddivstyle2)
    carddivstylereturn2= ','.join(carddivstylereturn)
    carddivstylereturn3.append(carddivstylereturn2)
    return [KPIGroup2]

#@app.callback([
#        Output('KPISelect', 'options'),
#       # Output('kpigroup0', 'style'),
#        ],
#     Input("KPIGroupSelect", "value"),
#    # eval(kpigrouplistinput3[0]),
#)
#
#def update_KPI_Options(KPIGroupSelect):#,*args
#    print('execute update_KPI_Options')
#    dff = d_kpi[
#        (d_kpi["KPIGroup"].isin(KPIGroupSelect))
#    ]
#    KPINameListOptions = dff['KPIName'].unique()
#    options = [{'label': i, 'value': i} for i in KPINameListOptions],
#    return options

kpi =[]
KPSelectInputList = eval(carddivnclicks3[0]+','+kpigrouplistinput3[0])

@app.callback([
    Output('KPISelect', 'value'),
    ],
    eval(carddivnclicks3[0]+','+kpigrouplistinput3[0])
)

def update_df_KPIGroup(KPIGroupSelect,*args): 
    print('execute update_df_KPIGroup')    
    tmpchangedlist=dash.callback_context.triggered
    tmpchangedlist2 = [item for item in tmpchangedlist if item['value'] is not None]
    if not tmpchangedlist2:
        changed_id ='tmp'
    else:
        changed_id = [p['prop_id'] for p in tmpchangedlist2][0].split('.')[0]
    #changed_id2 = [p['prop_id'] for p in dash.callback_context.triggered][0]
    #changed_id3 = ctx.triggered#[0]['prop_id'].split('.')[0]
  #  print(changed_id3)
    dffKPISelect = d_kpi[
        (d_kpi["KPIGroup"].isin(KPIGroupSelect))
    ]
    dffKPISelect.sort_values(by=['Sorting'])
    KPINameListi = dffKPISelect['KPIName'].unique()
    if 'carddiv' in changed_id[0:7]:
        listnumber = int(int(changed_id[7:])-1)
        kpi.append(KPINameListi[listnumber])
        carddivselected = changed_id[0:8]
    elif 'kpigroup' in changed_id[0:8]:
        kpi.append(KPINameListi[0])
    if not kpi:
        kpi.append(KPINameListi[0])
    return [kpi[-1]]

"""
@app.callback(
    eval(kpigroupstyleoutput3[0])
    ,
    Input('KPIGroupSelect', 'value'),
)

def update_df_KPIGroup(KPIGroupSelect,*args): 
    print('execute update_df_KPIGroup')
    
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    style = []
    numberofstyles = []
    if 'kpigroup' in changed_id[0:8]:
        for i,kpigroup in enumerate(KPIGroupList):
            numberofstyles.append(style[i])
            style.append({'color':buttonlogocolor, 'background-color': buttoncolor})
    else:
        for i,kpigroup in enumerate(KPIGroupList):
            numberofstyles.append(style[i])
            style.append({'color':buttonlogocolor, 'background-color': buttoncolor})

    dff = d_kpi[
        (d_kpi["KPIGroup"].isin(KPIGroupSelect))
    ]
    dff.sort_values(by=['Sorting'])
    KPINameListi = dff['KPIName'].unique()
    kpigroupbuttonstyle = []
    color1 = {'color':buttonlogocolor, 'background-color': buttoncolor}
    color2 = {'color':buttonlogocolor, 'background-color': buttoncolor}
    color3 = {}
    color4 = {}
    kpi =[]
    kpi.clear()
    print(numberofstyles)
    return numberofstyles
""" 

KPIdropdownCompare = html.Div([
    dbc.Select(
        id="KPISelectCompare",
        options=[{'label': i, 'value': i} for i in KPINameListCompare],
        value=KPINameListCompare[0],
    ),
],
    className="pretty_container",
   # style={"margin": "0px","padding-right":"0px","border-bottom-right-radius":"0px"},
    id="KPIContainerCompare",
)

Perioddropdown = html.Div([
    dcc.Dropdown(
        id="Perioddropdown",
       # value="2019-05-01",
        multi=True,
    ),
],
    className="pretty_container",
)

navbarlist =[]
navbarlist.append(
        f"""html.Li(html.A([
                html.I('category',className='material-icons icon'),
                html.Span('All categories',className='text nav-text')],href='#',id='kpigroup0')
                ,className='nav-link')"""
)

for i in range(kpigroupcountout[0]):
    numbertmp= i
    numberidtmp= i+1
    GroupImage2 = GroupImage[numbertmp]
    KPIGroupList2 = KPIGroupList[numbertmp]
    number=str(numbertmp)
    numberid=str(numberidtmp)
    navbarlist.append(
        f"""html.Li(html.A([
                html.I('{GroupImage2}',className='material-icons icon'),
                html.Span('{KPIGroupList2}',className='text nav-text')],href='#',id='kpigroup{numberidtmp}')
                ,className='nav-link')"""
    )
navbarlist2=','.join(navbarlist)

navbar = html.Nav([html.Header([
                    html.Div([
#                        html.Span(
#                            html.Img(src="https://cdn0.iconfinder.com/data/icons/social-media-2091/100/social-32-512.png",alt=''),
#                        className='image'),
                        html.Div(
                            Radiograin,className="col-sm-12 col-md-12 col-lg-12 col-xl-12 text logo-text"
                        )
                    ],className="image-text"),
                    html.I("chevron_right",className='material-icons toggle',id='Opennavbar')
                    ]),
                    html.Div([
                        html.Div([
                          html.Div(html.Span("Performace category",className='text nav-text')),
                          html.Ul(eval(navbarlist2)
                            ,className='menu-links'
                            )
                        ],className='menu'
                    ),
                    html.Div([
                     html.Div([
                          html.Div(html.Span("Performace view",className='text nav-text')),
                          html.Ul([
                            html.Li(html.A(
                                [html.I("lan",className='material-icons icon'),
                                 html.Span("Drill down",className='text nav-text')
                                ],href='/drilldown',id='NavItem1'
                                ),className='nav-link')
                            ,
                            html.Li(html.A(
                                [html.I("balance",className='material-icons icon'),
                                 html.Span("Compare",className='text nav-text')
                                ],href='/compare',id='NavItem2'
                                ),className='nav-link'
                            ),
                            html.Li(html.A(
                                [html.I("bolt",className='material-icons icon'),
                                html.Span("Predict",className='text nav-text')
                                ],href='/predict',id='NavItem3'
                                ),className='nav-link'
                            ),
                    ],className='menu-links'
                            ),
                    ],className='menu'),
                    ])
                    ],className='menu-bar'),  
                    ],className="sidebar close",id='nav'),


Totaalaggregaatswitch = html.Div([
    html.Div('Compare with total ',className='h6'),
    daq.BooleanSwitch(
        id='Totaalswitch',
        on=False,
        color="#01002a",
        label="Dark",
        labelPosition="left",
    )
])

CumulativeSwitch = html.Div([
    html.Div('Cumulative ',className='h6'),
    daq.BooleanSwitch(
        id='CumulativeSwitch',
        on=False,
        color="#01002a",
        label="Dark",
        labelPosition="left",
    )
])

TargetSwitch = html.Div([
    html.Div('Target ',className='h6'),
    daq.BooleanSwitch(
        id='TargetSwitch',
        on=False,
        color="#01002a",
        label="Dark",
        labelPosition="left",
    )
])

PercentageTotalSwitch = html.Div([
    html.Div('Percentage of total ',className='h6'),
    daq.BooleanSwitch(
        id='PercentageTotalSwitch',
        on=False,
        color="#01002a",
        label="Dark",
        labelPosition="left",
    )
])

ShowValueSwitch = html.Div([
    html.Div('Show values',className='h6'),
    daq.BooleanSwitch(
        id='ShowValueSwitch',
        on=False,
        color="#01002a",
        label="Dark",
        labelPosition="left",
    )
])


fade = html.Div([
        dbc.Button(children=[
            html.I("compare",className="material-icons md-48"),
            " Filters"
        ], id="fade-transition-button",color='info'),
        dbc.Collapse(
        dbc.Card(
        dbc.CardBody(
            [html.Div(KPIGroupdropdown,
                        id='KPIGroup',
                        style={'display':'none'}),
                html.Div(KPIdropdown,
                        id='KPI'),
            ]
        ),className='pretty_bigtab'
        ),
        id="fade-transition",
        style={"transition": "opacity 100ms ease"}
)
],
)

@app.callback(
    Output("fade-transition", "is_open"),
    [Input("fade-transition-button", "n_clicks")],
    [State("fade-transition", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        # Button has never been clicked
        return not is_open
    return is_open
    


def linesormarkers(Grain):
    if Grain == 'D':
        return 'lines'
    elif    Grain == 'M':     
        return 'lines'
    else:
        return 'lines+markers'

def CalculationLogicOveral(Calculation):
    if Calculation == 2:
        CalculationString = "i / j"
        return CalculationString
    elif Calculation == 1:
        CalculationString = "i"
        return CalculationString

def CalculationLogic0Cum(Calculation):
    if Calculation == 2:
        CalculationString = "df_by_Level0Name.NumeratorCum / df_by_Level0Name.DenominatorCum"
        return CalculationString
    elif Calculation == 1:
        CalculationString = "df_by_Level0Name.NumeratorCum"
        return CalculationString

def CalculationLogic1Cum(Calculation):
    if Calculation == 2:
        CalculationString = "df_by_Level1Name.NumeratorCum / df_by_Level1Name.DenominatorCum"
        return CalculationString
    elif Calculation == 1:
        CalculationString = "df_by_Level1Name.NumeratorCum"
        return CalculationString

def CalculationLogic2Cum(Calculation):
    if Calculation == 2:
        CalculationString = "df_by_Level2Name.NumeratorCum / df_by_Level2Name.DenominatorCum"
        return CalculationString
    elif Calculation == 1:
        CalculationString = "df_by_Level2Name.NumeratorCum"
        return CalculationString

def CalculationLogic0(Calculation):
    if Calculation == 2:
        CalculationString = "df_by_Level0Name.Numerator / df_by_Level0Name.Denominator"
        return CalculationString
    elif Calculation == 1:
        CalculationString = "df_by_Level0Name.Numerator"
        return CalculationString

def CalculationLogic0Relatief(Calculation):
    if Calculation == 2:
        CalculationString = "df_by_Level0Name.Numerator / df_by_Level0Name.Denominator"
        return CalculationString
    elif Calculation == 1:
        CalculationString = "df_by_Level0Name.Numerator" - "df_by_Level0Name.Numerator_LP"
        return CalculationString

def CalculationLogic2(Calculation):
    if Calculation == 2:
        CalculationString = "df_by_Level2Name.Numerator / df_by_Level2Name.Denominator"
        return CalculationString
    elif Calculation == 1:
        CalculationString = "df_by_Level2Name.Numerator"
        return CalculationString


def CalculationLogic1(Calculation):
    if Calculation == 2:
        CalculationString = "df_by_Level1Name.Numerator / df_by_Level1Name.Denominator"
        return CalculationString
    elif Calculation == 1:
        CalculationString = "df_by_Level1Name.Numerator" #"(df_by_Level1Name.Numerator - df_by_Level1Name.Numerator_LP) / df_by_Level1Name.Numerator"
        return CalculationString

def CalculationLogicTotal(Calculation):
    if Calculation == 2:
        CalculationString = "dff.Numerator / dff.Denominator"
        return CalculationString
    elif Calculation == 1:
        CalculationString = "dff.Numerator"
        return CalculationString

def CalculationLogicCompKPI(Calculation):
    if Calculation == 2:
        CalculationString = "df_filtered_kpi.Numerator / df_filtered_kpi.Denominator"
        return CalculationString
    elif Calculation == 1:
        CalculationString = "df_filtered_kpi.Numerator"
        return CalculationString

def CalculationLogicTotalCompare(Calculation):
    if Calculation == 2:
        CalculationString = "dffcomp.Numerator / dffcomp.Denominator"
        return CalculationString
    elif Calculation == 1:
        CalculationString = "dffcomp.Numerator"
        return CalculationString




def DBColorDEF(DBColor):
    if DBColor == 'False':
        ColorHex = ['"#144a68"', '"#c1c1c1"','"#0c2a4d"']
        return ColorHex
    elif DBColor == 'True': #707975
    #    ColorHex = ['"#144a68"', '"#c1c1c1"','"#0c2a4d"']
        ColorHex = ['"#00394a"', '"#c2c0b4"','"#164452"']
        return ColorHex#c2c0b4 001f3d

def PercentageTotalSwitchDEF(PercentageSwitchie):
    if PercentageSwitchie == 'True':
        list2 = "'percent'"
        return list2
    elif PercentageSwitchie == 'False':
        list2 = "''"
        return list2

def Totaalloop(Totaalloop):
    if Totaalloop == 'True':
        list = '[tracestotal,traces2]' #'tracestotal, traces2'
        return list
    elif Totaalloop == 'False': #707975
    #    ColorHex = ['"#144a68"', '"#c1c1c1"','"#0c2a4d"']
        list = '[traces2]'
        return list #c2c0b4 001f3d

def Cumloop0(Cumloop):
    if Cumloop == 'False':
        list = ['df_by_Level0Name','CalculationLogic0(Calculation)']
        return list
    elif Cumloop == 'True':
        list = ['df_by_Level0Name','CalculationLogic0Cum(Calculation)']
        return list #c2c0b4 001f3d

def Cumloop1(Cumloop):
    if Cumloop == 'False':
        list = ['df_by_Level1Name','CalculationLogic1(Calculation)']
        return list
    elif Cumloop == 'True':
        list = ['df_by_Level1Name','CalculationLogic1Cum(Calculation)']
        return list #c2c0b4 001f3d

def Cumloop2(Cumloop):
    if Cumloop == 'False':
        list = ['df_by_Level2Name','CalculationLogic2(Calculation)']
        return list
    elif Cumloop == 'True':
        list = ['df_by_Level2Name','CalculationLogic2Cum(Calculation)']
        return list #c2c0b4 001f3d


def KPISelectedStyle(kpi):
    Notation = KPINotation[kpi]
    if Notation == '%':
        Notation = ['".1%"']
        return Notation
    elif Notation == '#':
        Notation = ['".2s"']
     #   Notation = ['"^,"']
        return Notation
    elif Notation == '$':
        Notation = ['"$.2s"']
        return Notation

def KPISelectedStylePython(kpi):
     Notation = KPINotation[kpi]
     if Notation == '%':
         Notation = ["'{:2.2%}'"]
         return Notation
     elif Notation == '#':
         Notation = ["'{:.0f}'"]
         #   Notation = ['"^,"']
         return Notation
     elif Notation == '$':
         Notation = ["'${:,.2f}'"]
         return Notation

def KPISelectedStyleFloat(kpi):
    Notation = KPINotation[kpi]
    if Notation == '%':
        Notation = ['"{:.2%}"']
        return Notation
    elif Notation == '#':
        Notation = ['".2s"']
     #   Notation = ['"^,"']
        return Notation
    elif Notation == '$':
        Notation = ['"$.2s"']
        return Notation

def CalculationDEF(kpi):
    Calculation = KPICalculation[kpi]
    return Calculation

def NumaggregateDEF(kpi):
    Calculation = KPINumAgg[kpi]
    return Calculation

def DenomaggregateDEF(kpi):
    Calculation = KPIDenomAgg[kpi]
    return Calculation

def IsCum(kpi):
    IsCum = KPICum[kpi]
    return IsCum

def kpicolorDEF(kpi):
    Calculation = KPIColor[kpi]
    return Calculation

def visualDEF(kpi):
    visuall = visual[kpi]
    return visuall

def kpilevel0attrDEF(kpi):
    kpilevel0attr = Level0attr[kpi]
    return kpilevel0attr

def kpilevel1attrDEF(kpi):
    kpilevel1attr = Level1attr[kpi]
    return kpilevel1attr

def kpilevel2attrDEF(kpi):
    kpilevel2attr = Level2attr[kpi]
    return kpilevel2attr


def update_filter_l2(dfl2, GrainSelect, KPISelect,Level1NameSelect, Level2NameSelect):
    dff = dfl2[
        (dfl2["Grain"] == GrainSelect)
        & (dfl2["KPIName"] == KPISelect)
        & (dfl2["LevelName_1"].isin(Level1NameSelect))
        & dfl2["LevelName_2"].isin(Level2NameSelect)
        ]
    return dff

def update_filter_compare_l2(dfl2Compare, GrainSelect, KPISelectCompare,Level1NameSelect, Level2NameSelect):
    dffcomp = dfl2Compare[
        (dfl2Compare["Grain"] == GrainSelect)
        & (dfl2Compare["KPIName"] == KPISelectCompare)
        & (dfl2Compare["LevelName_1"].isin(Level1NameSelect))
        & dfl2Compare["LevelName_2"].isin(Level2NameSelect)
        ]
    return dffcomp

def update_filter_compare_l1(dfl1Compare, GrainSelect, KPISelectCompare,Level1NameSelect):
    dffcomp = dfl1Compare[
        (dfl1Compare["Grain"] == GrainSelect)
        & (dfl1Compare["KPIName"] == KPISelectCompare)
        & (dfl1Compare["LevelName_1"].isin(Level1NameSelect))
        ]
    return dffcomp

def update_filter_compare_l0(dfl0Compare, GrainSelect, KPISelectCompare):
    dffcomp = dfl0Compare[
        (dfl0Compare["Grain"] == GrainSelect)
        & (dfl0Compare["KPIName"] == KPISelectCompare)
        ]
    return dffcomp

def update_filter_nokpi(dfl0, GrainSelect,KPIGroup): 
    dff = dfl0[
        (dfl0["Grain"] == GrainSelect)
         & (dfl0["KPIGroup"].isin(KPIGroup)) 
        ]
    return dff

def update_filter_l0(dfl0, GrainSelect, KPISelect):
    dff = dfl0[
        (dfl0["Grain"] == GrainSelect)
        & (dfl0["KPIName"] == KPISelect)
        ]
    return dff

def update_filter_l1(dfl1, GrainSelect, KPISelect,Level1NameSelect):
    dff = dfl1[
        (dfl1["Grain"] == GrainSelect)
        & (dfl1["KPIName"] == KPISelect)
        & (dfl1["LevelName_1"].isin(Level1NameSelect))
        ]
    return dff



def update_KPIDescription(KPISelect):

    KPIValue = KPISelectedStyle(KPISelect)
    return KPIValue



@app.callback(
    dash.dependencies.Output('Totaalswitch', 'label'),
    [dash.dependencies.Input('Totaalswitch', 'on')])

def update_output(on):
    return format(on)


@app.callback(
    dash.dependencies.Output('CumulativeSwitch', 'label'),
    [dash.dependencies.Input('CumulativeSwitch', 'on')])

def update_output(on):
    return format(on)

@app.callback(
    dash.dependencies.Output('TargetSwitch', 'label'),
    [dash.dependencies.Input('TargetSwitch', 'on')])

def update_output(on):
    return format(on)


@app.callback(
    dash.dependencies.Output('PercentageTotalSwitch', 'label'),
    [dash.dependencies.Input('PercentageTotalSwitch', 'on')])

def update_output(on):
    return format(on)

@app.callback(
    dash.dependencies.Output('ShowValueSwitch', 'label'),
    [dash.dependencies.Input('ShowValueSwitch', 'on')])

def update_output(on):
    return format(on)


@app.callback([Output('Level1DD','style'),
              Output('Level2DD','style')],
             [Input('tabsdrilldown','active_tab'),
              #Input('Tab1',component_property='disabled'),
              #Input('Tab2',component_property='disabled')
              ])
def definefilterlevel(tabsdrilldown):
    if tabsdrilldown == 'tab-0':
        msg0 = {'display': 'block'}
        msg1 = {'display': 'none'}
        msg2 = {'display': 'none'}
    elif tabsdrilldown == 'tab-1':
        msg0 = {'display': 'none'}
        msg1 = {'display': 'block'}
        msg2 = {'display': 'none'}
    elif tabsdrilldown == 'tab-2':
        msg0 = {'display': 'none','overflow':'hidden'}
        msg1 = {'display': 'none','overflow':'hidden'}
        msg2 = {'display': 'block'}
    else:
        msg0 = {'display': 'block'}
        msg1 = {'display': 'none'}
        msg2 = {'display': 'none'}
    return msg1,msg2


######################################################################################################################
######################################################################################################################
################################################----tabs aanmaken----###############################################
######################################################################################################################
######################################################################################################################


tabs = html.Div(
    dbc.Tabs(children=
    [
    dbc.Tab(children=[dbc.CardBody(
        dbc.Row([
        dbc.Col(dbc.Spinner(children=[#,spinner_class_name='loading'
            dcc.Graph(id='graphlevel0',
                      config=dict(
                        modeBarButtonsToAdd =  ['customButton'],
                        modeBarButtonsToRemove = ['pan','lasso2d','select','zoom2d','zoomIn','zoomOut','hoverCompareCartesian','logo','autoScale'],
                        displaylogo = False,
                        scrollZoom = True,
                        toImageButtonOptions = dict(
                            width =550,
                            height = 300,
                            format = 'png',
                            scale = 10,
                            filename = 'Plotlygraph'),
                      ),
                      className="row-cols-sm-12 row-cols-md-12 row-cols-lg-12 row-cols-xl-12 pretty_graph"
                      )],spinnerClassName="loader1"),className="col-12 col-sm-12 col-md-12 col-lg-8 col-xl-8 empty_tab"
        ),
        dbc.Col(html.Div([
            html.I("delete_sweep",n_clicks=0,id='sweepl0',className="material-icons md-48",style={'position':'absolute','top':'1px','right':'12px','z-index': '1'}),
            dbc.Spinner(children=[dcc.Graph(id='graph-level0compare',
                      config=dict(
                          modeBarButtonsToAdd=['customButton'],
                          modeBarButtonsToRemove=['pan', 'lasso2d', 'select', 'zoom2d', 'zoomIn', 'zoomOut',
                                                  'hoverCompareCartesian', 'logo', 'autoScale'],
                          displaylogo=False,
                          scrollZoom=True,
                          toImageButtonOptions=dict(
                              width=500,
                              height=300,
                              format='png',
                              scale=10,
                              filename='Plotlygraph'),
                      )
                      )])
        ],className="col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12 pretty_graph2"
        ),className="col-12 col-sm-12 col-md-12 col-lg-4 col-xl-4 empty_tab2"
        )
        ],className="row-cols-sm-12 row-cols-md-12 row-cols-lg-12 row-cols-xl-12"
        ),className="row-cols-sm-12 row-cols-md-12 row-cols-lg-11 row-cols-xl-11 pretty_tab"
    )]
,id="Tab0drilldown"),
    dbc.Tab(children=[dbc.CardBody(
        dbc.Row([
        dbc.Col(dbc.Spinner(children=[
            dcc.Graph(id='graphoveralltime',
                      config=dict(
                          modeBarButtonsToAdd=['customButton'],
                          modeBarButtonsToRemove=['pan', 'lasso2d', 'select', 'zoom2d', 'zoomIn', 'zoomOut',
                                                  'hoverCompareCartesian', 'logo', 'autoScale'],
                          displaylogo=False,
                          scrollZoom=True,
                          toImageButtonOptions=dict(
                              width=550,
                              height=300,
                              format='png',
                              scale=10,
                              filename='Plotlygraph'),
                      ),
                      className="row-cols-sm-12 row-cols-md-12 row-cols-lg-12 row-cols-xl-12 pretty_graph"
                      )],spinnerClassName="loader1"),className="col-12 col-sm-12 col-md-12 col-lg-8 col-xl-8 empty_tab"
        ),
        dbc.Col(html.Div([
            html.I("delete_sweep",n_clicks=0,id='sweepl1',className="material-icons md-48",style={'position':'absolute','top':'1px','right':'12px','z-index': '1'}),
            dbc.Spinner(children=[dcc.Graph(id='graph-level1compare',
                      config=dict(
                          modeBarButtonsToAdd=['customButton'],
                          modeBarButtonsToRemove=['pan', 'lasso2d', 'select', 'zoom2d', 'zoomIn', 'zoomOut',
                                                  'hoverCompareCartesian', 'logo', 'autoScale'],
                          displaylogo=False,
                          scrollZoom=True,
                          toImageButtonOptions=dict(
                              width=500,
                              height=300,
                              format='png',
                              scale=10,
                              filename='Plotlygraph'),
                      )
                      )])
        ],className="col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12 pretty_graph2"
        ),className="col-12 col-sm-12 col-md-12 col-lg-4 col-xl-4 empty_tab2"
        )
        ],className="row-cols-sm-12 row-cols-md-12 row-cols-lg-12 row-cols-xl-12"
        ),className="row-cols-sm-12 row-cols-md-12 row-cols-lg-11 row-cols-xl-11 pretty_tab"
    )
    ]
,id="Tab1drilldown"),
    dbc.Tab(children=[dbc.CardBody(
        dbc.Row([
        dbc.Col(dbc.Spinner(children=[
            dcc.Graph(id='graph-with-slider',
                      config=dict(
                          modeBarButtonsToAdd=['customButton'],
                          modeBarButtonsToRemove=['pan', 'lasso2d', 'select', 'zoom2d', 'zoomIn', 'zoomOut',
                                                  'hoverCompareCartesian', 'logo', 'autoScale'],
                          displaylogo=False,
                          scrollZoom=True,
                          toImageButtonOptions=dict(
                              width=550,
                              height=300,
                              format='png',
                              scale=10,
                              filename='Plotlygraph'),
                      ),
                      className="col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12 pretty_graph",
                      )]),className="col-12 col-sm-12 col-md-12 col-lg-8 col-xl-8 empty_tab",
        ),
        html.I("delete_sweep",n_clicks=0,id='sweepl2',className="material-icons md-48",style={'position':'absolute','top':'1px','right':'12px','z-index': '1'}),
        dbc.Col(dbc.Spinner(children=[dcc.Graph(id='graph-level2compare',
                          config=dict(
                              modeBarButtonsToAdd=['customButton'],
                              modeBarButtonsToRemove=['pan', 'lasso2d', 'select', 'zoom2d', 'zoomIn', 'zoomOut',
                                                      'hoverCompareCartesian', 'logo', 'autoScale'],
                              displaylogo=False,
                              scrollZoom=True,
                              toImageButtonOptions=dict(
                                  width=500,
                                  height=300,
                                  format='png',
                                  scale=10,
                                  filename='Plotlygraph'),
                          ),
                     className="col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12  pretty_graph2"
                    )]),className="col-12 col-sm-12 col-md-12 col-lg-4 col-xl-4 empty_tab2"
    ),
    ],className="row-cols-sm-12 row-cols-md-12 row-cols-lg-12 row-cols-xl-12"
    ),className="row-cols-sm-12 row-cols-md-12 row-cols-lg-11 row-cols-xl-11 pretty_tab"
)],id="Tab2drilldown"),
            ],id="tabsdrilldown",active_tab="tab-0")
)


tabscompare = dbc.Tabs(
    [dbc.Tab(label="Compare two",children=[dbc.CardBody(
    dbc.Row([
        dbc.Col(KPIdropdownCompare,
                id='KPICompare'),
        dbc.Col(dbc.Spinner(children=[
            dcc.Graph(id='graph-compare-kpi',
                      config={
                          'modeBarButtonsToRemove': ['pan', 'lasso2d', 'select', 'zoom2d', 'zoomIn', 'zoomOut',
                                                     'hoverCompareCartesian', 'logo', 'autoScale'],
                          'displaylogo': False,
                          'scrollZoom': True,
                      }, className="col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12 pretty_graph",
                      )]), className="col-12 col-sm-11 col-md-11 col-lg-12 col-xl-12 empty_tab2",
        ),
    ], className="row-cols-sm-12 row-cols-md-12 row-cols-lg-12 row-cols-xl-12"
    ), className="row-cols-sm-12 row-cols-md-12 row-cols-lg-12 row-cols-xl-12 pretty_tab"
    )
    ]
    ,id="Tabcompare"),
    dbc.Tab(label="Compare change",children=[dbc.CardBody(
    dbc.Row([
        #dbc.Col(KPIdropdownCompare,
        #        id='KPICompare'),
        dbc.Col(
            dbc.Spinner(children=[dcc.Graph(id='graph-compare-kpi2',
                      config={
                          'modeBarButtonsToRemove': ['pan', 'lasso2d', 'select', 'zoom2d', 'zoomIn', 'zoomOut',
                                                     'hoverCompareCartesian', 'logo', 'autoScale'],
                          'displaylogo': False,
                          'scrollZoom': True,
                      }, className="col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12 pretty_graph",
                      )]), className="col-12 col-sm-11 col-md-11 col-lg-12 col-xl-12 empty_tab2",
        ),
    ], className="row-cols-sm-12 row-cols-md-12 row-cols-lg-12 row-cols-xl-12"
    ), className="row-cols-sm-12 row-cols-md-12 row-cols-lg-12 row-cols-xl-12 pretty_tab"
    )
    ]
    ,id="Tabcompare2"),
   #  dbc.Tab(label="Tab compare 2", children=[tab1_compare]),
    ]

)

tabscontainer = html.Div(
    dbc.Tabs(children=
        [dbc.Tab(label="Tab 1", children=[tabs]),
         dbc.Tab(label="Tab 2", children=[tabscompare]),
        ]
        )
  #  )
)


######################################################################################################################
################################################----layout aanmaken----###############################################
######################################################################################################################
######################################################################################################################


app.layout = html.Div([html.I("filter_alt", id='dropdowncontrol', className="material-icons filtericon", n_clicks=0),
    dbc.Row([
        html.Div(id='output-container-date-picker-range',
                 style={'margin-top': '12px'},
                 className='h7'),
            dbc.Popover(
            dbc.PopoverBody(children=[
                dbc.Col([mainlogo],className="col-sm-12 col-md-12 col-lg-12 col-xl-12",style={"margin-bottom": '2px'}),
                dbc.Col([Level1DD],className="col-sm-12 col-md-12 col-lg-12 col-xl-12",style={"margin-bottom": '2px'}),
                dbc.Col([Level2DD],className="col-sm-12 col-md-12 col-lg-12 col-xl-12",style={"margin-bottom": '2px'}),
            ],id="dropdowns"),
            target="dropdowncontrol",
            trigger="click",
            className='popupper_filters',
            placement='top'),
      dbc.Col(fade,className="col-sm-12 col-md-12 col-lg-2 col-xl-2",style={'display': 'none'}),
       ]),
    dbc.Row([
            dbc.Col(
            [html.Div(Perioddropdown,className="col-sm-2 col-md-2 col-lg-2 col-xl-2",style={'display': 'none'}),
            html.Div(children=eval(carousellist3[0]),className="col-sm-9 col-md-9 col-lg-9 col-xl-9",style={"margin": '0 auto'},id='cardsid'),
            # html.Div(className="col-sm-9 col-md-9 col-lg-9 col-xl-9"
            #    ,style={"margin": '0 auto'},id='cardsid')
            ]),
        ]),

    dbc.Row([
            dbc.Col([
             html.I("settings_suggest",id='graphset',className="material-icons", style={'text-align': 'left !important'},n_clicks=0),
            dbc.Popover(
                [dbc.PopoverBody(children=[
                        dbc.Col([Totaalaggregaatswitch], className="col-sm-12 col-md-12 col-lg-12 col-xl-12"),
                        dbc.Col([CumulativeSwitch], className="col-sm-12 col-md-12 col-lg-12 col-xl-12"),
                        dbc.Col([TargetSwitch], className="col-sm-12 col-md-12 col-lg-12 col-xl-12"),
                        dbc.Col([PercentageTotalSwitch], className="col-sm-12 col-md-12 col-lg-12 col-xl-12"),
                        dbc.Col([ShowValueSwitch], className="col-sm-12 col-md-12 col-lg-12 col-xl-12"),
                    ], id='Graphsettingpopfooter', className='h6'),
                ],
                target="graphset",
                trigger="legacy",
                className='popupper_graphsetting',
                placement='top'
            ),
            html.Div(tabs,
                     id="tabscontainer"
                     ),
            html.Div(tabscompare,
                     id="tabscompare"
                     ),
                    ],className="col-sm-11 col-md-11 col-lg-10 col-xl-10 pretty_bigtab",style={"margin": '0 auto','margin-top':'20px'}
                    ),
            
          #  html.Div(KPI_Group,className="col-sm-11 col-md-11 col-lg-4 col-xl-3"),

    ]
    ),
    html.Div(navbar),
    html.Span(html.I(''),style={'margin-top': '5em','display': 'block'}),
    dcc.Store(id='dfl0',data=[],storage_type='memory'),
    dcc.Store(id='dfl1',data=[],storage_type='memory'),
    dcc.Store(id='dfl2',data=[],storage_type='memory'),
    dcc.Store(id='dffcomparefilter',data=[],storage_type='memory'),
    dcc.Store(id='dflcomparekpi',data=[],storage_type='memory'),
    dcc.Store(id='selectedkpigroup',data=[],storage_type='memory'),
    WindowBreakpoints(
            id="breakpoints",
            # Define the breakpoint thresholds
            widthBreakpointThresholdsPx=[800, 1200],
            # And their name, note that there is one more name than breakpoint thresholds
            widthBreakpointNames=["sm", "md", "lg"],
    ),
    
    dbc.Row([
        #html.Div([dcc.DatePickerRange(
        #            id='my-date-picker-range',
        #            min_date_allowed=date(2010, 1, 1),
        #            max_date_allowed=date(2030, 12, 31),
        #            initial_visible_month=date(2020, 1, 1),
        #            end_date=date(2022, 10, 31),
        #            style={"color": "red"}
        #         ),
                ]),
],
)

app.clientside_callback(
    """window.onload=function () {
        addListeners()
        return 0
    }""",
    Output('nav','n_clicks'),
    Input('nav','children')
)

@app.callback(
    Output('sweepl1', 'n_clicks'),
    Input('sweepl1', 'n_clicks')
)
def upon_click(n_clicks):
    if (n_clicks is None): raise PreventUpdate
    return 1


@app.callback([Output('tabscontainer', 'style'),
             Output('graph-level1compare', 'style'),
             Output('graphoveralltime', 'style'),
             Output('tabscompare', 'style'),
             Output('graph-compare-kpi', 'style'),
             Output('NavItem1', 'style'),
             Output('NavItem2', 'style'),
             Output('NavItem3', 'style'),
             Output('Tab0drilldown', 'label'),
             Output('Tab1drilldown', 'label'),
             Output('Tab2drilldown', 'label'),
             Output('Tab0drilldown', 'tab_class_name'),
             Output('Tab1drilldown', 'tab_class_name'),
             Output('Tab2drilldown', 'tab_class_name')             
             ],
             [Input('NavItem1','n_clicks'),
              Input('NavItem2','n_clicks'),
              Input('NavItem3','n_clicks'),
              Input('KPISelect','value')
              ])
def hide_graph(NavItem1,NavItem2,NavItem3,KPISelect):
    print('execute hide_graph')
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    tab_class_name=[]
    Levelattrr = []
    for i in range(3):
        if KPILevelCountList[KPISelect]>i:
            tab_class_name.append('showntab')
        else:
            tab_class_name.append('hiddentab') 
        if  tab_class_name[i]=='showntab':
            Levelattrr.append(eval(f'Level{i}attr[KPISelect]'))
        else:
            Levelattrr.append('')
    #Level0attrr ='' if not Level0attr[KPISelect] else Level0attr[KPISelect]
    #Level1attrr ='' if not Level1attr[KPISelect] else Level1attr[KPISelect]
    #Level2attrr ='' if not Level2attr[KPISelect] else Level2attr[KPISelect]

    if 'NavItem1' in changed_id:
        kpicolor = kpicolorDEF(KPISelect)
        msg = {'display': 'block'}
        msg2 = {'display':'none'}
        msg3 = {'display': 'none'}
        color1 = {'color':buttonlogocolor,'background-color':buttoncolor}
        color2 = {}
        color3 = {}
    elif 'NavItem2' in changed_id:
        msg = {'display':'none'}
        msg2 = {'display': 'block'}
        msg3 = {'display': 'none'}
        color1 = {}
        color2 = {'color':buttonlogocolor,'background-color':buttoncolor}
        color3 = {}
    elif 'NavItem3' in changed_id:
        msg = {'display': 'none'}
        msg2 = {'display': 'none'}
        msg3 = {'display': 'block'}
        color1 = {}
        color2 = {}
        color3 = {'color':buttonlogocolor,'background-color': buttoncolor}
    else:
        kpicolor = kpicolorDEF(KPISelect)
        msg = {'display': 'block'}
        msg2 = {'display': 'none'}
        msg3 = {'display': 'none'}
        color1 = {'color':buttonlogocolor, 'background-color': buttoncolor}
        color2 = {}
        color3 = {}
    return msg,msg,msg,msg2,msg2,color1,color2,color3,Levelattrr[0],Levelattrr[1],Levelattrr[2],tab_class_name[0],tab_class_name[1],tab_class_name[2]

"""

@app.callback([
             Output("Level1NameSelect", "value"),
          #   Output("Level2NameSelect", "value"),
             ],         
              Input('GrainSelect', 'value'),
              Input('KPISelect', 'value'),     
              Input('tabsdrilldown','active_tab'),
              Input('graphlevel0', 'relayoutData'),
              Input('graphoveralltime', 'relayoutData'),
              Input('graph-with-slider', 'relayoutData'),
              Input('graphlevel0', 'clickData'),
              Input('graphoveralltime', 'clickData'),
              Input('graph-with-slider', 'clickData'),
              Input('graph-level1compare', 'clickData'),
              Input('graph-level2compare', 'clickData'),
              Input('graph-level1compare', 'relayoutData'),
              Input('graph-level2compare', 'relayoutData'),
              Input('sweepl1','n_clicks'),
              #eval(kpigrouplistinput3[0]),
              )
def filterclicks(GrainSelect,KPISelect,tabsdrilldown,relayoutDatal0,relayoutDatal1,relayoutDatal2,clickdatal0,clickdatal1,clickdatal2,clickdatal1bar,clickdatal2bar,relayoutl1bar,relayoutl2bar,sweepl1):#,*args
    print('execute filterclicks')
    if tabsdrilldown == 'tab-0':
        relayoutdata1 = relayoutDatal0
        clickdatabar1 = clickdatal1bar
        clickdata1 = clickdatal0
        changeid = 'graphlevel0.relayoutData'
    elif tabsdrilldown == 'tab-1':
        relayoutdata1 = relayoutDatal1
        clickdatabar1 = clickdatal1bar
        clickdata1 = clickdatal1
        changeid = 'graphoveralltime.relayoutData'
    elif tabsdrilldown == 'tab-2':
        relayoutdata1 = relayoutDatal2
        clickdatabar1 = clickdatal2bar
        clickdata1 = clickdatal2
        changeid = 'graph-with-slider.relayoutData'
    else:
        relayoutdata1 = relayoutDatal0
        changeid = 'graphlevel0.relayoutData'
        clickdatabar1 = clickdatal1bar
        clickdata1 = clickdatal0
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    Level1Name = clickdatabar1['points'][0]['y']
    if changed_id == 'tabselect.active_tab':
        Level1NameListoutput = Level1Name
    elif changed_id == 'tabsdrilldown.active_tab':
        Level1NameListoutput = Level1Name
    elif changed_id == 'GrainSelect.value':
        Level1NameListoutput = Level1Name
    elif changed_id == 'KPISelect.value':
        Level1NameListoutput = Level1Name
    elif Level1Name == '':
        Level1NameListoutput = Level1NameList
    elif sweepl1==1:
        Level1NameListoutput = Level1NameList
    else:
        Level1NameListoutput = Level1Name
    print(Level1Name)
    print(Level1NameListoutput)
    print(sweepl1)
    return Level1NameListoutput#,Level2NameList
"""
@app.callback(
    Output('graph-level1compare', 'selectedData'),
    [Input('sweepl1', 'n_clicks')]
)

def reset_clickDatal1(n_clicks):
    print('removefilter')
    return None

@app.callback(
    Output('graph-level2compare', 'selectedData'),
    [Input('sweepl2', 'n_clicks')]
)

def reset_clickDatal2(n_clicks):
    print('removefilter')
    return None

datefromtmp = []
datetotmp = []
datefromtmp.append(str(dfl0['Period_int'].min())[0:10])
datetotmp.append(str(dfl0['Period_int'].max())[0:10])


@app.callback([
              Output('dfl0', 'data'),
              Output('dfl1', 'data'),
              Output('dfl2', 'data'),
              Output('dffcomparefilter', 'data'),
              Output('dflcomparekpi', 'data'),
              Output('output-container-date-picker-range', 'children'),
             ],              
              Input('GrainSelect', 'value'),
              Input('KPISelect', 'value'),
              Input('graphlevel0', 'relayoutData'),
              Input('graphoveralltime', 'relayoutData'),
              Input('graph-with-slider', 'relayoutData'),
              Input('graph-with-slider', 'restyleData'),
              Input('graphlevel0', 'clickData'),
              Input('graphoveralltime', 'clickData'),
              Input('graph-with-slider', 'clickData'),
              Input('tabsdrilldown','active_tab'),
              Input("Level1NameSelect", "value"),
              Input("Level2NameSelect", "value"),
              Input('graph-level1compare', 'selectedData'),
              Input('graph-level2compare', 'selectedData'),
              )
def clean_data(GrainSelect,KPISelect,relayoutDatal0,relayoutDatal1,restyleDatal1,relayoutDatal2,clickdatal0,clickdatal1,clickdatal2,tabsdrilldown,Level1NameSelect,Level2NameSelect,selecteddatal1bar,selecteddatal2bar):#,*args,sweepl1 relayoutl1barclickdatal2bar
    print('execute clean_data')
    selectedlistl1= []
    selectedlistl2= []
    if selecteddatal1bar is None:
        print('leeg')
    else:
        for i in selecteddatal1bar['points']:
            selectedlistl1.append(i['y'])
    if selecteddatal2bar is None:
        print('leeg')
    else:
        for i in selecteddatal2bar['points']:
            selectedlistl2.append(i['y'])
    dfll0 = []
    dfll1 = []
    dfll2 = []
    dfllCompare = []
    #dff0 = update_filter_l0(dfl0, GrainSelect, KPISelect)
    dff1 = update_filter_l1(dfl1, GrainSelect, KPISelect, Level1NameSelect)
    dff2 = pd.DataFrame(update_filter_l2(dfl2, GrainSelect, KPISelect, Level1NameSelect, Level2NameSelect))
    dffcompare0 = dfl0[
        (dfl0["Grain"] == GrainSelect)
        ]
    dffcompare1 = dfl1[
        (dfl1["Grain"] == GrainSelect)
        & (dfl1["LevelName_1"].isin(Level1NameSelect))
        ]
    dffcompare2 = dfl2[
        (dfl2["Grain"] == GrainSelect)
        & (dfl2["LevelName_1"].isin(Level1NameSelect))
        & (dfl2["LevelName_2"].isin(Level2NameSelect))
        ]
    #recalculation the calculated values because for example one attribute of level x+1 can be found under multiple attributes x (for example attribute 'protocol version: V2' can me found both under 'Aave' and 'Compound')
    testtmp0 = pd.DataFrame(dff1.loc[:,~dff1.columns.str.endswith(('_1'))]).fillna(0)
    testtmp1 = pd.DataFrame(dff2.loc[:,~dff2.columns.str.endswith(('_2','_0'))]).fillna(0)

    columnsdff0 = testtmp0.columns.tolist()
    columnsdff0.remove('Numerator')
    columnsdff0.remove('Denominator')
    columnsdff0.remove('Numerator_LP')
    columnsdff0.remove('Denominator_LP')
    columnsdff0.remove('d_level1_id')
    
    columnsdff1 = testtmp1.columns.tolist()
    columnsdff1.remove('Numerator')
    columnsdff1.remove('Denominator')
    columnsdff1.remove('Numerator_LP')
    columnsdff1.remove('Denominator_LP')
    columnsdff1.remove('d_level0_id')
    columnsdff1.remove('d_level2_id')

    dff0 = testtmp0.groupby(columnsdff0, as_index=False, sort=False).agg(
            {'Denominator': eval(AggregateNumDenom(KPIDenomAgg[KPISelect])), 'Numerator': eval(AggregateNumDenom(KPINumAgg[KPISelect])), 'Denominator_LP': eval(AggregateNumDenom(KPIDenomAgg[KPISelect])), 'Numerator_LP': eval(AggregateNumDenom(KPINumAgg[KPISelect]))})
    

    dff1 = testtmp1.groupby(columnsdff1, as_index=False, sort=False).agg(
           {'Denominator': eval(AggregateNumDenom(KPIDenomAgg[KPISelect])), 'Numerator': eval(AggregateNumDenom(KPINumAgg[KPISelect])), 'Denominator_LP': eval(AggregateNumDenom(KPIDenomAgg[KPISelect])), 'Numerator_LP': eval(AggregateNumDenom(KPINumAgg[KPISelect]))})
   
    dffcompare = []
    if tabsdrilldown == 'tab-0':
        relayoutdata1 = relayoutDatal0
        clickdata1 = clickdatal0
        changeid = 'graphlevel0.relayoutData'
        dffcompare.append(dffcompare0)
    elif tabsdrilldown == 'tab-1':
        relayoutdata1 = relayoutDatal1
        clickdata1 = clickdatal1
        changeid = 'graphoveralltime.relayoutData'
        dffcompare.append(dffcompare1)
    elif tabsdrilldown == 'tab-2':
        relayoutdata1 = relayoutDatal2
        clickdata1 = clickdatal2
        changeid = 'graph-with-slider.relayoutData'
        dffcompare.append(dffcompare2)
    else:
        relayoutdata1 = relayoutDatal0
        changeid = 'graphlevel0.relayoutData'
        clickdata1 = clickdatal0
        dffcompare.append(dffcompare0)
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if relayoutdata1 == {'autosize': True} or relayoutdata1 == None:
        ''
    elif changed_id == changeid:
        if 'xaxis.range[0]' in relayoutdata1:
            datefromtmp.append(relayoutdata1['xaxis.range[0]'][0:10])
            datetotmp.append(relayoutdata1['xaxis.range[1]'][0:10])
        elif 'xaxis.range' in relayoutdata1:
            datefromtmp.append(relayoutdata1['xaxis.range'][0])
            datetotmp.append(relayoutdata1['xaxis.range'][1])
    elif changed_id == 'tabselect.active_tab':
        ''
    elif changed_id == 'tabsdrilldown.active_tab':
        ''
    elif changed_id == 'GrainSelect.value':
        ''
    elif changed_id == 'Level1NameSelect.value':
        ''
    elif changed_id == 'Level2NameSelect.value':
        ''
    elif changed_id == 'KPISelect.value':
        ''

    if not datefromtmp:
        dfll0.append(dff0)
        dfll1.append(dff1)
        dfll2.append(dff2)
        dfllCompare.append(dffcompare[0])
    elif changed_id == 'GrainSelect.value':
        dfll0.append(dff0)
        dfll1.append(dff1)
        dfll2.append(dff2)
        dfllCompare.append(dffcompare[0])
    else:
        dfll1.append(dff1[dff1['Period_int'].between(datefromtmp[-1], datetotmp[-1])].reset_index())
        dfll2.append(dff2[dff2['Period_int'].between(datefromtmp[-1], datetotmp[-1])].reset_index())
        dfll0.append(dff0[dff0['Period_int'].between(datefromtmp[-1], datetotmp[-1])].reset_index())
        dfllCompare.append(dffcompare[0][dffcompare[0]['Period_int'].between(datefromtmp[-1], datetotmp[-1])].reset_index())
    dffl0 = dfll0[0]   
    dffl1 = dfll1[0]   
    dffl2 = dfll2[0]  
    dffl0click = []
    dffl1click = []
    dffl2click = []
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if not selectedlistl1 and not selectedlistl2:
        dffl0click.append(dffl0)
        dffl1click.append(dffl1)
        dffl2click.append(dffl2)
    elif not selectedlistl2:
        dffl0click.append(dffl0)
        dffl1click.append(dffl1[dffl1['LevelName_1'].isin(selectedlistl1)])
        dffl2click.append(dffl2[dffl2['LevelName_1'].isin(selectedlistl1)])
    elif not selectedlistl1:
        dffl0click.append(dffl0)
        dffl1click.append(dffl1)
        dffl2click.append(dffl2[dffl2['LevelName_2'].isin(selectedlistl2)])
    else:
        dffl0click.append(dffl0)
        dffl1click.append(dffl1[dffl1['LevelName_1'].isin(selectedlistl1)])
        dffl2click.append(dffl2[(dffl2['LevelName_1'].isin(selectedlistl1)) & (dffl2['LevelName_2'].isin(selectedlistl2))])
    dffl0end = dffl0click[0]
    dffl1end = dffl1click[0]
    dffl2end = dffl2click[0]    
    dflCompare = dfllCompare[0]
    dffl0json = dffl0end.to_json(date_format='iso', orient='split')
    dffl1json = dffl1end.to_json(date_format='iso', orient='split')
    dffl2json = dffl2end.to_json(date_format='iso', orient='split')
    comparejson = dflCompare.to_json(date_format='iso', orient='split')

    dff1tmp = dffl1end 
    dff2tmp = dffl2end 
    dff2tmp['Period_int'] = pd.to_datetime(dff2tmp['Period_int']).dt.tz_localize(None)
    dff1tmp['Period_int'] = pd.to_datetime(dff1tmp['Period_int']).dt.tz_localize(None)
    dffcompareclick =[]

    if clickdata1 == "{'autosize': True}" or clickdata1 == None:
        dffcompareclick.append(dflCompare)
       # dff1.append(comparejson)
    else:
        dffcompareclick.append(dflCompare[dflCompare['Period_int'] == clickdata1['points'][0]['x']])
       # dff1.append(dff1tmp[dff1tmp['Period_int'] == clickdata1['points'][0]['x']])
    dffcompareclick2 = dffcompareclick[0]
    dffcomparejson = dffcompareclick2.to_json(date_format='iso', orient='split')
   # dffl2comparejson = dff2[0].to_json(date_format='iso', orient='split')

    clickdatasend = dffl0end['PeriodName'].unique()
    Periodchosencount = []
    Periodchosencount.clear()
    Periodchosencount.append(len(clickdatasend.tolist()))
    Displaypreviouscount = []
    if Periodchosencount[0]>1:
        Displaypreviouscount.append("block")
    else:
        Displaypreviouscount.append("none") 
   # style={eval(Displaypreviouscount[0])}
    style = {'display': Displaypreviouscount}
    string_prefix = 'You have selected: '
    if datefromtmp is not None:
        start_date_string = str(min(dffl0['Period_int']))[0:10]
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if datetotmp is not None:
        end_date_string = str(max(dffl0['Period_int']))[0:10]
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        string_prefix = 'Select a date to see it displayed here'
    level1options=dffl1end["LevelName_1"].unique()
    return dffl0json,dffl1json,dffl2json,dffcomparejson,comparejson,string_prefix#,style,style,style,style,style#,clickdatasend

datefromtmp.clear()
datetotmp.clear()  

@app.callback(
    Output('cardsid', 'children')
    ,
    Input('dflcomparekpi', 'data'),
  #  Input('dfl0','data'),
    Input('dffcomparefilter', 'data'),
  #  Input('tabsdrilldown','active_tab'),
    Input("KPISelect", "value"),
    Input("KPIGroupSelect", "value"),
    Input("breakpoints", "widthBreakpoint"),
    State("breakpoints", "width"),
    #Input("Perioddropdown", "value"),
    #Input('graphlevel0', 'clickData'),
    #Input('graphoveralltime', 'clickData'),
    #Input('graph-with-slider', 'clickData'),
   # eval(kpigrouplistinput3[0]),  
)

def updatekpiindicator(compareset,dffcomparefilter,KPISelect,KPIGroupSelect,widthBreakpoint,window_width): #,*args,tabsdrilldown,clickData0,clickDatal1,clickDatal2,dfl0
    print('execute updatekpiindicator')
   # dfl0 = pd.read_json(dfl0, orient='split')
    dffcomparefilter = pd.read_json(dffcomparefilter, orient='split')
   # dfl2 = pd.read_json(dfl2click, orient='split')
    dataCompare = pd.read_json(compareset, orient='split')
    carousellist.clear()
    carousellist3.clear()
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if kpicountout[0]<slides_to_show_ifenough:
        slides_to_show = kpicountout[0]
    else:
        slides_to_show = slides_to_show_ifenough
    
    dftouse = dffcomparefilter[
            (dffcomparefilter["KPIGroup"].isin(KPIGroupSelect))
        ]
    KPIListFiltered = d_kpi[
            (d_kpi["KPIGroup"].isin(KPIGroupSelect))
        ]
    KPIListFiltered.sort_values(by=['Sorting'])
    KPINameList2 = KPIListFiltered['KPIName'].unique()
    outputactual =[]
    outputactualtxt =[]
    outputlasttxt =[]
    outputlast = []
    Card = []
    Cardstyle = []
    popbody = []
    carddivstyle = []
   # outputlasttxtlogo = []
    arrow= []
    outputactual.clear()
    outputactualtxt.clear()
    Card.clear()
    Cardstyle.clear()
    carddivstyle.clear()
    arrow.clear()
    popbody.clear()
  #  outputlasttxtlogo.clear()
    for i,kpi in enumerate(KPINameList2):
        enum = str(i + 1)
        dataCompare1 = dftouse[
            (dftouse["KPIName"] == kpi)
        ]
        df_by_LevelName = dataCompare1[["Denominator","Numerator","Denominator_LP","Numerator_LP"]]#"d_kpi_id","Denominator","Numerator","Denominator_LP","Numerator_LP"
        
        clickdatasend = dataCompare1['PeriodName'].unique()
        Periodchosencount = []
        Periodchosencount.clear()
        Periodchosencount.append(len(clickdatasend.tolist()))
        Displayprevious = []
        if Periodchosencount[0]>1:
            Displayprevious.append("none")
        else:
            Displayprevious.append("block")
        logopositive = "green"
        logonegative = "red"
        logoneutral = "grey"
        value = []
        value_lp = []
        valueNum =[]
        valueDenom = []
        valueNumLP =[]
        valueDenomLP =[]
        notation =[]
        valueNum.clear()
        valueDenom.clear()
        valueNumLP.clear()
        valueDenomLP.clear()
        df_by_LevelName.reset_index(drop=True,inplace=True)
        Notationtmp = KPISelectedStylePython(kpi)
        Notation = KPISelectedStyle(kpi)
        Notationlist=Notationtmp[0]
        Calculation = CalculationDEF(kpi)
        CalculationLogic = CalculationLogicOveral(Calculation)
        AggregateNum = AggregateNumDenom(Calculation)
        AggregateDenom = AggregateNumDenom(Calculation)
        meannum = []
        if str(eval(AggregateNum))=='mean':
            meannum.append("axis = 0")
        else:
            meannum.append("")
        meandenom = []
        if str(eval(AggregateDenom)) == 'mean':
            meandenom.append("axis = 0")
        else:
            meandenom.append("")
        agnum = "df_by_LevelName['Numerator']."+str(eval(AggregateNum)) +"("+meannum[0]+")"
        agdenom = "df_by_LevelName['Denominator']." + str(eval(AggregateDenom)) +"("+meandenom[0]+")"
        agnumlp = "df_by_LevelName['Numerator_LP']." + str(eval(AggregateNum)) +"("+meannum[0]+")"
        agdenomlp = "df_by_LevelName['Denominator_LP']." + str(eval(AggregateDenom)) +"("+meandenom[0]+")"
        df_by_LevelName = df_by_LevelName.assign(Aggnum=eval(agnum))
        valueNum.append(df_by_LevelName['Aggnum'].iloc[0])
        df_by_LevelName = df_by_LevelName.assign(Aggdenom=eval(agdenom))
        valueDenom.append(df_by_LevelName['Aggdenom'].iloc[0])
        df_by_LevelName = df_by_LevelName.assign(Aggnum_LP=eval(agnumlp))
        valueNumLP.append(df_by_LevelName['Aggnum_LP'].iloc[0])
        df_by_LevelName = df_by_LevelName.assign(Aggdenom_LP=eval(agdenomlp))
        valueDenomLP.append(df_by_LevelName['Aggdenom_LP'].iloc[0])
        twee = [i / j for i, j in zip(valueNum, valueDenom)]
        twee_lp = [i / j for i, j in zip(valueNumLP, valueDenomLP)]
        if Calculation == 2:
            CalculationString = twee[0]
            CalculationStringlp = twee_lp[0]
            value.append(CalculationString)
            value_lp.append(CalculationStringlp)
        elif Calculation == 1:
            CalculationString = sum(valueNum)
            CalculationStringlp = sum(valueNumLP)
            value.append(CalculationString)
            value_lp.append(CalculationStringlp)
        if value_lp[0]==value[0]:
            arrow = "'arrow_right'"
        elif value_lp[0]<value[0]:
            arrow = "'arrow_drop_up'"
        else:
            arrow = "'arrow_drop_down'"
        valueNum.clear()
        valueDenom.clear()
        valueNumLP.clear()
        valueDenomLP.clear()
        meannum.clear()
        meandenom.clear()
        notation.append(Notationlist)
        if kpi == KPISelect:
            style111 = {'box-shadow': f'0px -0px 5px 2px {Highlightcardcolor}'}
        else:
            style111 = {}
        outputactualtxt =str(eval(Notationlist).format(value_lp[0])) #value[0]#eval(Notationlist).format(value[0]),
        outputlasttxt = str(eval(Notationlist).format(value[0])) #value[0]#eval(Notationlist).format(value[0]),
        Card.append(kpi)
        style = {'display': Displayprevious[0] , 'color' : logopositive if HigherIs[kpi]==1 else logonegative if HigherIs[kpi]==2 else logoneutral}
        popbody.append(kpi)
     #   outputlasttxtlogo = logopositive
      #  carddivstyle.append(stylempty)
        value.clear()
        value_lp.clear()
        notation.clear()
        numbertmp= i+1
        number=str(numbertmp)
        numberi=str(numbertmp)
        carousellist.append(
        f"""html.Div(
                html.Div([
                    html.I('info', className='material-icons', 
                               id='open-box{number}', n_clicks=0),
                    dbc.Popover(
                        [
                            dbc.PopoverBody('And heres some amazing content. Cool!',id='popbody{number}',className='h6'),
                        ],
                        target='open-box{number}',
                        trigger='legacy',
                        className='popupper',
                        hide_arrow=False
                        ),
                    dcc.Textarea(value=f'{kpi}',
                                 disabled=True,
                                 draggable=False,
                                 contentEditable=False,
                                 id='Card{number}',
                                 className='col-12 h5'),
                    html.Div(children=[
                        dcc.Textarea(value=f'{outputactualtxt}',
                            id='indicator-graph{number}TXT',
                            contentEditable=False,
                            disabled=True,
                            readOnly=True,
                            draggable=False,
                            className='col-12 h6'
                        ),
                        html.Div([
                             dcc.Textarea(value=f'{outputlasttxt}',
                                 id="indicatorlast-graph{number}TXT",
                                 contentEditable =False,
                                 disabled=True,
                                 readOnly=True,
                                 draggable=False,
                                 className='col-8 h7',
                             ),
                             html.I({arrow},className="material-icons icon",id="arrow{number}")
                            ],id="indicatorlast-graph{number}TXTLogo",style={style})
                        ])
                	],id='CardContent{number}'),id='carddiv{number}',style={style111},className='carddiv')"""
        ) 
    carousellist2=','.join(carousellist)
    carousellist3.append(carousellist2)
    if widthBreakpoint =='sm':
        slides_to_showfinal = 1
        slides_to_scrollfinal = 1
    else:
        slides_to_showfinal = slides_to_show
        slides_to_scrollfinal = slides_to_scroll
    return [html.Div(dbc.Spinner(size='md',delay_hide=1500,children=[dtc.Carousel(eval(carousellist3[0])
        ,
        slides_to_scroll=slides_to_scrollfinal,
        slides_to_show=slides_to_showfinal,
        center_padding='10px',
        swipe_to_slide=True,
        autoplay=False,
        speed=2000,
       # variable_width=True,
        dots=True,
        center_mode=False,
        id='slickthinky',
        className='col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12',
        responsive=[
            ],
    )]))
    ]


######################################################################################################################
######################################################################################################################
################################################----tab 0 aanmaken----###############################################
######################################################################################################################
######################################################################################################################


"""
@app.callback(
    eval(carddivstyle3[0]),
      #  Output('kpigroup0', 'style'),
      #  Output('kpigroup1', 'style'),
      #  Output('kpigroup2', 'style'),
      #  Output('kpigroup3', 'style'),
      #  Output('kpigroup4', 'style'),
    [   
    Input("KPISelect", "value"),
    Input("KPIGroupSelect", "value"),
    eval(kpigrouplistinput3[0]),
    eval(carddivnclicks3[0])
    ]
)

def update_df_KPI(KPISelect,KPIGroupSelect,*args):#,
    print('execute update_df_KPI')
    #dff1 = dfl1[
    #(dfl1["KPIName"] == KPISelect)
    #]
    dff = dfl1[
        (dfl1["KPIGroup"].isin(KPIGroupSelect))
    ]
    KPIListFiltered = d_kpi[
            (d_kpi["KPIGroup"].isin(KPIGroupSelect))
        ]
    KPIListFiltered.sort_values(by=['Sorting'])
    KPINameListo = KPIListFiltered['KPIName'].unique()
   # listtop =[{'label': i, 'value': i} for i in dff1["Level1Name"].unique()]
    cardstyle = []
    cardstyle.clear()
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    for i in KPINameListo:
        if i == KPISelect:
            cardstyle.append({'box-shadow': f'0px -0px 9px 0px {BeautifulSignalColor}'})
        else:
            cardstyle.append({'box-shadow':'0px 0px 9px 0px transparent'})
    if IsCum(KPISelect) == 1:
        IsCumStyle= {'display': 'block'}
    else:
        IsCumStyle= {'display': 'none'}
    xstyles = []
    xstyles2 =[]
    xstyles.clear()
    xstyles2.clear()       

    KPIGroupList = d_kpi['KPIGroup'].unique().tolist()
    for i,kpigroup in enumerate(KPIGroupList):
        xstyles2.append(f'xstyles[{i}]')
        if  KPIGroupSelect == KPIGroupList:
            if i == 0:
                xstyles.append({'color':buttonlogocolor,'background-color':buttoncolor})
            else:
                xstyles.append({})
        elif kpigroup == KPIGroupSelect:
            xstyles.append({'color':buttonlogocolor,'background-color':buttoncolor})
        else:
            xstyles.append({})
    return eval(carddivstylereturn3[0])#,eval(xstyles2[0])
"""

#graphlevel0
@app.callback(
    Output('graphlevel0', 'figure'),
     
     Input('dfl0', 'data'),
     Input('GrainSelect', 'value'),
     Input("KPISelect", "value"),
     Input("KPIGroupSelect", "value"),
     Input("CumulativeSwitch", "label"),
     Input("PercentageTotalSwitch", "label"),
     Input("ShowValueSwitch", "label"),
)

def update_kpiagg(data00,GrainSelect,KPISelect,KPIGroupSelect,CumulativeSwitch,PercentageTotalSwitch,ShowValueSwitch):  #,*args ,Level2NameSelect,toggle, relayoutData
    print('execute update_kpiagg')
    data0 = pd.read_json(data00, orient='split')
    dff = data0 #update_filter_l0(data0, GrainSelect, KPISelect)  # ,Level2NameSelect
    traces3 = []
    dataframe = Cumloop0(CumulativeSwitch)
    Notation = KPISelectedStyle(KPISelect)
    Calculation = CalculationDEF(KPISelect)
    Notation = KPISelectedStyle(KPISelect)
    Calculation = CalculationDEF(KPISelect)
    for i in dff.LevelName_0.unique():
        df_by_Level0Name = dff[dff['LevelName_0'] == i]
        ##df_by_Level0NameCum = dff[dff['Level0Name'] == i]
        ##df_by_Level0NameCum['Numerator'] = df_by_Level0NameCum['Numerator'].cumsum()
        ##df_by_Level0NameCum['Denominator'] = df_by_Level0NameCum['Denominator'].cumsum()
        df_by_Level0Name = df_by_Level0Name.assign(NumeratorCum=lambda df_by_Level0Name: df_by_Level0Name.Numerator.cumsum())
        df_by_Level0Name = df_by_Level0Name.assign(DenominatorCum=lambda df_by_Level0Name: df_by_Level0Name.Denominator.cumsum())
        y = eval(eval(dataframe[1]))
        default_color = "red"
        colors = {"2021-05-31T00:00:00.000Z": "red"}
        color_discrete_map = {
            c: colors.get(c, default_color)
            for c in eval(dataframe[0]).Period_int.unique()}
        traces3.append(dict(
            eval(dataframe[0]),
            x=eval(dataframe[0]).Period_int,  # df_by_Level1Name['Period_int'],
            cumulative_enabled=True,
            color=eval(dataframe[0]).Period_int,
            y=y,
            text=y if ShowValueSwitch == 'True' else '',
            mode=linesormarkers(GrainSelect),
            opacity=1,
            customdata=eval(dataframe[0]).LevelName_0,
            line=dict(
                width=2,
                shape="spline",
            ),
            marker=dict(
                size=5,
                line=dict(width=0.1
                          ),
                color=Level0NameColor[i],
            ),
            type=visualDEF(KPISelect),
            name=i,
            transforms=dict(
                type='aggregate',
                groups="Period_int",
                aggregations=[
                    dict(target='Numerator', func=AggregateNumDenom(Calculation)),  # , enabled=True
                    dict(target='Denominator', func=AggregateNumDenom(Calculation))  # , enabled=True
                ]
            ),
        )
        )
    return {
        'data': traces3,
        'layout': dict(
            barmode='stack',
            barnorm=eval(PercentageTotalSwitchDEF(PercentageTotalSwitch)),
            xaxis=dict(type='string',
                       title='',
                       showgrid=False,
                       gridwidth=0,
                       showline=False,
                       color=fontcolor,
                       rangeselector=dict(
                           buttons=list([
                               dict(count=1,
                                    label="1m",
                                    step="month",
                                    stepmode="backward"),
                               dict(count=6,
                                    label="6m",
                                    step="month",
                                    stepmode="backward"),
                               dict(count=1,
                                    label="YTD",
                                    step="year",
                                    stepmode="todate"),
                               dict(count=1,
                                    label="1y",
                                    step="year",
                                    stepmode="backward"),
                               dict(count=10,
                                    label="All",
                                    step="year",
                                    stepmode="backward")
                           ])
                       ),
                       rangeslider=dict(
                           visible=False
                       ),
                       linewidth=2,
                       font=dict(
                           size=14,
                       )
                       ),
            yaxis=dict(title='',
                       linewidth=2,
                       tickformat=eval(Notation[0]),
                       showgrid=False,
                       showline=False,
                       autorange=True,
                       fixedrange=True,
                       color=fontcolor,
                       gridwidth=0.5,
                       font=dict(
                           size=14,
                       )
                       ),
            margin={'l': 60, 'b': 45, 't': 33, 'r': 40},
            legend=dict(
                font=dict(
                    size=15,
                    color=fontcolor,
                ),
                yanchor="top",
                y=1,
                x=1.01,
                xanchor="left",
            ),
            modebar = dict(
                        bgcolor='transparent',
                        color=BeautifulSignalColor,
            ),
            autosize=True,
            plot_bgcolor=graphcolor,
            paper_bgcolor=graphcolor,
            font=dict(
            ),
            images=dict(
                x = 0,
                y = 1,
                sizex=0.2,
                sizey=0.2,
            ),
            title=dict(text=str(KPISelect),  # +' -     selected: '+str(Level2NameSelect),
                       font=dict(color=fontcolor,
                                 ),
                       ),
            hovermode='closest',
            transition={'duration': 500},
        )
    }


@app.callback(
    Output('graph-level0compare', 'figure'),
    [Input('dfl0', 'data'),
    # Input('dfl1', 'data'),
     Input("KPISelect", "value"),
     Input("KPIGroupSelect", "value"),
     Input("Level1NameSelect", "value"),
     Input("Level2NameSelect", "value"),
     Input('graphlevel0', 'clickData'),
     Input("Totaalswitch", "label"),
     Input("breakpoints", "widthBreakpoint"),
    # eval(kpigrouplistinput3[0]),  
     ]
)
def update_level1Graph(data00,KPISelect,KPIGroupSelect,Level1NameSelect,Level2NameSelect,clickData,Totaalswitch,widthBreakpoint): #,hoverData,*args
    data0 = pd.read_json(data00, orient='split')
    dff0tmp = data0 
    dff0tmp['Period_int'] = pd.to_datetime(dff0tmp['Period_int']).dt.tz_localize(None)
    dff0 = []
    if clickData == "{'autosize': True}" or clickData == None:
        dff0.append(dff0tmp)
    else:
        dff0.append(dff0tmp[dff0tmp['Period_int'] == clickData['points'][0]['x']])
    dff0 = dff0[0]
    traces = []
    if widthBreakpoint=='sm':
        title = ''
    else:
        title = dict(text=str(KPISelect) + ' per ',# + Level2Entitytype,
                       # +' -     selected: '+str(Level2NameSelect),
                       font=dict(#family='Montserrat',
                                 size=22,
                                 color=fontcolor,
                        ),
        ) 
    Notation = KPISelectedStyle(KPISelect)
    Calculation = CalculationDEF(KPISelect)
    AggregateNum = NumaggregateDEF(KPISelect)
    AggregateDenom = DenomaggregateDEF(KPISelect)
    for j in dfl0.LevelName_0.unique():
        df_by_Level0Name = dff0[dff0['LevelName_0'] == j]
        x2 = eval(CalculationLogic0(Calculation))
        traces.append(dict(
            df_by_Level0Name,
            y=df_by_Level0Name.LevelName_0,
            x=x2,
            text=x2,
            text_auto=True,
            texttemplate="%{value:" + eval(Notation[0]) + "}",  # "%{value:.01%}",
            textformat=eval(Notation[0]),
            type='bar',
            marker=dict(
                opacity=1,
                color=df_by_Level0Name.LevelColor_0,
                color_discrete_map='identity',
                line=dict(width=0.1,
                          color=df_by_Level0Name.LevelColor_0,
                          color_discrete_map='identity',
                          opacity=1,
                          ),
            ),
            orientation="h",
            name=j,
            transforms=[dict(
                type='aggregate',
                groups=df_by_Level0Name.LevelName_0,
                aggregations=[
                    dict(target='Numerator', func=AggregateNumDenom(AggregateNum)),  
                    dict(target='Denominator', func=AggregateNumDenom(AggregateDenom))  
                ]
            ),
            ]
        ))
    return {
        'data': traces,
        'layout': dict(
            clickmode='event+select',
            type='bar',
            xaxis=dict(type='string',
                       title='',
                       showgrid=False,
                       gridwidth=0,
                       fixedrange=True,
                       showline=False,
                       tickformat=eval(Notation[0]),
                       visible=False,
                       color=fontcolor,
                       font=dict(
                           size=14,
                       )
                       ),
            yaxis=dict(title='',
                       showline=False,
                       showgrid=False,
                       categoryorder="total ascending",
                       gridwidth=0,
                       color=fontcolor,
                       ),
            margin={'l': 140, 'b': 25, 't': 37, 'r': 40},
            showlegend=False,
            autosize=True,
            plot_bgcolor=graphcolor,
            paper_bgcolor=graphcolor,
            modebar=dict(
                bgcolor='transparent',
                color=BeautifulSignalColor,
            ),
            font=dict(
                size=15,
            ),
            title=title,
            hovermode='closest',
            transition={'duration': 500},
        )
    }

######################################################################################################################
######################################################################################################################
################################################----tab 1 aanmaken----###############################################
######################################################################################################################
######################################################################################################################

#graphoveralltime
@app.callback([
    Output('graphoveralltime', 'figure'),
    Output('Level2NameSelect', 'options'),
    ],
    [Input('dfl0', 'data'),
     Input('dfl1', 'data'),
     Input('dfl2', 'data'),
     Input('GrainSelect', 'value'),
     Input("KPISelect", "value"),
     Input("KPIGroupSelect", "value"),
     Input("Level1NameSelect", "value"),
     Input("Level2NameSelect", "value"),
     Input("Totaalswitch", "label"),
     Input("CumulativeSwitch", "label"),
     Input("PercentageTotalSwitch", "label"),
     Input("ShowValueSwitch", "label"),
     Input("breakpoints", "widthBreakpoint"),
     #eval(kpigrouplistinput3[0]),  
   #  Input("DBColorVar", "value"),
     ]
)
def update_mainfigure(data00,data11,data22,GrainSelect,KPISelect,KPIGroupSelect,Level1NameSelect,Level2NameSelect,Totaalswitch,CumulativeSwitch,PercentageTotalSwitch,ShowValueSwitch,widthBreakpoint):#,*args
    print('execute update_mainfigure')
    data0 = pd.read_json(data00, orient='split')
    data1 = pd.read_json(data11, orient='split')
    data2 = pd.read_json(data22, orient='split')
    dff0 = data0 
    dff1 = data1  
    dff2 = data2 
    Level2NameList = dff2['LevelName_2'].unique().tolist()
    options = [{'label': str(i), 'value': str(i)} for i in Level2NameList]
    traces3 = []
    tracestotal = []
    traces = []
    traces2 = []
    totaaljanee = Totaalloop(Totaalswitch)
    appendList1 = [tracestotal, traces]
    appendList2 = eval(totaaljanee)
    dataframe0 = Cumloop0(CumulativeSwitch)
    dataframe1 = Cumloop1(CumulativeSwitch)
    Notation = KPISelectedStyle(KPISelect)
    Calculation = CalculationDEF(KPISelect)
    if widthBreakpoint=='sm':
        title = ''
    else:
        title = dict(text=str(KPISelect) + ' per ',# + Level2Entitytype,
                       # +' -     selected: '+str(Level2NameSelect),
                       font=dict(#family='Montserrat',
                                 size=22,
                                 color=fontcolor,
                        ),
        ) 
    if widthBreakpoint=='sm':
        legend=dict(
                    font=dict(
                        size=15,
                        color=fontcolor,
                    ),
                    orientation="h"
                )
    else:
        legend=dict(
                    font=dict(
                        size=15,
                        color=fontcolor,
                    ),
                    yanchor="top",
                    y=1,
                    x=1.01,
                    xanchor="left",
                )
    for z in appendList1:
        for i in dff1.LevelName_1.unique():
           df_by_Level1Name = dff1[dff1['LevelName_1'] == i]
          ## df_by_Level1NameCum = dff[dff['Level1Name'] == i]
          ## df_by_Level1NameCum['Numerator'] = df_by_Level1NameCum['Numerator'].cumsum()
          ## df_by_Level1NameCum['Denominator'] = df_by_Level1NameCum['Denominator'].cumsum()
           df_by_Level1Name = df_by_Level1Name.assign(NumeratorCum=lambda df_by_Level1Name: df_by_Level1Name.Numerator.cumsum())
           df_by_Level1Name = df_by_Level1Name.assign(DenominatorCum=lambda df_by_Level1Name: df_by_Level1Name.Denominator.cumsum())
           y = eval(eval(dataframe1[1]))
           z.append(dict(
               eval(dataframe1[0]),
               x=eval(dataframe1[0]).Period_int, 
               cumulative_enabled=True,
               y=y,
               text=y if ShowValueSwitch == 'True' else '',
               text_auto=True,
               mode=linesormarkers(GrainSelect),
               opacity=1,
               customdata=eval(dataframe1[0]).LevelName_1,
               line=dict(
                 width=2,
                 shape="spline",
                 color=eval(dataframe1[0]).LevelColor_1,
               ),
               marker=dict(
                   size = 5,
                   line = dict(width=0.1
                               ),
                   color=eval(dataframe1[0]).LevelColor_1,
               ),
               type=visualDEF(KPISelect),
               name=i,
               transforms=dict(
                   type='aggregate',
                   groups="Period_int",
                   aggregations=[
                       dict(target='Numerator', func=AggregateNumDenom(Calculation)),  # , enabled=True
                       dict(target='Denominator', func=AggregateNumDenom(Calculation))  # , enabled=True
                   ]
               ),
           )
           )
    for d in appendList2:
        for v in dff0.LevelName_0.unique():
            df_by_Level0Name = dff0[dff0['LevelName_0'] == v]
            ##df_by_Level0NameCum = dff0[dff0['Level0Name'] == v]
            ##df_by_Level0NameCum['Numerator'] = df_by_Level0NameCum['Numerator'].cumsum()
            ##df_by_Level0NameCum['Denominator'] = df_by_Level0NameCum['Denominator'].cumsum()
            df_by_Level0Name = df_by_Level0Name.assign(NumeratorCum=lambda df_by_Level0Name: df_by_Level0Name.Numerator.cumsum())
            df_by_Level0Name = df_by_Level0Name.assign(DenominatorCum=lambda df_by_Level0Name: df_by_Level0Name.Denominator.cumsum())
            y2 = eval(eval(dataframe0[1]))
            d.append(dict(
                eval(dataframe0[0]),
                x=eval(dataframe0[0]).Period_int, 
                cumulative_enabled=True,
                y=y2, 
                text=y2,
                text_auto=True,
                customdata=eval(dataframe0[0]).LevelName_0,
                mode=linesormarkers(GrainSelect),
                opacity=1,
                marker=dict(
                    size = 5,
                    color=eval(dataframe0[0]).LevelColor_0,
                    color_discrete_map='identity', 
                    line=dict(width=0.1,
                             color = 'white'
                               )
                ),
                type="line",
                name=v,
                line= dict(
                    width=5,
                    shape="spline",
                    color=Level0NameColor[v],
                ),
              #  fill='tozeroy',
                transforms=[dict(
                    type='aggregate',
                    groups=eval(dataframe0[0]).Period_int,
                    aggregations=[
                        dict(target='Numerator', func=AggregateNumDenom(Calculation)),  # , enabled=True
                        dict(target='Denominator', func=AggregateNumDenom(Calculation))  # , enabled=True
                    ]
                ),
                ]
            ))
    return {
        'data': tracestotal,
        'layout': dict(
            barmode='stack',
            barnorm=eval(PercentageTotalSwitchDEF(PercentageTotalSwitch)),
            xaxis=dict(type='string',
                       title='',
                       autorange=True,
                       showgrid=False,
                       rangeselector=dict(
                           buttons=list([
                               dict(count=1,
                                    label="1m",
                                    step="month",
                                    stepmode="backward"),
                               dict(count=6,
                                    label="6m",
                                    step="month",
                                    stepmode="backward"),
                               dict(count=1,
                                    label="YTD",
                                    step="year",
                                    stepmode="todate"),
                               dict(count=1,
                                    label="1y",
                                    step="year",
                                    stepmode="backward"),
                               dict(count=10,
                                    label="All",
                                    step="year",
                                    stepmode="backward")
                           ])
                       ),
                       rangeslider=dict(
                           visible=False
                       ),
                       gridwidth=0,
                       showline=False,
                       linewidth=0,
                       color=fontcolor,
                       font=dict(
                           size=14,
                       )
                       ),
            yaxis=dict(title='',
                       showline=False,
                       linewidth=0,
                       autorange=True,
                       tickformat=eval(Notation[0]),
                       fixedrange=True,
                       showgrid=False,
                       gridwidth=0.5,
                       color=fontcolor,
                       font=dict(
                           size=14,
                       )
                       ),
            margin={'l': 60, 'b': 45, 't': 33, 'r': 40},
            legend=legend,
            autosize=True,
            plot_bgcolor=graphcolor,
            paper_bgcolor=graphcolor,
            modebar=dict(
                bgcolor='transparent',
                color=BeautifulSignalColor,
            ),
            font=dict(
                size=15,
            ),
            images=dict(
                source="https://raw.githubusercontent.com/cldougl/plot_images/add_r_img/vox.png",
                xref="paper", yref="paper",
                x=1, y=1.05,
                sizex=0.2, sizey=0.2,
                xanchor="right", yanchor="bottom"
            ),
            title=title,
            hovermode='closest',
            transition={'duration': 500},
        )
    },options


@app.callback(
    Output('graph-level1compare', 'figure'),
    [Input('dfl0', 'data'),
     Input('dfl1', 'data'),
     Input("KPISelect", "value"),
     Input("KPIGroupSelect", "value"),
     Input("Level1NameSelect", "value"),
     Input("Level2NameSelect", "value"),
     Input('graphoveralltime', 'clickData'),
     Input("Totaalswitch", "label"),
     Input("breakpoints", "widthBreakpoint"),
    # eval(kpigrouplistinput3[0]),  
     ]
)
def update_level1Graph(data00,data11,KPISelect,KPIGroupSelect,Level1NameSelect,Level2NameSelect,clickData,Totaalswitch,widthBreakpoint): #,hoverData,*args
    data0 = pd.read_json(data00, orient='split')
    data1 = pd.read_json(data11, orient='split')
    dff1tmp = data1 
    dff0tmp = data0 
    dff0tmp['Period_int'] = pd.to_datetime(dff0tmp['Period_int']).dt.tz_localize(None)
    dff1tmp['Period_int'] = pd.to_datetime(dff1tmp['Period_int']).dt.tz_localize(None)
    dff0 = []
    dff1 = []
    if clickData == "{'autosize': True}" or clickData == None:
        dff0.append(dff0tmp)
        dff1.append(dff1tmp)
    else:
        dff0.append(dff0tmp[dff0tmp['Period_int'] == clickData['points'][0]['x']])
        dff1.append(dff1tmp[dff1tmp['Period_int'] == clickData['points'][0]['x']])
    dff0 = dff0[0]
    dff1 = dff1[0]
    tracestotal = []
    traces = []
    traces2 = []
    if widthBreakpoint=='sm':
        title = ''
    else:
        title = dict(text=str(KPISelect) + ' per ',# + Level2Entitytype,
                       # +' -     selected: '+str(Level2NameSelect),
                       font=dict(#family='Montserrat',
                                 size=22,
                                 color=fontcolor,
                        ),
        ) 
    totaaljanee = Totaalloop(Totaalswitch)
    appendList1 = [tracestotal, traces]
    appendList2 = eval(totaaljanee)
    Notation = KPISelectedStyle(KPISelect)
    Calculation = CalculationDEF(KPISelect)
    AggregateNum = NumaggregateDEF(KPISelect)
    AggregateDenom = DenomaggregateDEF(KPISelect)
    for j in dfl1.LevelName_1.unique():
        df_by_Level1Name = dff1[dff1['LevelName_1'] == j]
        x = eval(CalculationLogic1(Calculation))
        for g in appendList1:
            g.append(dict(
                df_by_Level1Name,
                y=df_by_Level1Name.LevelName_1,
                x=x,
                text=x,
                texttemplate="%{value:" + eval(Notation[0]) + "}",
                text_auto=True,
                type='bar',
                marker=dict(
                    color=df_by_Level1Name.LevelColor_1,
                    color_discrete_map='identity',
                ),
                orientation="h",
                name=i,
                transforms=[dict(
                    type='aggregate',
                    groups=df_by_Level1Name.LevelName_1,
                    aggregations=[
                        dict(target='Numerator', func=AggregateNumDenom(Calculation)),  # , enabled=True
                        dict(target='Denominator', func=AggregateNumDenom(Calculation))  # , enabled=True
                    ]
                ),
                ]
            ))
    for j in dfl0.LevelName_0.unique():
        df_by_Level0Name = dff0[dff0['LevelName_0'] == j]
        x2 = eval(CalculationLogic0(Calculation))
        for g in appendList2:
            g.append(dict(
                df_by_Level0Name,
                y=df_by_Level0Name.LevelName_0,
                x=x2,
                text=x2,
                text_auto=True,
                texttemplate="%{value:" + eval(Notation[0]) + "}",  # "%{value:.01%}",
                textformat=eval(Notation[0]),
                type='bar',
                marker=dict(
                    opacity=1,
                    color=df_by_Level0Name.LevelColor_0,
                    color_discrete_map='identity',
                    line=dict(width=0.1,
                              color=df_by_Level0Name.LevelColor_0,
                              color_discrete_map='identity',
                              opacity=1,
                              ),
                ),
                orientation="h",
                name=j,
                transforms=[dict(
                    type='aggregate',
                    groups=df_by_Level0Name.LevelName_0,
                    aggregations=[
                        dict(target='Numerator', func=AggregateNumDenom(AggregateNum)),  
                        dict(target='Denominator', func=AggregateNumDenom(AggregateDenom))  
                    ]
                ),
                ]
            ))
    return {
        'data': tracestotal,
        'layout': dict(
            clickmode='event+select',
            type='bar',
            xaxis=dict(type='string',
                       title='',
                       showgrid=False,
                       gridwidth=0,
                       fixedrange=True,
                       showline=False,
                       tickformat=eval(Notation[0]),
                       visible=False,
                       color=fontcolor,
                       font=dict(
                           size=14,
                       )
                       ),
            yaxis=dict(title='',
                       showline=False,
                       showgrid=False,
                       categoryorder="total ascending",
                       gridwidth=0,
                       color=fontcolor,
                       ),
            margin={'l': 140, 'b': 25, 't': 37, 'r': 40},
            showlegend=False,
            autosize=True,
            plot_bgcolor=graphcolor,
            paper_bgcolor=graphcolor,
            modebar=dict(
                bgcolor='transparent',
                color=BeautifulSignalColor,
            ),
            font=dict(
                size=15,
            ),
            title=title,
            hovermode='closest',
            transition={'duration': 500},
        )
    }


######################################################################################################################
######################################################################################################################
################################################----tab 2 aanmaken----###############################################
######################################################################################################################
######################################################################################################################

#graph-with-slider
@app.callback(
     Output('graph-with-slider', 'figure'),
   # Output('Level2NameSelect','options')],
    [Input('dfl1', 'data'),
     Input('dfl2', 'data'),
     Input('GrainSelect', 'value'),
     Input("KPISelect", "value"),
     Input("KPIGroupSelect", "value"),
    # Input("Level1NameSelect", "value"),
   #  Input("Level2NameSelect", "value"),
     Input("Totaalswitch", "label"),
     Input("CumulativeSwitch", "label"),
     Input("PercentageTotalSwitch", "label"),
     Input("ShowValueSwitch", "label"),
     Input("breakpoints", "widthBreakpoint"),
     #eval(kpigrouplistinput3[0]),  
     ]

)


def update_figure(data11,data22,GrainSelect, KPISelect,KPIGroupSelect,Totaalswitch,CumulativeSwitch,PercentageTotalSwitch,ShowValueSwitch,widthBreakpoint):#,*args
    data1 = pd.read_json(data11, orient='split')
    data2 = pd.read_json(data22, orient='split')
    dff2 = data2 
    dff1 = data1
    if widthBreakpoint=='sm':
        title = ''
    else:
        title = dict(text=str(KPISelect) + ' per ',# + Level2Entitytype,
                       # +' -     selected: '+str(Level2NameSelect),
                       font=dict(#family='Montserrat',
                                 size=22,
                                 color=fontcolor,
                        ),
    )
    if widthBreakpoint=='sm':
        legend=dict(
                    font=dict(
                        size=15,
                        color=fontcolor,
                    ),
                    orientation="h"
                )
    else:
        legend=dict(
                    font=dict(
                        size=15,
                        color=fontcolor,
                    ),
                    yanchor="top",
                    y=1,
                    x=1.01,
                    xanchor="left",
                )
    Level2NameList = dff2['LevelName_2'].unique().tolist()
    options = [{'label': str(i), 'value': str(i)} for i in Level2NameList]
    tracestotal = []
    traces = []
    traces2 = []
    totaaljanee = Totaalloop(Totaalswitch)
    appendList1 = [tracestotal,traces]
    appendList2 = eval(totaaljanee)
    Notation = KPISelectedStyle(KPISelect)
    dataframe = Cumloop1(CumulativeSwitch)
    dataframe2 = Cumloop2(CumulativeSwitch)
    Calculation = CalculationDEF(KPISelect)
    for z in appendList1:
        for i in dff2.LevelName_2.unique():
            df_by_Level2Name = dff2[dff2['LevelName_2'] == i]
         #   print(df_by_Level2Name)
           # df_by_Level2Name.to_csv(r'assets/Attributes/dashboard_data/df_by_Level2Name.csv', index=False)
           # quit()
           ##df_by_Level2NameCum = dff[dff['Level2Name'] == i]
           ##df_by_Level2NameCum['Numerator'] = df_by_Level2NameCum['Numerator'].cumsum()
           ##df_by_Level2NameCum['Denominator'] = df_by_Level2NameCum['Denominator'].cumsum()
            df_by_Level2Name = df_by_Level2Name.assign(NumeratorCum=lambda df_by_Level2Name: df_by_Level2Name.Numerator.cumsum())
            df_by_Level2Name = df_by_Level2Name.assign(DenominatorCum=lambda df_by_Level2Name: df_by_Level2Name.Denominator.cumsum())
            y = eval(eval(dataframe2[1]))
            
            z.append(dict(
                eval(dataframe2[0]),
                x=eval(dataframe2[0]).Period_int, 
                y=y,  
                text=y if ShowValueSwitch == 'True' else '',
                text_auto=True,
                customdata=eval(dataframe2[0]).LevelName_2,
                line=dict(
                    width=2,
                    shape="spline",
                    color=Level2NameColor[i],
                ),
                mode=linesormarkers(GrainSelect),
                marker=dict(
                    size = 5,
                    color=Level2NameColor[i],  
                    line=dict(width=0.1
                    ),
                ),
                type=visualDEF(KPISelect),
                name=i,
                transforms=[dict(
                    type='aggregate',
                    groups=eval(dataframe2[0]).Period_int,
                    aggregations=[
                        dict(target='Numerator', func=AggregateNumDenom(Calculation)),   
                        dict(target='Denominator', func=AggregateNumDenom(Calculation))
                    ]
                ),
                ]
            ))
    for d in appendList2:
        for v in dff1.LevelName_1.unique():
            df_by_Level1Name = dff1[dff1['LevelName_1'] == v]
           ##df_by_Level1NameCum = dff2[dff2['Level1Name'] == v]
           ##df_by_Level1NameCum['Numerator'] = df_by_Level1NameCum['Numerator'].cumsum()
           ##df_by_Level1NameCum['Denominator'] = df_by_Level1NameCum['Denominator'].cumsum()
            df_by_Level1Name = df_by_Level1Name.assign(NumeratorCum=lambda df_by_Level1Name: df_by_Level1Name.Numerator.cumsum())
            df_by_Level1Name = df_by_Level1Name.assign(DenominatorCum=lambda df_by_Level1Name: df_by_Level1Name.Denominator.cumsum())
            y2 = eval(eval(dataframe[1]))
            d.append(dict(
                eval(dataframe[0]),
                x=eval(dataframe[0]).Period_int,  
                cumulative_enabled=True,
                y=y2, 
                text=y2,
                text_auto=True,
                customdata=eval(dataframe[0]).LevelName_1,
                mode=linesormarkers(GrainSelect),
                marker=dict(
                    size = 5,
                    color=eval(dataframe[0]).LevelColor_1,
                    line=dict(width=0.1,
                              color = 'white'
                               )
                ),
                type='line',
                name=v,
                line= dict(
                    width=5,
                    shape="spline",
                    color=Level1NameColor[v],
                ),
                transforms=[dict(
                    type='aggregate',
                    groups=eval(dataframe[0]).Period_int,
                    aggregations=[
                        dict(target='Numerator', func=AggregateNumDenom(Calculation)),    
                        dict(target='Denominator', func=AggregateNumDenom(Calculation)) 
                    ]
                ),
                ]
            ))
    return {
        'data': tracestotal,
        'layout': dict(
            clickmode='event+select',
            barmode='stack',
            barnorm=eval(PercentageTotalSwitchDEF(PercentageTotalSwitch)),
            activeselection = dict(color='red'
                                   ,opacity=0.2),
            xaxis=dict(type='string',
                       title='',
                       rangeselector=dict(
                           buttons=list([
                               dict(count=1,
                                    label="1m",
                                    step="month",
                                    stepmode="backward"),
                               dict(count=6,
                                    label="6m",
                                    step="month",
                                    stepmode="backward"),
                               dict(count=1,
                                    label="YTD",
                                    step="year",
                                    stepmode="todate"),
                               dict(count=1,
                                    label="1y",
                                    step="year",
                                    stepmode="backward"),
                               dict(count=10,
                                    label="All",
                                    step="year",
                                    stepmode="backward")
                           ])
                       ),
                       rangeslider=dict(
                           visible=False,
                           style=dict(
                                opacity=0.4,
                           )
                       ),
                       showgrid=False,
                       gridwidth=0,
                       gridcolor='transparent',
                       showline=False,
                       linewidth=0,
                       color=fontcolor,
                       font=dict(
                           size=12,
                       )
                       ),
            yaxis=dict(title='',
                       showline=False,
                       linewidth=0,
                       tickformat=eval(Notation[0]),
                       showgrid=False,
                       fixedrange=True,
                       gridwidth=0,
                       color=fontcolor,
                       ),
            margin={'l': 60, 'b': 55, 't': 33, 'r': 40},
            autosize=True,
            legend=legend,
            plot_bgcolor=graphcolor,
            paper_bgcolor=graphcolor,
            modebar=dict(
                bgcolor='transparent',
                color=BeautifulSignalColor,
            ),
            font=dict(
                size=15,
              #  color=eval(DBColor[1])
            ),
            images=dict(
                source="https://raw.githubusercontent.com/cldougl/plot_images/add_r_img/vox.png",
                xref="paper", yref="paper",
                x=1, y=1.05,
                sizex=0.2, sizey=0.2,
                xanchor="right", yanchor="bottom"
            ),
            title=title,
            hovermode='closest',
            transition={'duration': 500},
            fixedrange=False,
        )
    }

#graph-level2compare
@app.callback(
    Output('graph-level2compare', 'figure'),
    [Input('dfl1', 'data'),
     Input('dfl2', 'data'),
   #  Input('GrainSelect', 'value'),
     Input("KPISelect", "value"),
     Input("KPIGroupSelect", "value"),
    # Input('graph-with-slider', 'hoverData'),
     Input('graph-with-slider', 'clickData'),
  #   Input('Perioddropdown', 'value'),
    # Input("Level1NameSelect", "value"),
    # Input("Level2NameSelect", "value"),
     Input("Totaalswitch", "label"),
     Input("breakpoints","widthBreakpoint")
    # eval(kpigrouplistinput3[0]),  
     ]
)
def update_level2Graph(data11,data22,KPISelect,KPIGroupSelect,clickData,Totaalswitch,widthBreakpoint):#,*args
    data1 = pd.read_json(data11, orient='split')
    data2 = pd.read_json(data22, orient='split')
    dff2tmp = data2 
    dff1tmp = data1 
    dff1tmp['Period_int'] = pd.to_datetime(dff1tmp['Period_int']).dt.tz_localize(None)
    dff2tmp['Period_int'] = pd.to_datetime(dff2tmp['Period_int']).dt.tz_localize(None)
    dff2 = []
    dff1 = []
    if clickData == {'autosize': True} or clickData == None:
        dff2.append(dff2tmp)
        dff1.append(dff1tmp)
    else:
        dff2.append(dff2tmp[dff2tmp['Period_int'] == clickData['points'][0]['x']])
        dff1.append(dff1tmp[dff1tmp['Period_int'] == clickData['points'][0]['x']])
    dff2 = dff2[0]
    dff1 =  dff1[0]
    tracestotal = []
    traces = []
    traces2 = []
    if widthBreakpoint=='sm':
        title = ''
    else:
        title = dict(text=str(KPISelect) + ' per ',# + Level2Entitytype,
                       # +' -     selected: '+str(Level2NameSelect),
                       font=dict(#family='Montserrat',
                                 size=22,
                                 color=fontcolor,
                        ),
    )
    totaaljanee = Totaalloop(Totaalswitch)
    appendList1 = [tracestotal, traces]
    appendList2 = eval(totaaljanee)
    Notation = KPISelectedStyle(KPISelect)
    Calculation = CalculationDEF(KPISelect)
    AggregateNum = NumaggregateDEF(KPISelect)
    AggregateDenom = DenomaggregateDEF(KPISelect)
    for i in dfl2.LevelName_2.unique():
        df_by_Level2Name = dff2[dff2['LevelName_2'] == i]
        x = eval(CalculationLogic2(Calculation))
        for z in appendList1:
            z.append(dict(
                df_by_Level2Name,
                y=df_by_Level2Name.LevelName_2,
                x=x,
                text=x,
                texttemplate="%{value:"+eval(Notation[0])+"}",#"%{value:.01%}",
                textformat=eval(Notation[0]),
                text_auto=True,
                marker = dict(
                        color=df_by_Level2Name.LevelColor_2,
                        color_discrete_map='identity',
                        line = dict(width=0.1)
                ),
                type='bar',
                orientation="h",
                name=i,
                transforms=[dict(
                    type='aggregate',
                    groups=df_by_Level2Name.LevelName_2,
                    aggregations=[
                        dict(target='Numerator', func=AggregateNumDenom(AggregateNum)),  # , enabled=True
                        dict(target='Denominator', func=AggregateNumDenom(AggregateDenom))  # , enabled=True
                    ]
                ),
                ]
            ))
    for j in dfl1.LevelName_1.unique():
        df_by_Level1Name = dff1[dff1['LevelName_1'] == j]
        x2 = eval(CalculationLogic1(Calculation))
        for g in appendList2:
            g.append(dict(
                df_by_Level1Name,
                y=df_by_Level1Name.LevelName_1,
                x=x2,
                text=x2,
                texttemplate="%{value:" + eval(Notation[0]) + "}",  # "%{value:.01%}",
                textformat=eval(Notation[0]),
                text_auto=True,
                type='bar',
                marker=dict(
                    opacity=1,
                    color=df_by_Level1Name.LevelColor_1,
                    color_discrete_map='identity',
                    line=dict(color=df_by_Level1Name.LevelColor_1,
                              width=0.1
                              ),
                ),
                orientation="h",
                name=j,
                transforms=[dict(
                    type='aggregate',
                    groups=df_by_Level1Name.LevelName_1,
                    aggregations=[
                        dict(target='Numerator', func=AggregateNumDenom(AggregateNum)),  # , enabled=True
                        dict(target='Denominator', func=AggregateNumDenom(AggregateDenom))  # , enabled=True
                    ]
                ),
                ]
            ))
    return {
        'data': tracestotal,
        'layout': dict(
            clickmode='event+select',
            type='bar',
            xaxis=dict(type='string',
                       title='',
                       visible=False,
                       autorange=True,
                       fixedrange=True,
                       showgrid=False,
                       showline=False,
                       gridwidth=0,
                       tickformat=eval(Notation[0]),
                       color=fontcolor,
                       font=dict(
                           size=14,
                       )
                       ),
            yaxis=dict(title='',
                       showline=False,
                       showgrid=False,
                       categoryorder="total ascending",
                       gridwidth=0,
                       color=fontcolor,
                       ),
            margin={'l': 140, 'b': 25, 't': 37, 'r': 40},
            showlegend=False,
            plot_bgcolor=graphcolor,
            paper_bgcolor=graphcolor,
            modebar=dict(
                bgcolor='transparent',
                color=BeautifulSignalColor,
            ),
            font=dict(
                size=15,
            ),
            title=title,
            hovermode='closest',
            transition={'duration': 500},
        )
    }


######################################################################################################################
######################################################################################################################
################################################----comparetegel aanmaken----###############################################
######################################################################################################################
######################################################################################################################


#graph-compare-kpi
@app.callback([
    Output('graph-compare-kpi', 'figure'),
    Output('TopImage','src'),
    ],
    [Input('dfl0', 'data'),
     Input('dfl1', 'data'),
     Input('dfl2', 'data'),
     Input('GrainSelect', 'value'),
     Input("KPISelect", "value"),
     Input("KPIGroupSelect", "value"),
     Input("KPISelectCompare", "value"),
     Input("Level1NameSelect", "value"),
     Input("Level2NameSelect", "value"),
     Input('tabsdrilldown','active_tab'),
    # eval(kpigrouplistinput3[0]),  
     ]
)


def update_kpicompare(data00,data11,data22,GrainSelect, KPISelect,KPIGroupSelect, KPISelectCompare,Level1NameSelect, Level2NameSelect,tabsdrilldown):#,*args
    data0 = pd.read_json(data00, orient='split')
    data1 = pd.read_json(data11, orient='split')
    data2 = pd.read_json(data22, orient='split')
    if tabsdrilldown == 'tab-0':
        dfftmp = pd.DataFrame(update_filter_l0(data0, GrainSelect, KPISelect))
        dffcomptmp = pd.DataFrame(update_filter_compare_l0(dfl0Compare, GrainSelect, KPISelectCompare))
        TopImageName = dfftmp['LevelName_0'].unique().astype(str)
    elif tabsdrilldown == 'tab-1':
        dfftmp = pd.DataFrame(update_filter_l1(data1, GrainSelect, KPISelect,Level1NameSelect))
        dffcomptmp = pd.DataFrame(update_filter_compare_l1(dfl1Compare, GrainSelect, KPISelectCompare, Level1NameSelect))
        if dfftmp['LevelName_1'].nunique() == 1:
            TopImageName = dfftmp['LevelName_1'].unique().astype(str)
        else:
            TopImageName = dfftmp['LevelName_1'].unique().astype(str)
    elif tabsdrilldown == 'tab-2':
        dfftmp = pd.DataFrame(update_filter_l2(data2, GrainSelect, KPISelect,Level1NameSelect, Level2NameSelect))
        dffcomptmp = pd.DataFrame(update_filter_compare_l2(dfl2Compare, GrainSelect, KPISelectCompare, Level1NameSelect, Level2NameSelect))
        if dfftmp['LevelName_2'].nunique() == 1:
            TopImageName = dfftmp['LevelName_2'].unique().astype(str)
        else:
            TopImageName = dfftmp['LevelName_1'].unique().astype(str)
    else:
        dfftmp = pd.DataFrame(update_filter_l0(data0, GrainSelect, KPISelect))
        dffcomptmp = pd.DataFrame(update_filter_compare_l0(dfl0Compare, GrainSelect, KPISelectCompare))
        TopImageName = dfftmp['LevelName_0'].unique().astype(str)
    TopImageURL = f'assets/attributes/Images/sythetix.png' 
    TopImageURLCheck =[]
    if os.path.exists(TopImageURL):
        TopImageURLCheck.append(TopImageURL)
    else:
        TopImageURLCheck.append('assets/Attributes/Images/synthetix.png')
    TopImage= 'data:image/png;base64,{}'.format(base64.b64encode(open(TopImageURLCheck[0], 'rb').read()).decode())
    AggregateNum = NumaggregateDEF(KPISelect)
    AggregateDenom = DenomaggregateDEF(KPISelect)
    AggregateNumcomp = NumaggregateDEF(KPISelectCompare)
    AggregateDenomcomp = DenomaggregateDEF(KPISelectCompare)
    dfftmp.fillna(value=0, inplace=True)
    dffcomptmp.fillna(value=0, inplace=True)
    dff = dfftmp.groupby(columnsdftotal, as_index=False, sort=False).agg(
        {'Denominator': [eval(AggregateNumDenom(AggregateDenom))], 'Numerator': [eval(AggregateNumDenom(AggregateNum))], 'Denominator_LP': [eval(AggregateNumDenom(AggregateDenom))], 'Numerator_LP': [eval(AggregateNumDenom(AggregateNum))]},dtype=object);
    dffcomp = dffcomptmp.groupby(columnsdftotal, as_index=False, sort=False).agg(
        {'Denominator': [eval(AggregateNumDenom(AggregateDenomcomp))], 'Numerator': [eval(AggregateNumDenom(AggregateNumcomp))], 'Denominator_LP': [eval(AggregateNumDenom(AggregateDenomcomp))], 'Numerator_LP': [eval(AggregateNumDenom(AggregateNumcomp))]},dtype=object);
    dff.reset_index()
    dffcomp.reset_index()
    dff.columns = dff.columns.droplevel(1)
    dffcomp.columns = dffcomp.columns.droplevel(1)
    tracestotal = []
    traceskpi = []
    traceskpicomp = []
    Notation = KPISelectedStyle(KPISelect)
    NotationComp = KPISelectedStyle(KPISelectCompare)
    KPIList = [KPISelect,KPISelectCompare]
    appendList1 = [tracestotal, traceskpi]
    appendList2 = [tracestotal, traceskpicomp]
    Calculation = CalculationDEF(KPISelect)
    CalculationComp = CalculationDEF(KPISelectCompare)
    ycomp = eval(CalculationLogicTotalCompare(CalculationComp))
    y = eval(CalculationLogicTotal(Calculation))
    for i in appendList1:
        i.append(dict(
            x=dff.Period_int,
            y=y,
            yaxis='y1',
            mode=linesormarkers(GrainSelect),
            opacity=1,
            type='Scatter',
            line=dict(
                width=2,
                shape="spline",
                color='#FFA500'  
            ),
            name=KPIList[0],
            transforms=[dict(
                type='aggregate',
                groups=dff.Period_int,
                aggregations=[
                    dict(target='Numerator', func=AggregateNumDenom(Calculation)),  
                    dict(target='Denominator', func=AggregateNumDenom(Calculation))  
                ]
            ),
            ]
    ))
    for j in appendList2:
        j.append(dict(
            x=dffcomp.Period_int,
            y=ycomp,  
            mode=linesormarkers(GrainSelect),
            showgrid=False,
            yaxis='y2',
            secondary_y=True,
            opacity=1,
            type='line',
            line=dict(
                width=2,
                shape="spline",
                color='#005AFF',
                #               
            ),
           # fill='tozeroy',
            name=KPIList[1],
            transforms=[dict(
                type='aggregate',
                groups=dffcomp.Period_int,
                aggregations=[
                    dict(target='Numerator', func=AggregateNumDenom(CalculationComp)),  # , enabled=True
                    dict(target='Denominator', func=AggregateNumDenom(CalculationComp))  # , enabled=True
                ]
        ),
        ]
    ))
    return {
        'data': tracestotal,
        'layout': dict(
            xaxis=dict(type='string',
                       title='',
                       rangeselector=dict(
                           buttons=list([
                               dict(count=1,
                                    label="1m",
                                    step="month",
                                    stepmode="backward"),
                               dict(count=6,
                                    label="6m",
                                    step="month",
                                    stepmode="backward"),
                               dict(count=1,
                                    label="YTD",
                                    step="year",
                                    stepmode="todate"),
                               dict(count=1,
                                    label="1y",
                                    step="year",
                                    stepmode="backward"),
                               dict(step="all")
                           ])
                       ),
                       rangeslider=dict(
                            visible=False
                       ),
                     
                       showgrid=False,
                       showline=False,
                       color=fontcolor,
                       font=dict(
                           size=14,
                       )
                       ),
            yaxis=dict(
                       fixedrange=False,
                       linecolor='#FFA500',# kpicolorDEF(KPISelect),
                       showline=True,
                       linewidth=2,
                       showgrid=False,
                       tickformat=eval(Notation[0]),
                       yaxis='y1',
                       secondary_y=False,
                       color=fontcolor,
                       tickcolor='#FFA500'
                       ),
            yaxis2=dict(
                       fixedrange=False,
                       showline=True,
                       showgrid=False,
                       font=dict(color='#005AFF'),
                       linecolor='#005AFF',
                       linewidth=2,
                       tickformat=eval(NotationComp[0]),
                       tickcolor='#005AFF',
                       yaxis='y2',
                       secondary_y=True,
                       overlaying="y",
                       color=fontcolor,
                       side="right"
                       ),
            margin={'l': 60, 'b': 45, 't': 33, 'r': 60},
            secondary_y=True,
            legend=dict(
                font=dict(
                    size=15,
                    color=fontcolor,
                ),
                orientation="h",
                yanchor="top",
                y=0.99,
                x=0.01,
                xanchor="left",
            ),
            plot_bgcolor=graphcolor,
            paper_bgcolor=graphcolor,
            modebar=dict(
                bgcolor='transparent',
                color=BeautifulSignalColor,
            ),
            font=dict(
                size=15,
            ),
            title=dict(text=str(KPISelect) + ' over time per vergeleken met ' + str(KPISelectCompare),# + ' ' + Level2Entitytype,
                       # +' -     selected: '+str(Level2NameSelect),
                       font=dict(
                                 size=22,
                                 color=fontcolor,
                           ),
                       ),
            hovermode='closest',
            transition={'duration': 500},
            autosize=True,
        )
    },TopImage


#graph-compare-kpi2
@app.callback(
    Output('graph-compare-kpi2', 'figure')
    ,
    [Input('dfl0', 'data'),
     Input('dfl1', 'data'),
     Input('dfl2', 'data'),
     Input('GrainSelect', 'value'),
     Input("KPISelect", "value"),
     Input("KPIGroupSelect", "value"),
     Input("KPISelectCompare", "value"),
     Input("Level1NameSelect", "value"),
     Input("Level2NameSelect", "value"),
     Input('tabsdrilldown','active_tab'),
     Input('dffcomparefilter', 'data'),
     #eval(kpigrouplistinput3[0]),  
     ]
)


def update_kpicompare(data00,data11,data22,GrainSelect, KPISelect,KPIGroupSelect, KPISelectCompare,Level1NameSelect, Level2NameSelect,tabsdrilldown,dflcomparekpi):#,*args
    dffcomparefilter = pd.read_json(dflcomparekpi, orient='split')
    data0 = pd.read_json(data00, orient='split')
    data1 = pd.read_json(data11, orient='split')
    data2 = pd.read_json(data22, orient='split')
    dfftmp = dffcomparefilter
    #if tabsdrilldown == 'tab-0':
    #    dfftmp = pd.DataFrame(update_filter_l0(data0, GrainSelect, KPISelect))
    #    dffcomptmp = pd.DataFrame(update_filter_compare_l0(dfl0Compare, GrainSelect, KPISelectCompare))
    #elif tabsdrilldown == 'tab-1':
    #    dfftmp = pd.DataFrame(update_filter_l1(data1, GrainSelect, KPISelect,Level1NameSelect))
    #    dffcomptmp = pd.DataFrame(update_filter_compare_l1(dfl1Compare, GrainSelect, KPISelectCompare, Level1NameSelect))
    #elif tabsdrilldown == 'tab-2':
    #    dfftmp = pd.DataFrame(update_filter_l2(data2, GrainSelect, KPISelect,Level1NameSelect, Level2NameSelect))
    #    dffcomptmp = pd.DataFrame(update_filter_compare_l2(dfl2Compare, GrainSelect, KPISelectCompare, Level1NameSelect, Level2NameSelect))
    #else:
    #    dfftmp = pd.DataFrame(update_filter_l0(data0, GrainSelect, KPISelect))
    #    dffcomptmp = pd.DataFrame(update_filter_compare_l0(dfl0Compare, GrainSelect, KPISelectCompare))
    AggregateNum = NumaggregateDEF(KPISelect)
    AggregateDenom = DenomaggregateDEF(KPISelect)
    dfftmp.fillna(value=0, inplace=True)
   
    dff = dfftmp.groupby(columnsdftotal, as_index=False, sort=False).agg(
        {'Denominator': [eval(AggregateNumDenom(AggregateDenom))], 'Numerator': [eval(AggregateNumDenom(AggregateNum))], 'Denominator_LP': [eval(AggregateNumDenom(AggregateDenom))], 'Numerator_LP': [eval(AggregateNumDenom(AggregateNum))]},dtype=object)
    dff.reset_index() 
    dff.columns = dff.columns.droplevel(1)
    appendList1 = []
    Calculation = CalculationDEF(KPISelect)
    y = eval(CalculationLogicTotal(Calculation))
    dff['pct_changed_tmp'] = y
    for i in dff.d_kpi_id.unique():
        Calculation = CalculationDEF(KPISelect)
        df_filtered_kpi = dff[dff['d_kpi_id'] == i]
        df_filtered_kpi['pct_changed'] = df_filtered_kpi['pct_changed_tmp'].pct_change()
        appendList1.append(dict(
            x=df_filtered_kpi.Period_int,
            y=df_filtered_kpi.pct_changed,
            yaxis='y1',
            mode=linesormarkers(GrainSelect),
            opacity=1,
            type='Scatter',
            line=dict(
                width=2,
                shape="spline",
                #color='#FFA500'  
            ),
            name=i,
            #transforms=[dict(
            #    type='aggregate',
            #    groups=df_filtered_kpi.Period_int,
            #    aggregations=[
            #        dict(target='Numerator', func=AggregateNumerator(Calculation)),  
            #        dict(target='Denominator', func=AggregateDenominator(Calculation))  
            #    ]
            #),
            #]
    ))
    return {
        'data': appendList1,
        'layout': dict(
            xaxis=dict(type='string',
                       title='',
                       rangeselector=dict(
                           buttons=list([
                               dict(count=1,
                                    label="1m",
                                    step="month",
                                    stepmode="backward"),
                               dict(count=6,
                                    label="6m",
                                    step="month",
                                    stepmode="backward"),
                               dict(count=1,
                                    label="YTD",
                                    step="year",
                                    stepmode="todate"),
                               dict(count=1,
                                    label="1y",
                                    step="year",
                                    stepmode="backward"),
                               dict(step="all")
                           ])
                       ),
                       rangeslider=dict(
                            visible=False
                       ),
                     
                       showgrid=False,
                       showline=False,
                       color=fontcolor,
                       font=dict(
                           size=14,
                       )
                       ),
            yaxis=dict(
                       fixedrange=False,
                       showline=True,
                       linewidth=2,
                       showgrid=False,
                       tickformat=".1%",
                       yaxis='y1',
                       secondary_y=False,
                       color=fontcolor,
                       ),
            margin={'l': 60, 'b': 45, 't': 33, 'r': 60},
            legend=dict(
                font=dict(
                    size=15,
                    color=fontcolor,
                ),
                orientation="h",
                yanchor="top",
                y=0.99,
                x=0.01,
                xanchor="left",
            ),
            plot_bgcolor=graphcolor,
            paper_bgcolor=graphcolor,
            modebar=dict(
                bgcolor='transparent',
                color=BeautifulSignalColor,
            ),
            font=dict(
                size=15,
            ),
            title=dict(text=str(KPISelect) + ' over time per vergeleken met ' + str(KPISelectCompare),# + ' ' + Level2Entitytype,
                       # +' -     selected: '+str(Level2NameSelect),
                       font=dict(
                                 size=22,
                                 color=fontcolor,
                           ),
                       ),
            hovermode='closest',
            transition={'duration': 500},
            autosize=True,
        )
    }

#app.config['suppress_callback_exceptions'] = True



if __name__ == "__main__":
    print('application loaded')
    app.run_server(debug=True) #,config=config


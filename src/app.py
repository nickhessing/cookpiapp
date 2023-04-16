
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
from dash import Dash,DiskcacheManager, CeleryManager, dcc, html, Input, Output, State, MATCH, ALL, ctx
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
import json
#from dash_extensions.callback import CallbackCache, DiskCache
import base64
import time
from uuid import uuid4
import polars as pl
from dash_extensions.enrich import RedisStore,DashProxy, Output, Input, State, ServersideOutput, html, dcc,FileSystemStore,ServersideOutputTransform
#from flask_caching import Cache
import redis

external_stylesheets = [
{
    'href': 'https://fonts.googleapis.com/icon?family=Material+Icons',
    'rel': 'stylesheet',
},
]

print('starttheshow')

#my_backend = RedisStore(redis_url=os.environ['redis://red-cgs78qpjvhtitjuma0tg:6379'])
print(os.environ)
# Connect to your internal Redis instance using the REDIS_URL environment variable
# The REDIS_URL is set to the internal Redis URL e.g. redis://red-343245ndffg023:6379

#if 'redis://red-cgr84kgrddl6f7enda00:6379' in os.environ:
    # Use Redis & Celery if REDIS_URL set as an env variable
#from celery import Celery
#celery_app = Celery(__name__, broker=os.environ['redis://red-cgr84kgrddl6f7enda00:6379']) #, backend=os.environ['redis://red-cgr84kgrddl6f7enda00:6379']
#background_callback_manager = CeleryManager(celery_app)
#r = redis.from_url(os.environ['redis://red-cgr84kgrddl6f7enda00:6379'])
#r.set('key', 'redis-py')
#r.get('key')

#else:
#    # Diskcache for non-production apps when developing locally
#    import diskcache
#    cache = diskcache.Cache("./cache")
#    background_callback_manager = DiskcacheManager(cache)

#app = dash.Dash(__name__,suppress_callback_exceptions=True)#background_callback_manager=background_callback_manager
app = DashProxy(__name__,
                transforms=[ServersideOutputTransform(arg_check=False)]#backend = RedisStore(),
              #  ,background_callback_manager=background_callback_manager
                ,suppress_callback_exceptions=True,external_stylesheets=external_stylesheets)#

server = app.server
app.secret_key = os.getenv('redis://red-cgs78qpjvhtitjuma0tg:6379', "super-secret")

app.css.config.serve_locally = True

#CACHE_CONFIG = {
#    # try 'FileSystemCache' if you don't want to setup redis
#    'CACHE_TYPE': 'redis',
#    'CACHE_REDIS_URL': os.environ.get('REDIS_URL', 'redis://localhost:6379')
#}
#cache = Cache()
#cache.init_app(app.server, config=CACHE_CONFIG)

#my_backend = FileSystemStore(cache_dir="C:/Users/nickh/OneDrive/Documents/Projects/cookkpi/dashboard/src/assets/Attributes/redis")

"""
launch_uid = uuid4()

if 'REDIS_URL' in os.environ:
    # Use Redis & Celery if REDIS_URL set as an env variable
    from celery import Celery
    celery_app = Celery(__name__, broker=os.environ['REDIS_URL'], backend=os.environ['REDIS_URL'])
    background_callback_manager = CeleryManager(
        celery_app, cache_by=[lambda: launch_uid], expire=60
    )

else:
    # Diskcache for non-production apps when developing locally
    import diskcache
    cache = diskcache.Cache("./cache")
    background_callback_manager = DiskcacheManager(
        cache, cache_by=[lambda: launch_uid], expire=60
    )

"""

BeautifulSignalColor="#f3f6d0"
ProjectOrange="#b37400"
Highlightcardcolor="#f3f6d0"
graphcolor="#243b55" #8EC5FC #tbv export
fontcolor='rgb(247, 239, 213)'  #141e30
buttoncolor="#f3f6d0"
buttonlogocolor="#020b15"
slides_to_show_ifenough = 4
slides_to_scroll = 4
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

cookpi_attributestmp = pd.read_excel(open('assets/Attributes/dashboard_data/cookpi_per_pi.xlsx', 'rb'),
              sheet_name='linktable')
#KPIFramework = pd.DataFrame(
#        pd.read_csv(r'assets/Attributes/dashboard_data/KPIFrameworkEnd.csv',sep=',', decimal='.',low_memory=False))

#
#KPIIDList =  cookpi_attributestmp['d_kpi_id'].unique()
#
#KPIFrameworklist =[]
#
#for i in KPIIDList:
#    KPIFrameworkloop = KPIFrameworktmp[(KPIFrameworktmp.d_kpi_id ==i)]
#    cookpi_attributes = cookpi_attributestmp[(cookpi_attributestmp.d_kpi_id == i)]
#    sheettmp = cookpi_attributes[(cookpi_attributes.Level_ID_present =="d_level0_id")] 
#    sheettmpl1 = cookpi_attributes[(cookpi_attributes.Level_ID_present =="d_level1_id")] 
#    sheettmpl2 = cookpi_attributes[(cookpi_attributes.Level_ID_present =="d_level2_id")] 
#    rename = dict(sheettmp.set_index('Level_ID')['Level_ID_present'].to_dict()) 
#    renamel1 = dict(sheettmpl1.set_index('Level_ID')['Level_ID_present'].to_dict()) 
#    renamel2 = dict(sheettmpl2.set_index('Level_ID')['Level_ID_present'].to_dict()) 
#    rename_dict = {}
#    rename_dict.update(rename)
#    rename_dict.update(renamel1)
#    rename_dict.update(renamel2)
#    KPIFrameworkloop.rename(columns=rename_dict, inplace = True)
#    KPIFrameworklist.append(KPIFrameworkloop)
#
#KPIFramework = pd.concat(KPIFrameworklist)

#KPIFramework['d_level0_id']=KPIFramework['d_level0_id'].astype(int)
#KPIFramework['d_level1_id']=KPIFramework['d_level1_id'].astype(int)
#KPIFramework['d_level2_id']=KPIFramework['d_level2_id'].astype(int)

d_kpi_tmp = pd.read_excel(open('assets/Attributes/dashboard_data/cookpi_per_pi.xlsx', 'rb'),
              sheet_name='d_kpi')
              
Project = pd.DataFrame(pd.read_excel(open('assets/Attributes/dashboard_data/cookpi_per_pi.xlsx', 'rb'),
              sheet_name='Project'))
Project["Filter1"].fillna("Overig", inplace = True)      

Blockchain = pd.DataFrame(pd.read_excel(open('assets/Attributes/dashboard_data/cookpi_per_pi.xlsx', 'rb'),
              sheet_name='Blockchain'))
Blockchain["Filter1"].fillna("Overig", inplace = True)   

kpilevelcount = cookpi_attributestmp.groupby(['d_kpi_id'])['d_kpi_id'].count().reset_index(name="kpilevelcount")
d_kpi = d_kpi_tmp[(d_kpi_tmp.live == 1)] #& (df.carrier == "B6")
d_kpi = d_kpi.merge(kpilevelcount)

d_kpi.sort_values(by=['Sorting'])

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
dfl0polars = pl.read_csv(r"assets/Attributes/dashboard_data/dfl0.csv")
dfl1polars = pl.read_csv(r"assets/Attributes/dashboard_data/dfl1.csv")
dfl2polars = pl.read_csv(r"assets/Attributes/dashboard_data/dfl2.csv")

"""
dfl0 = pd.DataFrame(
        pd.read_csv(r'assets/Attributes/dashboard_data/dfl0.csv',sep=',', decimal='.',low_memory=False))
dfl0Compare = dfl0


dfl1 = pd.DataFrame(

        pd.read_csv(r'assets/Attributes/dashboard_data/dfl1.csv',sep=',', decimal='.',low_memory=False))
dfl1Compare = dfl1


dfl2 = pd.DataFrame(
        pd.read_csv(r'assets/Attributes/dashboard_data/dfl2.csv',sep=',', decimal='.',low_memory=False))
dfl2Compare = dfl2
"""

GrainNameListtmp = pl.DataFrame(dfl0polars["Grain"].unique())
tmp =GrainNameListtmp.rows(named=True)
GrainNameList = [i['Grain'] for i in tmp] 
#Level0NameList = dfl0['LevelName_0'].unique()
Level0NameListtmp = pl.DataFrame(dfl0polars["LevelName_0"].unique())
tmp =Level0NameListtmp.rows(named=True)
Level0NameList = [i['LevelName_0'] for i in tmp] 

Level1NameListtmp = pl.DataFrame(dfl1polars["LevelName_1"].unique())
tmp =Level1NameListtmp.rows(named=True)
Level1NameList = [i['LevelName_1'] for i in tmp] 

Level2NameListtmp = pl.DataFrame(dfl2polars["LevelName_2"].unique())
tmp =Level2NameListtmp.rows(named=True)
Level2NameList = [i['LevelName_2'] for i in tmp] 

#Level1NameList = dfl1['LevelName_1'].unique()
#Level2NameList = dfl2['LevelName_2'].unique().tolist()

Level0Name = dfl0polars.select(['LevelEntitytype_0','LevelName_0','LevelColor_0','KPIName','Filter1_0']).unique()
Level1Name = dfl1polars.select(['LevelEntitytype_1','LevelName_1','LevelColor_1','KPIName','Filter1_1']).unique()
Level2Name = dfl2polars.select(['LevelEntitytype_2','LevelName_2','LevelColor_2','KPIName','Filter1_2']).unique()

dfl0polars.drop_in_place("LevelColor_0")
dfl0polars.drop_in_place("LevelEntitytype_0")
dfl0polars.drop_in_place("LevelDescription_0")
dfl0polars.drop_in_place("KPIType")
dfl0polars.drop_in_place("Denominator_LP")
dfl0polars.drop_in_place("Numerator_LP")

dfl1polars.drop_in_place("LevelColor_1")
dfl1polars.drop_in_place("LevelEntitytype_1")
dfl1polars.drop_in_place("LevelDescription_1")
dfl1polars.drop_in_place("KPIType")
dfl1polars.drop_in_place("Denominator_LP")
dfl1polars.drop_in_place("Numerator_LP")

dfl2polars.drop_in_place("LevelColor_2")
dfl2polars.drop_in_place("LevelEntitytype_2")
dfl2polars.drop_in_place("LevelDescription_2")
dfl2polars.drop_in_place("KPIType")
dfl2polars.drop_in_place("Denominator_LP")
dfl2polars.drop_in_place("Numerator_LP")

#Level0Name = dfl0[['LevelEntitytype_0','LevelName_0','LevelColor_0','KPIName','Filter1_0']]
#Level1Name = dfl1[['LevelEntitytype_1','LevelName_1','LevelColor_1','KPIName','Filter1_1']]
#Level2Name = dfl2[['LevelEntitytype_2','LevelName_2','LevelColor_2','KPIName','Filter1_2']]
#Category1List = Level0Name['Filter1_0'].unique()

Category1Listtmp = pl.DataFrame(dfl0polars["Filter1_0"].unique())
tmp =Category1Listtmp.rows(named=True)
Category1List = [i['Filter1_0'] for i in tmp] 

#Level0Name = Level0Name.drop_duplicates()
#Level1Name = Level1Name.drop_duplicates()
#Level2Name = Level2Name.drop_duplicates()

Level0NameColortmp = Level0Name.select(['LevelName_0','LevelColor_0'])
Level0NameColor =Level0NameColortmp.rows(named=True)
Level0NameColor = {level['LevelName_0']: level['LevelColor_0'] for level in Level0NameColor}
#Level0NameColor = dict(Level0Name.set_index('LevelName_0')['LevelColor_0'].to_dict())
Level1NameColortmp = Level1Name.select(['LevelName_1','LevelColor_1'])
Level1NameColor =Level1NameColortmp.rows(named=True)
Level1NameColor = {level['LevelName_1']: level['LevelColor_1'] for level in Level1NameColor}

Level2NameColortmp = Level2Name.select(['LevelName_2','LevelColor_2'])
Level2NameColor =Level2NameColortmp.rows(named=True)
Level2NameColor = {level['LevelName_2']: level['LevelColor_2'] for level in Level2NameColor}

Level0attrtmp = Level0Name.select(['KPIName','LevelEntitytype_0'])
Level0attr =Level0attrtmp.rows(named=True)
Level0attr = {level['KPIName']: level['LevelEntitytype_0'] for level in Level0attr}

Level1attrtmp = Level1Name.select(['KPIName','LevelEntitytype_1'])
Level1attr =Level1attrtmp.rows(named=True)
Level1attr = {level['KPIName']: level['LevelEntitytype_1'] for level in Level1attr}

Level2attrtmp = Level2Name.select(['KPIName','LevelEntitytype_2'])
Level2attr =Level2attrtmp.rows(named=True)
Level2attr = {level['KPIName']: level['LevelEntitytype_2'] for level in Level2attr}

#Level0attr = dict(Level0Name.set_index('KPIName')['LevelEntitytype_0'].to_dict())
#Level1attr = dict(Level1Name.set_index('KPIName')['LevelEntitytype_1'].to_dict())
#Level2attr = dict(Level2Name.set_index('KPIName')['LevelEntitytype_2'].to_dict())


KPINameListCompare = d_kpi['KPIName'].unique()
KPINameToID = dict(d_kpi.set_index('KPIName')['d_kpi_id'].to_dict())
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

#columnsdftotal = KPIFramework.columns.tolist()
#columnsdftotal.remove('d_level0_id')
#columnsdftotal.remove('d_level1_id')
#columnsdftotal.remove('d_level2_id')
#columnsdftotal.remove('Numerator')
#columnsdftotal.remove('Denominator')
#columnsdftotal.remove('Numerator_LP')
#columnsdftotal.remove('Denominator_LP')
#columnsdftotal.remove('Period_int_lp')

kpicountout = [len(KPINameList)]
kpigroupcountout = [len(KPIGroupList)]
KPIattributes =[]

pd.set_option('display.expand_frame_repr', False)

template_theme1 = "stylesheet.css"
template_theme2 = "stylesheet2.css"

css_directory = os.getcwd()
stylesheets = ['stylesheet.css']
static_css_route = '/static/'




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
        value=KPIGroupList,
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
)


Category1 = html.Div([
    html.Div(dcc.Textarea(value='Category',id='Category1txt',className='h6')),
    dcc.Dropdown(
    id="Category1Select",
    options=[{'label': html.Span([i],style={'background-color': ProjectOrange}), 'value': i}  for i in Category1List],#
    multi=True,
    optionHeight=1,
    placeholder="Select a value",
    value=Category1List,#'Derivatives',
),
],id="Category1"
)

#@app.callback(
#    Output('Category1Select', 'value'),
#    [Input('sweepl0filter', 'n_clicks'),
#    ]
#)
#
#def reset_filter0(n_clicks):#,n_clicks2
#    print('removefilterl0')
#    filterl0 = [{'label': html.Span([i],style={'background-color': ProjectOrange}), 'value': i}  for i in Category1List]
#    print(filterl0)
#    return filterl0


Level0DD = html.Div([
    html.Div(dcc.Textarea(value='Level zero filters',id='dropdown0',className='h6')),
    dcc.Dropdown(
    id="Level0NameSelect",
    options=[{'label': html.Span([i],style={'background-color': Level0NameColor[i]}), 'value': i} for i in Level0NameList],#, 'style': {'backgroundColor': Level0NameColor[i]}
    multi=True,
    optionHeight=1,
    placeholder="Select a value",
    value=Level0NameList,
),
],id="Level0DD"
)


Level1DD = html.Div([
    html.Div(dcc.Textarea(value='Level one filters',id='dropdown1',className='h6')),
    dcc.Dropdown(
        id="Level1NameSelect",
        options=[{'label': html.Span([i],style={'background-color': Level1NameColor[i]}), 'value': i} for i in Level1NameList],#, 'style': {'backgroundColor': Level0NameColor[i]}
        multi=True,
        optionHeight=1,
        placeholder="Select a value",
        value=Level1NameList,
),
],id="Level1DD"
)

@app.callback(
    Output('graphoveralltime', 'selectedData'),
    [Input('sweepl1', 'n_clicks'),
     #Input({'type': 'filter-dropdown-ex3-reset', 'index': ALL}, 'n_clicks'),
    ], session_check=False, prevent_initial_call=True
)

def reset_clickDatal1(n_clicks):#,n_clicks2
    print('removefilterl1')
    return None


@app.callback([
              Output("Level1NameSelect", "value"),
             ],             
              Input('graph-level1compare', 'selectedData'),
              Input('sweepl1', 'n_clicks'),
              Input("Level1NameSelect", "value"),
              Input({'type': 'filter-dropdown-ex3-reset', 'index': ALL}, 'n_clicks'), prevent_initial_call=True
             )
def Level1Update(selecteddatal1bar,n_clicks,Level1NameSelect,reset):#,selecteddatal0,n_clicks,KPINameSelect,clickdatal0bar,clickdatal0
    print('Level1Update')
    selectedlistl1bar_list =[]
    selectedlistl1bar_list.clear()
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    changed_id2 = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    try:
        if 'sweepl1' in changed_id:
            selectedlistl1bar_list.clear()
            for d in Level1NameList:
                selectedlistl1bar_list.append(d)
        elif selecteddatal1bar['points']:
            selectedlistl1bar_list.clear()
            for p in selecteddatal1bar['points']:
                selectedlistl1bar_list.append(p['y'])
        elif "filter-dropdown-ex3-reset" in list(json.loads(changed_id2).values()):
            selectedlistl1bar_list.clear()
            for j in Level1NameList:
                selectedlistl1bar_list.append(j)
    except:
        print()
    if len(selectedlistl1bar_list)>0:
        return selectedlistl1bar_list
    else:
        raise dash.exceptions.PreventUpdate


Level2DD = html.Div([
    html.Div(dcc.Textarea(value='Level two filters',id='dropdown2',className='h6')),
    dcc.Dropdown(
        id="Level2NameSelect",
        options=[{'label': html.Span([i],style={'background-color': Level2NameColor[i]}), 'value': i} for i in Level2NameList],
        multi=True,
        placeholder="Select a value",
        value=Level2NameList,
),
],id="Level2DD"
)

@app.callback(
    Output('graph-with-slider', 'selectedData'),
    [Input('sweepl2', 'n_clicks'),
     #Input({'type': 'filter-dropdown-ex3-reset', 'index': ALL}, 'n_clicks'),
    ], session_check=False, prevent_initial_call=True
)

def reset_clickDatal2(n_clicks):#,n_clicks2
    print('removefilterl2')
    return None


@app.callback([
              Output("Level2NameSelect", "value"),
             ],             
              Input('graph-level2compare', 'selectedData'),
              Input('sweepl2', 'n_clicks'),
              Input("Level2NameSelect", "value"),
              Input({'type': 'filter-dropdown-ex3-reset', 'index': ALL}, 'n_clicks'), prevent_initial_call=True
             )
def Level2Update(selecteddatal2bar,n_clicks,Level2NameSelect,reset):#,selecteddatal0,n_clicks,KPINameSelect,clickdatal0bar,clickdatal0
    print('Level2Update')
    selectedlistl2bar_list =[]
    selectedlistl2bar_list.clear()
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    changed_id2 = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    try:
        if 'sweepl2' in changed_id:
            selectedlistl2bar_list.clear()
            for d in Level2NameList:
                selectedlistl2bar_list.append(d)
        elif selecteddatal2bar['points']:
            selectedlistl2bar_list.clear()
            for p in selecteddatal2bar['points']:
                selectedlistl2bar_list.append(p['y'])
        elif "filter-dropdown-ex3-reset" in list(json.loads(changed_id2).values()):
            selectedlistl2bar_list.clear()
            for j in Level2NameList:
                selectedlistl2bar_list.append(j)
    except:
        print()
    if len(selectedlistl2bar_list)>0:
        return selectedlistl2bar_list
    else:
        return Level2NameSelect
    

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


#navbarlist =[]
#navbarlist.append(
#        f"""html.Li(html.A([
#                html.I('category',className='material-icons icon'),
#                html.Span('All categories',className='text nav-text')],href='#',id='kpigroup0')
#                ,className='nav-link')"""
#)
#
#for i in range(kpigroupcountout[0]):
#    numbertmp= i
#    numberidtmp= i+1
#    GroupImage2 = GroupImage[numbertmp]
#    KPIGroupList2 = KPIGroupList[numbertmp]
#    number=str(numbertmp)
#    numberid=str(numberidtmp)
#    navbarlist.append(
#        f"""html.Li(html.A([
#                html.I('{GroupImage2}',className='material-icons icon'),
#                html.Span('{KPIGroupList2}',className='text nav-text')],href='#',id='kpigroup{numberidtmp}')
#                ,className='nav-link')"""
#    )
#navbarlist2=','.join(navbarlist)
#
#navbar = html.Nav([html.Header([
#                    html.Div([
#                        html.Div(Radiograin,className="col-sm-12 col-md-12 col-lg-12 col-xl-12 text logo-text")
#                    ],className="image-text"),
#                    html.I("chevron_right",className='material-icons toggle',id='Opennavbar')
#                    ]),
#                    html.Div([
#                        html.Div([
#                          html.Div(html.Span("Performace category",className='text nav-text')),
#                          html.Ul(eval(navbarlist2)
#                            ,className='menu-links'
#                            )
#                        ],className='menu'
#                    ),
#                    html.Div([
#                     html.Div([
#                          html.Div(html.Span("Performace view",className='text nav-text')),
#                          html.Ul([
#                            html.Li(html.A(
#                                [html.I("lan",className='material-icons icon'),
#                                 html.Span("Drill down",className='text nav-text')
#                                ],href='/drilldown',id='NavItem1'
#                                ),className='nav-link')
#                            ,
#                            html.Li(html.A(
#                                [html.I("balance",className='material-icons icon'),
#                                 html.Span("Compare",className='text nav-text')
#                                ],href='/compare',id='NavItem2'
#                                ),className='nav-link'
#                            ),
#                            html.Li(html.A(
#                                [html.I("bolt",className='material-icons icon'),
#                                html.Span("Predict",className='text nav-text')
#                                ],href='/predict',id='NavItem3'
#                                ),className='nav-link'
#                            ),
#                    ],className='menu-links'
#                            ),
#                    ],className='menu'),
#                    ])
#                    ],className='menu-bar'),  
#                    ],className="sidebar close",id='nav')


Totaalaggregaatswitch = html.Div([
    html.Div('Compare with total ',className='h6'),
    daq.BooleanSwitch(
        id='Totaalswitch',
        on=False,
        color=ProjectOrange,
        label="Dark",
        labelPosition="left",
    )
])

CumulativeSwitch = html.Div([
    html.Div('Cumulative ',className='h6'),
    daq.BooleanSwitch(
        id='CumulativeSwitch',
        on=False,
        color=ProjectOrange,
        label="Dark",
        labelPosition="left",
    )
])

TargetSwitch = html.Div([
    html.Div('Target ',className='h6'),
    daq.BooleanSwitch(
        id='TargetSwitch',
        on=False,
        color=ProjectOrange,
        label="Dark",
        labelPosition="left",
    )
])

PercentageTotalSwitch = html.Div([
    html.Div('Percentage of total ',className='h6'),
    daq.BooleanSwitch(
        id='PercentageTotalSwitch',
        on=False,
        color=ProjectOrange,
        label="Dark",
        labelPosition="left",
    )
])

ShowValueSwitch = html.Div([
    html.Div('Show values',className='h6'),
    daq.BooleanSwitch(
        id='ShowValueSwitch',
        on=False,
        color=ProjectOrange,
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

def rangeselector(Grain):
    if Grain == 'D':
        buttons=list([dict(count=7,
                           label="1w",
                           step="day",
                           stepmode="backward"),
                      dict(count=14,
                           label="2w",
                           step="day",
                           stepmode="backward"),
                      dict(count=1,
                           label="1m",
                           step="month",
                           stepmode="backward"),
                      dict(count=3,
                           label="3m",
                           step="month",
                           stepmode="backward"),
                      dict(count=1,
                           label="YTD",
                           step="year",
                           stepmode="todate"),
                      ])
    elif Grain == 'M':     
        buttons=list([dict(count=1,
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
    else:
        buttons=list([dict(count=1,
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
    return buttons

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




def PercentageTotalSwitchDEF(PercentageSwitchie):
    if PercentageSwitchie == 'True':
        list2 = "'percent'"
        return list2
    elif PercentageSwitchie == 'False':
        list2 = "''"
        return list2

def Totaalloop(Totaalloop):
    if Totaalloop == 'True':
        list = '[tracestotal,traces2]' 
        return list
    elif Totaalloop == 'False':
        list = '[traces2]'
        return list 

def Cumloop0(Cumloop):
    if Cumloop == 'False':
        list = ['df_by_Level0Name','CalculationLogic0(Calculation)']
        return list
    elif Cumloop == 'True':
        list = ['df_by_Level0Name','CalculationLogic0Cum(Calculation)']
        return list 

def Cumloop1(Cumloop):
    if Cumloop == 'False':
        list = ['df_by_Level1Name','CalculationLogic1(Calculation)']
        return list
    elif Cumloop == 'True':
        list = ['df_by_Level1Name','CalculationLogic1Cum(Calculation)']
        return list

def Cumloop2(Cumloop):
    if Cumloop == 'False':
        list = ['df_by_Level2Name','CalculationLogic2(Calculation)']
        return list
    elif Cumloop == 'True':
        list = ['df_by_Level2Name','CalculationLogic2Cum(Calculation)']
        return list 


def KPISelectedStyle(kpi):
    Notation = KPINotation[kpi]
    if Notation == '%':
        Notation = ['".1%"']
        return Notation
    elif Notation == '#':
        Notation = ['".2s"']
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


def update_filter_l0(dfl0, GrainSelect, KPISelect,Level0NameSelect):
    dff = dfl0[
        (dfl0["Grain"] == GrainSelect)
        & (dfl0["KPIName"] == KPISelect)
        & (dfl0["LevelName_0"].isin(Level0NameSelect))
        ]
    return dff

def update_filter_l1(dfl1, GrainSelect, KPISelect,Level0NameSelect,Level1NameSelect):
    dff = dfl1[
        (dfl1["Grain"] == GrainSelect)
        & (dfl1["KPIName"] == KPISelect)
        & (dfl1["LevelName_0"].isin(Level0NameSelect))
        & (dfl1["LevelName_1"].isin(Level1NameSelect))
        ]
    return dff

def update_filter_l2(dfl2, GrainSelect, KPISelect,Level0NameSelect,Level1NameSelect, Level2NameSelect,Category1):
    dff = dfl2[
        (dfl2["Grain"] == GrainSelect)
        & (dfl2["KPIName"] == KPISelect)
        & (dfl2["LevelName_0"].isin(Level0NameSelect))
        & (dfl2["LevelName_1"].isin(Level1NameSelect))
        & (dfl2["LevelName_2"].isin(Level2NameSelect))
        & (dfl2["Filter1_0"].isin(Category1))
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
        msg0 = {'display': 'block'}
        msg1 = {'display': 'block'}
        msg2 = {'display': 'none'}
    elif tabsdrilldown == 'tab-2':
        msg0 = {'display': 'block'}
        msg1 = {'display': 'block'}
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

tabs = html.Div([
    dbc.Tabs(children=
    [
    dbc.Tab(children=[#html.I("delete_sweep",n_clicks=0,id='shiftbutton',className="material-icons md-48",style={'position':'absolute','top':'1px','right':'12px','z-index': '1'}),
    dbc.CardBody(
        dbc.Row([
        dbc.Col(dbc.Spinner(children=[#,spinner_class_name='loading'
            dcc.Graph(id='graphlevel0',
                      config=dict(
                        modeBarButtonsToAdd =  ['customButton'],
                        modeBarButtonsToRemove = ['pan', 'lasso2d', 'select', 'zoom2d', 'zoomIn', 'zoomOut','toImage','resetScale',
                                                      'hoverCompareCartesian', 'logo', 'autoScale'],
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
            dbc.Spinner(children=[dcc.Graph(id='graph-level0compare',
                      config=dict(
                          modeBarButtonsToAdd=['customButton'],
                          modeBarButtonsToRemove=['pan','zoom2d','select2d', 'lasso2d', 'zoomIn', 'zoomOut','toImage','resetScale',
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
                      style={'overflow': 'auto'}
                      )])
        ],className="col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12 pretty_graph2"
        ),className="col-12 col-sm-12 col-md-12 col-lg-4 col-xl-4 empty_tab2"
        )
        ],className="row-cols-sm-12 row-cols-md-12 row-cols-lg-12 row-cols-xl-12"
        ),className="row-cols-sm-12 row-cols-md-12 row-cols-lg-11 row-cols-xl-11 pretty_tab"
    )]
,id="Tab0drilldown"),
    dbc.Tab(children=[dbc.CardBody(
        dbc.Row(
        [dbc.Col(dbc.Spinner(children=[
            dcc.Graph(id='graphoveralltime',
                      config=dict(
                          modeBarButtonsToAdd=['customButton'],
                          modeBarButtonsToRemove=['pan', 'lasso2d', 'select', 'zoom2d', 'zoomIn', 'zoomOut','toImage','resetScale',
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
            dbc.Spinner(children=[dcc.Graph(id='graph-level1compare',
                      config=dict(
                          modeBarButtonsToAdd=['customButton'],
                          modeBarButtonsToRemove=['pan','select2d', 'lasso2d', 'select', 'zoom2d', 'zoomIn', 'zoomOut','toImage','resetScale',
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
                          modeBarButtonsToRemove=['pan', 'lasso2d', 'select', 'zoom2d', 'zoomIn', 'zoomOut','toImage','resetScale',
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
        dbc.Col(dbc.Spinner(children=[dcc.Graph(id='graph-level2compare',
                          config=dict(
                              modeBarButtonsToAdd=['customButton'],
                              modeBarButtonsToRemove=['pan','select2d', 'lasso2d', 'select', 'zoom2d', 'zoomIn', 'zoomOut','toImage','resetScale',
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
])




tabscompare = dbc.Tabs(
    [dbc.Tab(label="Compare two",children=[dbc.CardBody(
    dbc.Row([
        dbc.Col(KPIdropdownCompare,
                id='KPICompare'),
        dbc.Col(dbc.Spinner(children=[
            dcc.Graph(id='graph-compare-kpi',
                      config={
                          'modeBarButtonsToRemove': ['pan', 'lasso2d', 'select', 'zoom2d', 'zoomIn', 'zoomOut','toImage','resetScale',
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
                          'modeBarButtonsToRemove': ['pan', 'lasso2d', 'select', 'zoom2d', 'zoomIn', 'zoomOut','toImage','resetScale',
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
,style={'min-height': 'auto'})


######################################################################################################################
################################################----layout aanmaken----###############################################
######################################################################################################################
######################################################################################################################

app.layout = html.Div([
    html.I("chevron_right",className='material-icons toggle-right',id='Opennavbar-right'),#html.I("filter_alt", id='dropdowncontrol', className="material-icons filtericon", n_clicks=0),
    html.Div([
        html.I("filter_alt_off",id='sweepl0filter',className="material-icons md-48"),
       # html.I("filter_alt_off",id='sweepl1',className="material-icons md-48"),
       # html.I("filter_alt_off",id='sweepl2',className="material-icons md-48")
    ],style={'position':'fixed','top':'44%','right':'12px','z-index': '1','display': 'flex','flex-direction': 'column'}),
    html.Div([html.I("settings_suggest",id='open-settings',className="material-icons",n_clicks=0,style={'position':'fixed'}),
              html.I("chevron_right",className='material-icons toggle-bottom',id='Opennavbar-bottom',style={'position':'fixed'})
    ],style={'position':'fixed','top': '96.7%','right': '50%','z-index': '1'}),
    html.Div([
        html.I("filter_list_off",id='sweepl0',className="material-icons md-48"),
        html.I("filter_list_off",id='sweepl1',className="material-icons md-48"),
        html.I("filter_list_off",id='sweepl2',className="material-icons md-48")
    ],style={'position':'fixed','top':'52%','right':'12px','z-index': '1','display': 'flex','flex-direction': 'column'}),
    #dcc.Graph(id='animatedbar'),
    dbc.Row([
        html.Div(id='output-container-date-picker-range',
                 style={'margin-top': '12px'},
                 className='h7'),
        dbc.Modal([
            dbc.ModalBody(children=[
                dbc.Col([mainlogo],className="col-sm-12 col-md-12 col-lg-12 col-xl-12",style={"margin-bottom": '2px'}),
                dbc.Col([Category1],className="col-sm-12 col-md-12 col-lg-12 col-xl-12",style={"margin-bottom": '2px'}),
                dbc.Col([Level0DD],className="col-sm-12 col-md-12 col-lg-12 col-xl-12",style={"margin-bottom": '2px'}),
                dbc.Col([Level1DD],className="col-sm-12 col-md-12 col-lg-12 col-xl-12",style={"margin-bottom": '2px'}),
                dbc.Col([Level2DD],className="col-sm-12 col-md-12 col-lg-12 col-xl-12",style={"margin-bottom": '2px'}),
            ],id="dropdowns"
            ),
            dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close-filter", className="ms-auto", n_clicks=0
                    ),style={'border-top': '0px'}
                ),
        ],
        id="modalfilter",
        className="modalfilter",
        is_open=False,
        ),
    dbc.Col(fade,className="col-sm-12 col-md-12 col-lg-2 col-xl-2",style={'display': 'none'}),
       ]),
    dbc.Row([
            dbc.Col(
            [html.Div(Perioddropdown,className="col-sm-2 col-md-2 col-lg-2 col-xl-2",style={'display': 'none'}),
            html.Div(className="col-sm-9 col-md-9 col-lg-9 col-xl-9",style={"margin": '0 auto'},id='cardsid'),
            html.Div(id='container-ex3', children=[])
            # html.Div(className="col-sm-9 col-md-9 col-lg-9 col-xl-9"
            #    ,style={"margin": '0 auto'},id='cardsid')
            ]),
        ]),

    dbc.Row([
            dbc.Col([
            dbc.Modal(
                [dbc.ModalHeader(dbc.ModalTitle("Graph settings", className='h5'),style={'border-bottom': '0px'}),
                dbc.ModalBody(children=[
                        dbc.Col([Radiograin],className="col-sm-12 col-md-12 col-lg-12 col-xl-12",style={'margin-bottom': '46px'}),
                        dbc.Col([Totaalaggregaatswitch], className="col-sm-12 col-md-12 col-lg-12 col-xl-12"),
                        dbc.Col([CumulativeSwitch], className="col-sm-12 col-md-12 col-lg-12 col-xl-12"),
                        dbc.Col([TargetSwitch], className="col-sm-12 col-md-12 col-lg-12 col-xl-12"),
                        dbc.Col([PercentageTotalSwitch], className="col-sm-12 col-md-12 col-lg-12 col-xl-12"),
                        dbc.Col([ShowValueSwitch], className="col-sm-12 col-md-12 col-lg-12 col-xl-12"),
                    ]),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close-settings", className="ms-auto", n_clicks=0
                    ),style={'border-top': '0px'}
                ),
                ],
                id="modal",
                is_open=False,
            ),
            html.Div(tabs,
                     id="tabscontainer"
                     ,style={'min-height': 'auto'}),
            html.Div(tabscompare,
                     id="tabscompare"
                     ),
                    ],className="col-sm-11 col-md-11 col-lg-10 col-xl-10 pretty_bigtab",style={"margin": '0 auto','margin-top':'20px'}
                    ),
            
          #  html.Div(KPI_Group,className="col-sm-11 col-md-11 col-lg-4 col-xl-3"),

    ],style={'min-height': 'auto'}
    ),
    html.Div(html.Nav(id='navbar')),
    #html.Div(navbarfilters),
    html.Span(html.I(''),style={'margin-top': '5em','display': 'block'}),
    #dcc.Store(id='dff0',data=dfl0json,storage_type='memory'),
    #dcc.Store(id='dff1',data=dfl1json,storage_type='memory'),
    #dcc.Store(id='dff2',data=dfl2json,storage_type='memory'),
    dcc.Store(id='dfl0'),
    dcc.Store(id='dfl1'),
    dcc.Store(id='dfl2'),
    dcc.Store(id='dfl0notime'),
    dcc.Store(id='dfl1notime'),
    dcc.Store(id='dfl2notime'),
    dcc.Store(id='dffcomparefilter'),
    dcc.Store(id='dflcomparekpi'),
    dcc.Store(id='selectedkpigroup'),
    dcc.Store(id='dfgroups'),
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

#app.clientside_callback(
#    """
#    function() {
#        // Create a new KeyboardEvent object
#        var event = new KeyboardEvent('keydown', {
#            key: 'Shift',
#            code: 'ShiftLeft',
#            which: 16,
#            shiftKey: true,
#            bubbles: true
#        });
#
#        // Dispatch the KeyboardEvent on the window
#        window.dispatchEvent(event);
#    }
#    """,
#    Output('output', 'children'),
#    [Input('shiftbutton', 'n_clicks')]
#)


KPIGroup =[]

@app.callback([
             Output("KPIGroupSelect", 'value'),
             ],
            Input({'type': 'kpigroup-ex3', 'index': ALL}, 'n_clicks'), prevent_initial_call=True
           # eval(kpigrouplistinput3[0])
            )
def KPIgrouplighter(n_clicks):#*args
    print('execute KPIgrouplighter')
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    valuelist =[]
    try:
        valuelisttmp = list(json.loads(changed_id).values()) 
        valuelist.clear()
        valuelist.append(valuelisttmp[0])
    except json.decoder.JSONDecodeError as e:
        print("Unable to decode JSON: ", e)
    KPIGroupList = d_kpi['KPIGroup'].unique().tolist()
    #try:
    #    if len(dash.callback_context.triggered)!= 1:
    #        print('nothingtoseehere')
    #    elif "filter-dropdown-ex3-reset" in valuelist: 
    #        kpigroup.append(valuelist[0])
    #        print('bloei')
    #    elif "filter-dropdown-ex3" in valuelist: 
    #        kpigroup.append(valuelist[0])
    #    elif 'kpigroup' in changed_id[0:8]:
    #        kpigroup.append(KPINameListi[0])
    #except:
    #    print('bs!')
    if changed_id =='{"index":"kpigroup0","type":"kpigroup-ex3"}':
        KPIGrouptmp1 = []
        for i in range(len(KPIGroupList)):
            KPIGrouptmp1.append(KPIGroupList[i])
        KPIGroup.append(KPIGrouptmp1)
        kpicountout.clear() 
        kpicountout.append(len(KPINameList))
    elif valuelist:
        KPIGroup.append([valuelist[0]])
    if not KPIGroup:
        KPIGrouptmp3 = []
        for i in range(len(KPIGroupList)):
            KPIGrouptmp3.append(KPIGroupList[i])
        KPIGroup.append(KPIGrouptmp3)
        kpicountout.clear() 
        kpicountout.append(len(KPINameList))
    KPIGroup2 = KPIGroup[-1]
    print('KPIGroup2')
    print(KPIGroup2)
    return KPIGroup2


kpi =[]

#print(eval(carddivnclicks3new[0]+','+kpigrouplistinput3[0]) if carddivnclicks3new else eval(carddivnclicks3[0]+','+kpigrouplistinput3[0]))
@app.callback([
    Output('KPISelect', 'value'),
  #  Output({'type': 'output-ex3', 'index': MATCH}, 'children'),
    ],
    [
    Input({'type': 'filter-dropdown-ex3', 'index': ALL}, 'n_clicks'),
    Input({'type': 'filter-dropdown-ex3-reset', 'index': ALL}, 'n_clicks'),
    Input('KPIGroupSelect', 'value'),
    Input({'type': 'kpigroup-ex3', 'index': ALL}, 'n_clicks'),
    #eval(kpigrouplistinput3[0])
    ], prevent_initial_call=True
 )

def update_df_KPIGroup(n_clicks,n_clicks2,KPIGroupSelect,n_clicks3):#,*args
    print('execute update_df_KPIGroup')   
    dffKPISelect = d_kpi[
        (d_kpi["KPIGroup"].isin(KPIGroupSelect))
    ]
    dffKPISelect.sort_values(by=['Sorting'])
    KPINameListi = dffKPISelect['KPIName'].unique()
    try:
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
        valuelist = list(json.loads(changed_id).values()) 
    except json.decoder.JSONDecodeError as e:
        print("Unable to decode JSON: ", e)
    try:
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
        if len(dash.callback_context.triggered)!= 1:
            print('nothingtoseehere')
        elif "filter-dropdown-ex3-reset" in valuelist: 
            kpi.append(valuelist[0])
        elif "filter-dropdown-ex3" in valuelist: 
            kpi.append(valuelist[0])
        elif 'kpigroup' in changed_id[0:8]:
            kpi.append(KPINameListi[0])
    except:
        print('bs!')
    return KPINameListi[0] if not kpi else kpi[-1]


######################################################################################################################
######################################################################################################################
################################################----tab 0 aanmaken----###############################################
######################################################################################################################
######################################################################################################################


@app.callback(
    Output('graph-level0compare', 'selectedData'),
    [Input('sweepl0', 'n_clicks'),
     #Input({'type': 'filter-dropdown-ex3-reset', 'index': ALL}, 'n_clicks'),
    ], session_check=False, prevent_initial_call=True
)

def reset_clickDatal0(n_clicks):#,n_clicks2
    print('removefilterl0')
    return None


@app.callback([
              Output("Level0NameSelect", "value"),
             ],             
              Input('graph-level0compare', 'selectedData'),
              Input('sweepl0', 'n_clicks'),
              Input("Level0NameSelect", "value"),
              Input({'type': 'filter-dropdown-ex3-reset', 'index': ALL}, 'n_clicks'), prevent_initial_call=True
             )
def Level0Update(selecteddatal0bar,n_clicks,Level0NameSelect,reset):#,selecteddatal0,n_clicks,KPINameSelect,clickdatal0bar,clickdatal0
    print('Level0Update')
    selectedlistl0bar_list =[]
    selectedlistl0bar_list.clear()
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    changed_id2 = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    try:
        if 'sweepl0' in changed_id:
            selectedlistl0bar_list.clear()
            for d in Level0NameList:
                selectedlistl0bar_list.append(d)
        elif selecteddatal0bar['points']:
            selectedlistl0bar_list.clear()
            for p in selecteddatal0bar['points']:
                selectedlistl0bar_list.append(p['y'])
        elif "filter-dropdown-ex3-reset" in list(json.loads(changed_id2).values()):
            selectedlistl0bar_list.clear()
            for j in Level0NameList:
                selectedlistl0bar_list.append(j)
    except:
        print()
    if len(selectedlistl0bar_list)>0:
        return selectedlistl0bar_list
    else:
        raise dash.exceptions.PreventUpdate

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

@app.callback([
    Output("Category1Select", "options"),
    Output("Level0NameSelect", "options"),
    Output("Level1NameSelect", "options"),
    Output("Level2NameSelect", "options")
],
   # Output('animatedbar', 'figure'),
     Input("Category1Select", "value"),
     Input("Level0NameSelect", "value"),
     Input("Level1NameSelect", "value"),
     Input("Level2NameSelect", "value"),
     Input("KPISelect", "value"),
     Input('tabsdrilldown','active_tab'), prevent_initial_call=True
)

def DropdownOptions(Category1Select,Level0NameSelect,Level1NameSelect,Level2NameSelect,KPISelect,tabsdrilldown):  #,*args ,Level2NameSelect,toggle, relayoutData
   print('execute DropdownOptions')
   Category1filtered = dfl0polars.filter((pl.col("KPIName") == KPISelect)
                            )
   dff0onlykpifiltered = dfl0polars.filter((pl.col("KPIName") == KPISelect)
                            & (pl.col("Filter1_0").is_in(Category1Select)))
   dff1onlykpifiltered = dfl1polars.filter((pl.col("KPIName") == KPISelect)
                            & (pl.col("LevelName_0").is_in(Level0NameSelect))
                            & (pl.col("Filter1_0").is_in(Category1Select)))
   dff2onlykpifiltered = dfl2polars.filter((pl.col("KPIName") == KPISelect)
                            & (pl.col("LevelName_0").is_in(Level0NameSelect))
                            & (pl.col("LevelName_1").is_in(Level1NameSelect))
                            & (pl.col("Filter1_0").is_in(Category1Select)))
   Category1Select =  [{'label': html.Span([i],style={'background-color': ProjectOrange}), 'value': i}  for i in Category1filtered["Filter1_0"].unique()]
   Level0NameSelect = [{'label': html.Span([i],style={'background-color': Level0NameColor[i]}), 'value': i} for i in dff0onlykpifiltered["LevelName_0"].unique()]
   Level1NameSelect = [{'label': html.Span([i],style={'background-color': Level1NameColor[i]}), 'value': i} for i in dff1onlykpifiltered["LevelName_1"].unique()]
   Level2NameSelect = [{'label': html.Span([i],style={'background-color': Level2NameColor[i]}), 'value': i} for i in dff2onlykpifiltered["LevelName_2"].unique()]
   #print(Category1Select)
   #print(Level0NameSelect)
   #print(Level1NameSelect)
   #print(Level2NameSelect)
   return Category1Select,Level0NameSelect,Level1NameSelect,Level2NameSelect

#@app.callback([
#    Output("Category1Select", "value"),
#    ],
#    Input('sweepl0filter', 'n_clicks'),
#    State("KPISelect", "value"),
#)
#
#def dropdown1_reset(n_clicks,KPISelect):  #,*args ,Level2NameSelect,toggle, relayoutData
#   print('execute dropdown1_reset')
#   print(KPISelect)
#   Category1filtered = dfl0[(dfl0["KPIName"] == KPISelect)]
#   output=[]
#   Category1Select =  [i for i in Category1filtered["Filter1_0"].unique()]
#   for i in Category1Select:
#       output.append(i)
#   print(Category1Select)
#   return [Category1Select]


datefromtmp = []
datetotmp = []
#datefromtmp.append(str(dfl0['Period_int'].min())[0:10])
#datetotmp.append(str(dfl0['Period_int'].max())[0:10])
datefromtmp.append('2021-01-01')
datetotmp.append('2023-09-01')

@app.callback([
              ServersideOutput('dfgroups', 'data'),
              ServersideOutput('dfl0', 'data'),
              ServersideOutput('dfl1', 'data'),
              ServersideOutput('dfl2', 'data'),
              ServersideOutput('dfl0notime', 'data'),
              ServersideOutput('dfl1notime', 'data'),
              ServersideOutput('dfl2notime', 'data'),
            #  Output('dffcomparefilter', 'data'),
              ServersideOutput('dflcomparekpi', 'data'),#,backend=my_backend
              Output('output-container-date-picker-range', 'children'),
              Output('dropdown0', 'value'),
              Output('dropdown1', 'value'),
              Output('dropdown2', 'value'),
              Output('sweepl0', 'style'),
              Output('sweepl1', 'style'),
              Output('sweepl2', 'style'),
            #  Output('ProjectDropdown1', 'style'),
             ],            
              Input('GrainSelect', 'value'),
              Input('KPISelect', 'value'),
              Input('KPIGroupSelect', 'value'),
              Input('graphlevel0', 'relayoutData'),
              Input('graphoveralltime', 'relayoutData'),
              Input('graph-with-slider', 'relayoutData'),
              #Input('graphlevel0', 'clickData'),
              #Input('graphoveralltime', 'clickData'),
              #Input('graph-with-slider', 'clickData'),
              Input('tabsdrilldown','active_tab'),
              Input("Level0NameSelect", "value"),
              Input("Level1NameSelect", "value"),
              Input("Level2NameSelect", "value"),
              Input("Category1Select", "value")
              ,memoize=True)
def clean_data(GrainSelect,KPISelect,KPIGroupSelect,relayoutDatal0,relayoutDatal1,relayoutDatal2,tabsdrilldown,Level0NameSelect,Level1NameSelect,Level2NameSelect,Category1):#,*args,sweepl1 relayoutl1barclickdatal2bar,clickdatal0,clickdatal1,clickdatal2
    print('execute clean_data')
    dfll2 = []
    dfll0pol = []
    dfll1pol = []
    dfll2pol =[]
    dfll0notime = []
    dfll1notime = []
    dfll2notime = []
    dfllCompare = []
    dffcompare = []
    dfftstst0 = dfl0polars.filter((pl.col("Grain") == GrainSelect) 
                            & (pl.col("KPIName") == KPISelect)
                            & (pl.col("LevelName_0").is_in(Level0NameSelect))
                            & (pl.col("Filter1_0").is_in(Category1)))
    dfftstst1 = dfl1polars.filter((pl.col("Grain") == GrainSelect) 
                            & (pl.col("KPIName") == KPISelect)
                            & (pl.col("LevelName_0").is_in(Level0NameSelect))
                            & (pl.col("LevelName_1").is_in(Level1NameSelect))
                            & (pl.col("Filter1_0").is_in(Category1)))
    dfftstst2 = dfl2polars.filter((pl.col("Grain") == GrainSelect) 
                            & (pl.col("KPIName") == KPISelect)
                            & (pl.col("LevelName_0").is_in(Level0NameSelect))
                            & (pl.col("LevelName_1").is_in(Level1NameSelect))
                            & (pl.col("LevelName_2").is_in(Level2NameSelect))
                            & (pl.col("Filter1_0").is_in(Category1)))
    
    #dff2 = pd.DataFrame(update_filter_l2(dfl2, GrainSelect, KPISelect,Level0NameSelect, Level1NameSelect, Level2NameSelect,Category1))
    dfl0polarsfilter = dfl0polars.filter((pl.col("Grain") == GrainSelect) 
                                         & (pl.col("LevelName_0").is_in(Level0NameSelect))
                                         & (pl.col("KPIGroup").is_in(KPIGroupSelect))
                                         & (pl.col("Filter1_0").is_in(Category1)))
    dfl1polarsfilter = dfl1polars.filter((pl.col("Grain") == GrainSelect) 
                                         & (pl.col("LevelName_0").is_in(Level0NameSelect))
                                         & (pl.col("LevelName_1").is_in(Level1NameSelect))
                                         & (pl.col("KPIGroup").is_in(KPIGroupSelect))
                                         & (pl.col("Filter1_0").is_in(Category1)))
    dfl2polarsfilter = dfl2polars.filter((pl.col("Grain") == GrainSelect) 
                                         & (pl.col("LevelName_0").is_in(Level0NameSelect))
                                         & (pl.col("LevelName_1").is_in(Level1NameSelect))
                                         & (pl.col("LevelName_2").is_in(Level2NameSelect))
                                         & (pl.col("KPIGroup").is_in(KPIGroupSelect))
                                         & (pl.col("Filter1_0").is_in(Category1)))
    
    dfl0polarsgroup = dfl2polars.filter((pl.col("Grain") == GrainSelect) 
                                         & (pl.col("LevelName_0").is_in(Level0NameSelect))
                                         & (pl.col("Filter1_0").is_in(Category1)))
    dfl1polarsgroup = dfl2polars.filter((pl.col("Grain") == GrainSelect) 
                                         & (pl.col("LevelName_0").is_in(Level0NameSelect))
                                         & (pl.col("LevelName_1").is_in(Level1NameSelect))
                                         & (pl.col("Filter1_0").is_in(Category1)))
    dfl2polarsgroup = dfl2polars.filter((pl.col("Grain") == GrainSelect) 
                                         & (pl.col("LevelName_0").is_in(Level0NameSelect))
                                         & (pl.col("LevelName_1").is_in(Level1NameSelect))
                                         & (pl.col("LevelName_2").is_in(Level2NameSelect))
                                         & (pl.col("Filter1_0").is_in(Category1)))
    dfl0polarsgroup = dfl0polarsgroup.select("KPIGroup").unique()
    dfl1polarsgroup = dfl1polarsgroup.select("KPIGroup").unique()
    dfl2polarsgroup = dfl2polarsgroup.select("KPIGroup").unique()
    dffpolars = []
    dfllComparepolar =[]
    if tabsdrilldown == 'tab-0':
        relayoutdata1 = relayoutDatal0
        dflpolarsgroup = dfl0polarsgroup
     #   clickdata1 = clickdatal0
        changeid = 'graphlevel0.relayoutData'
        dffpolars.append(dfl0polarsfilter)
        levelindicator = 'level0'
    elif tabsdrilldown == 'tab-1':
        relayoutdata1 = relayoutDatal1
        dflpolarsgroup = dfl1polarsgroup
     #   clickdata1 = clickdatal1
        changeid = 'graphoveralltime.relayoutData'
        dffpolars.append(dfl1polarsfilter)
        levelindicator = 'level1'
    elif tabsdrilldown == 'tab-2':
        relayoutdata1 = relayoutDatal2
        dflpolarsgroup = dfl2polarsgroup
    #    clickdata1 = clickdatal2
        changeid = 'graph-with-slider.relayoutData'
        dflpolarsgroup = dfl2polarsgroup
        dffpolars.append(dfl2polarsfilter)
        levelindicator = 'level2'
    else:
        relayoutdata1 = relayoutDatal0
        changeid = 'graphlevel0.relayoutData'
        dflpolarsgroup = dfl0polarsgroup
      #  clickdata1 = clickdatal0
        dffpolars.append(dfl0polarsfilter)
        levelindicator = 'level0'
    cookpi_attributes = cookpi_attributestmp[(cookpi_attributestmp.d_kpi_id == KPINameToID[KPISelect])]
    result = {}
    level0 =[]
    level1 =[]
    level2 =[]
    for index,row in cookpi_attributes.iterrows():
        if row['Level_ID_present'] == 'd_level0_id':
            result[row['Level_ID_present']] = row['dds_name']
            level0.append(result['d_level0_id'])
        elif row['Level_ID_present'] == 'd_level1_id':
            result[row['Level_ID_present']] = row['dds_name']
            level1.append(result['d_level1_id'])
        elif row['Level_ID_present'] == 'd_level2_id':
            result[row['Level_ID_present']] = row['dds_name']
            level2.append(result['d_level2_id']) #used to fill the name of the dropdownlist
    
        
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if relayoutdata1 == {'autosize': True} or relayoutdata1 is None:
        pass
    elif changed_id == changeid:
        if 'xaxis.range[0]' in relayoutdata1:
            datefromtmp.append(relayoutdata1['xaxis.range[0]'][0:10])
            datetotmp.append(relayoutdata1['xaxis.range[1]'][0:10])
        elif 'xaxis.range' in relayoutdata1:
            datefromtmp.append(relayoutdata1['xaxis.range'][0])
            datetotmp.append(relayoutdata1['xaxis.range'][1])
    elif changed_id in ['tabselect.active_tab', 'tabsdrilldown.active_tab', 'GrainSelect.value', 'Level1NameSelect.value', 'Level2NameSelect.value', 'KPISelect.value']:
        pass
        
    if not datefromtmp:
        #dfll2.append(dff2)
        dfll0pol.append(dfftstst0)
        dfll1pol.append(dfftstst1)
        dfll2pol.append(dfftstst2)
     #   dfllCompare.append(dffcompare[0])
        dfllComparepolar.append(dffpolars[0])
    elif changed_id == 'GrainSelect.value':
       # dfll2.append(dff2)
        dfll0pol.append(dfftstst0)
        dfll1pol.append(dfftstst1)
        dfll2pol.append(dfftstst2)
     #   dfllCompare.append(dffcompare[0])
        dfllComparepolar.append(dffpolars[0])
    else:
       # dfff = dff2[dff2['Period_int'].between(datefromtmp[-1], datetotmp[-1])].reset_index(drop=True)
       # dfll2.append(dfff)
        dfll0pol.append(dfftstst0.filter((pl.col('Period_int')>= datefromtmp[-1]) 
                                                    &(pl.col('Period_int')<= datetotmp[-1])))
        dfll1pol.append(dfftstst1.filter((pl.col('Period_int')>= datefromtmp[-1]) 
                                                    &(pl.col('Period_int')<= datetotmp[-1])))
        dfll2pol.append(dfftstst2.filter((pl.col('Period_int')>= datefromtmp[-1]) 
                                                    &(pl.col('Period_int')<= datetotmp[-1])))
       # dfllCompare.append(dffcompare[0][dffcompare[0]['Period_int'].between(datefromtmp[-1], datetotmp[-1])].reset_index(drop=True))
        dfllComparepolar.append(dffpolars[0].filter((pl.col('Period_int')>= datefromtmp[-1]) 
                                                    &(pl.col('Period_int')<= datetotmp[-1])))
    
    #testtmp0 = dfll2[0].filter(regex='^(?!.*(_1|_2)$)')
    #testtmp1 = dfll2[0].filter(regex='^(?!.*(_0|_2)$)')
    #testtmp2 = dfll2[0].filter(regex='^(?!.*(_0|_1)$)')

    testtmp0pol = (
    dfll0pol[0]
    .lazy()
    #.select(pl.exclude("^.*(_1|_2)$")) #'^prefix_.*$'
    .sort(["Period_int", "LevelName_0"])
    .collect()
    
    )
    testtmp1pol = (
    dfll1pol[0]
    .lazy()
    .select(pl.exclude("^.*(_0)$")) #'^prefix_.*$'|_2
    .sort(["Period_int", "LevelName_1"])
    .collect()
    )
    testtmp2pol = (
    dfll2pol[0]
    .lazy()
    .select(pl.exclude("^.*(_0|_1)$")) #'^prefix_.*$'
    .sort(["Period_int", "LevelName_2"])
    .collect()
    )
    #testtmp0pol = dfll2pol[0].filter(regex='^(?!.*(_1|_2)$)')
    #testtmp1pol = dfll2pol[0].filter(regex='^(?!.*(_0|_2)$)')
    #testtmp2pol = dfll2pol[0].filter(regex='^(?!.*(_0|_1)$)')
    

    #testtmp0 = testtmp0.drop('d_level1_id',axis=1)
    #testtmp0 = testtmp0.drop('d_level2_id',axis=1)
    #testtmp0pol.select(pl.exclude(["d_level1_id","d_level2_id"]))
    
    #testtmp1 = testtmp1.drop('d_level0_id',axis=1)
    #testtmp1 = testtmp1.drop('d_level2_id',axis=1)
    testtmp1pol.select(pl.exclude(["d_level0_id"]))#,"d_level2_id"

    #testtmp2 = testtmp2.drop('d_level0_id',axis=1)
    #testtmp2 = testtmp2.drop('d_level1_id',axis=1)
    testtmp2pol.select(pl.exclude(["d_level0_id","d_level1_id"]))

    #testtmp0.fillna(value=0, inplace=True)
    #testtmp1.fillna(value=0, inplace=True)
    #testtmp2.fillna(value=0, inplace=True)
    testtmp0pol.fill_null(0)
    testtmp1pol.fill_null(0)
    testtmp2pol.fill_null(0)

    columnsdff0pol = testtmp0pol.columns
    #columnsdff0 = testtmp0.columns.tolist()
    #columnsdff0.remove('Numerator')
    #columnsdff0.remove('Denominator')
    #columnsdff0.remove('Numerator_LP')
    #columnsdff0.remove('Denominator_LP')
    #columnsdff0pol.remove('d_level1_id')
    #columnsdff0pol.remove('d_level2_id')
    columnsdff0pol.remove('Numerator')
    columnsdff0pol.remove('Denominator')
    #columnsdff0pol.remove('Numerator_LP')
    #columnsdff0pol.remove('Denominator_LP')

    #columnsdff1 = testtmp1.columns.tolist()
    columnsdff1pol = testtmp1pol.columns
    #columnsdff1.remove('Numerator')
    #columnsdff1.remove('Denominator')
    #columnsdff1.remove('Numerator_LP')
    #columnsdff1.remove('Denominator_LP')
    columnsdff1pol.remove('d_level0_id')
    #columnsdff1pol.remove('d_level2_id')
    columnsdff1pol.remove('Numerator')
    columnsdff1pol.remove('Denominator')
    #columnsdff1pol.remove('Numerator_LP')
    #columnsdff1pol.remove('Denominator_LP')


    #columnsdff2 = testtmp2.columns.tolist()
    columnsdff2pol = testtmp2pol.columns
    #columnsdff2.remove('Numerator')
    #columnsdff2.remove('Denominator')
    #columnsdff2.remove('Numerator_LP')
    #columnsdff2.remove('Denominator_LP')
    columnsdff2pol.remove('d_level0_id')
    columnsdff2pol.remove('d_level1_id')
    columnsdff2pol.remove('Numerator')
    columnsdff2pol.remove('Denominator')
    #columnsdff2pol.remove('Numerator_LP')
    #columnsdff2pol.remove('Denominator_LP')
    
    noemer = f'pl.col("Denominator").{eval(AggregateNumDenom(KPIDenomAgg[KPISelect]))}()'
    teller = f'pl.col("Numerator").{eval(AggregateNumDenom(KPINumAgg[KPISelect]))}()'
    dff0pol = (
    testtmp0pol.lazy()
    .groupby(columnsdff0pol)
    .agg(
        [
            eval(noemer),
            eval(teller),
        ]
    )
     .sort(["Period_int", "LevelName_0"])
   # .limit(5)
    )

    dff1pol = (
    testtmp1pol.lazy()
    .groupby(columnsdff1pol)
    .agg(
        [
            eval(noemer),
            eval(teller),
        ]
    )
     .sort(["Period_int", "LevelName_1"])
    #.limit(5)
    )
    dff2pol = (
    testtmp2pol.lazy()
    .groupby(columnsdff2pol)
    .agg(
        [
            eval(noemer),
            eval(teller),
        ]
    )
    .sort(["Period_int", "LevelName_2"])
    #.limit(5)
    )
    #dff0 = testtmp0.head(5).groupby(columnsdff0, as_index=False, sort=False).agg(
    #       {'Denominator': eval(AggregateNumDenom(KPIDenomAgg[KPISelect])),'Numerator': eval(AggregateNumDenom(KPINumAgg[KPISelect]))})
    #
    #dff1 = testtmp1.groupby(columnsdff1, as_index=False, sort=False).agg(
    #       {'Denominator': eval(AggregateNumDenom(KPIDenomAgg[KPISelect])),'Numerator': eval(AggregateNumDenom(KPINumAgg[KPISelect]))})
    #
    #dff2 = testtmp2.groupby(columnsdff2, as_index=False, sort=False).agg(
    #       {'Denominator': eval(AggregateNumDenom(KPIDenomAgg[KPISelect])),'Numerator': eval(AggregateNumDenom(KPINumAgg[KPISelect]))})
    #testtmp00 = testtmp0.drop('Period_int',axis=1)
    #testtmp00 = testtmp0.drop('PeriodName',axis=1)
    testtmp0pol.select(pl.exclude(["Period_int","PeriodName"]))


    #testtmp11 = testtmp1.drop('Period_int',axis=1)
    #testtmp11 = testtmp1.drop('PeriodName',axis=1)
    testtmp1pol.select(pl.exclude(["Period_int","PeriodName"]))

    #testtmp22 = testtmp2.drop('Period_int',axis=1)
    #testtmp22 = testtmp2.drop('PeriodName',axis=1)
    testtmp2pol.select(pl.exclude(["Period_int","PeriodName"]))

    #testtmp00.fillna(value=0, inplace=True)
    #testtmp11.fillna(value=0, inplace=True)
    #testtmp22.fillna(value=0, inplace=True)

    #columnsdff0.remove('Period_int')
    #columnsdff0.remove('PeriodName')
    #columnsdff1.remove('Period_int')
    #columnsdff1.remove('PeriodName')
    #columnsdff2.remove('Period_int')
    #columnsdff2.remove('PeriodName')
    columnsdff0pol.remove('Period_int')
    columnsdff1pol.remove('Period_int')
    columnsdff2pol.remove('Period_int')
    columnsdff0pol.remove('PeriodName')
    columnsdff1pol.remove('PeriodName')
    columnsdff2pol.remove('PeriodName')

    dfll0notime = (
    testtmp0pol.lazy()
    .groupby(columnsdff0pol)
    .agg(
        [
            eval(noemer),
            eval(teller),
        ]
    )
    .sort(["LevelName_0"])
   # .limit(5)
    )

    dfll1notime = (
    testtmp1pol.lazy()
    .groupby(columnsdff1pol)
    .agg(
        [
            eval(noemer),
            eval(teller),
        ]
    )
    .sort(["LevelName_1"])
   # .sort("Period_int")
    #.limit(5)
    )
    dfll2notime = (
    testtmp2pol.lazy()
    .groupby(columnsdff2pol)
    .agg(
        [
            eval(noemer),
            eval(teller),
        ]
    )
    .sort(["LevelName_2"])
    )   
    
    #dfll0notime.append(testtmp00.groupby(columnsdff0,as_index=False, sort=False).agg(
    #        {'Denominator': eval(AggregateNumDenom(KPIDenomAgg[KPISelect])),'Numerator': eval(AggregateNumDenom(KPINumAgg[KPISelect]))})
    #)
#
    #dfll1notime.append(testtmp11.groupby(columnsdff1,as_index=False, sort=False).agg(
    #       {'Denominator': eval(AggregateNumDenom(KPIDenomAgg[KPISelect])),'Numerator': eval(AggregateNumDenom(KPINumAgg[KPISelect]))})
    #)
#
    #dfll2notime.append(testtmp22.groupby(columnsdff2,as_index=False, sort=False).agg(
    #       {'Denominator': eval(AggregateNumDenom(KPIDenomAgg[KPISelect])),'Numerator': eval(AggregateNumDenom(KPINumAgg[KPISelect]))})
    #)

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    #dffcomparejson = dfllCompare[0].to_json(date_format='iso', orient='split')
    dffcomparejson = dfllComparepolar[0]
    ##dffcomparejsontmp = dfllComparepolar[0].write_json()
    ##dffcomparejson = {i['name']: i['values'] for i in json.loads(dffcomparejsontmp)['columns']} 
    #timefiltered
   # print(dff01.to_json(date_format='iso', orient='split'))
    dffl0json = dff0pol.collect()
    ##dffl0jsontmp = dff0pol.collect().write_json()
    ##dffl0json = {i['name']: i['values'] for i in json.loads(dffl0jsontmp)['columns']} 

    #timefiltered & kpi filtered
    dffl1json = dff1pol.collect()
    ##dffl1jsontmp = dff1pol.collect().write_json()
    ##dffl1json = {i['name']: i['values'] for i in json.loads(dffl1jsontmp)['columns']} 
    #timefiltered & kpi filtered
    dffl2json = dff2pol.collect()
    ##dffl2jsontmp = dff2pol.collect().write_json()
    ##dffl2json = {i['name']: i['values'] for i in json.loads(dffl2jsontmp)['columns']} 
    #timefiltered & kpi filtered
    dffl0jsonnotime = dfll0notime.collect()
    ##dffl0jsonnotimetmp = dfll0notime.collect().write_json()
    ##dffl0jsonnotime = {i['name']: i['values'] for i in json.loads(dffl0jsonnotimetmp)['columns']} 
    #timefiltered & kpi filtered without time
    dffl1jsonnotime = dfll1notime.collect()
    ##dffl1jsonnotimetmp = dfll1notime.collect().write_json()
    ##dffl1jsonnotime = {i['name']: i['values'] for i in json.loads(dffl1jsonnotimetmp)['columns']} 
   #timefiltered & kpi filtered without time
    dffl2jsonnotime = dfll2notime.collect()
    ##dffl2jsonnotimetmp = dfll2notime.collect().write_json()
    ##dffl2jsonnotime = {i['name']: i['values'] for i in json.loads(dffl2jsonnotimetmp)['columns']} 

    dffgroups = dflpolarsgroup
    #dffgroups = {i['name']: i['values'] for i in json.loads(dffgroupstmp)['columns']} 
    #clickdatasend = dfll2[0]['PeriodName'].unique()
    #Periodchosencount = []
    #Periodchosencount.clear()
    #Periodchosencount.append(len(clickdatasend.tolist()))
    #Displaypreviouscount = []
    #if Periodchosencount[0]>1:
    #    Displaypreviouscount.append("block")
    #else:
    #    Displaypreviouscount.append("none") 
   # style={eval(Displaypreviouscount[0])}
   # style = {'display': Displaypreviouscount}
    string_prefix = 'You have selected: '
    #print(dff0pol.select(pl.col('Period_int')).max().collect())
    if datefromtmp is not None:
        start_date_string = str(dff0pol.select(pl.col('Period_int')).min().collect())[0:10]
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if datetotmp is not None:
        end_date_string = str(dff0pol.select(pl.col('Period_int')).max().collect())[0:10]
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        string_prefix = 'Select a date to see it displayed here'
    if Level0NameSelect == list(Level0NameList):
        sweep0style = {'opacity':'0.2'}
    else:
        sweep0style = {}
    if Level1NameSelect == list(Level1NameList):
        sweep1style = {'opacity':'0.2'}
    else:
        sweep1style = {}
    if Level2NameSelect == list(Level2NameList):
        sweep2style = {'opacity':'0.2'}
    else:
        sweep2style = {}
    return dffgroups,dffl0json,dffl1json,dffl2json,dffl0jsonnotime,dffl1jsonnotime,dffl2jsonnotime,dffcomparejson,string_prefix,'bs' if not level0 else level0[0],'bs' if not level1 else level1[0],'bs' if not level2 else level2[0],sweep0style,sweep1style,sweep2style#,style,style,style,style,style#,clickdatasend,dffcomparejson

datefromtmp.clear()
datetotmp.clear()  

@app.callback([
    Output('cardsid', 'children'),
    Output('navbar', 'children'),
    ]
    ,
    Input('dfgroups', 'data'),
    Input('dflcomparekpi', 'data'),
    Input("KPISelect", "value"),
    Input("KPIGroupSelect", "value"),
    Input("breakpoints", "widthBreakpoint"), session_check=False, prevent_initial_call=True
)

def updatekpiindicator(dfgroups,dffcompare,KPISelect,KPIGroupSelect,widthBreakpoint):#
    print('execute updatekpiindicator')
    sidemenulist=[]
    sidemenulist3=[]
    sidemenulist.clear()
    sidemenulist3.clear()
    accordionlist=[]
    accordionlist3=[]
    accordionlist.clear()
    accordionlist3.clear()
    carousellistnew = []
    carousellist3new =[]
    carousellist3new.clear()
    carousellistnew.clear()
   # dfl0 = pd.read_json(dfl0, orient='split')
    #dffcompare = pd.read_json(dffcompare, orient='split')
    dftouse = dffcompare.to_pandas()#pd.DataFrame(dffcompare)
    dfgroups = dfgroups #pd.DataFrame(dfgroups)
   # dfl2 = pd.read_json(dfl2click, orient='split')
    #dataCompare = pd.read_json(compareset, orient='split')
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if kpicountout[0]<slides_to_show_ifenough:
        slides_to_show = kpicountout[0]
    else:
        slides_to_show = slides_to_show_ifenough
    
    dftouse.sort_values(by=['Sorting'])
    print('test2')
    #create list with all kpi group names that exist for the selected level 1, 2 or 3
    KPIGroupListmodelfilter = dfgroups['KPIGroup'].unique()
    #create list with all kpi group names that exist in the selected group without select
    KPIGroupListFiltered = d_kpi["KPIGroup"].unique()
    #create list with all kpi names that exist for the selected level 1, 2 or 3
    KPINameListmodelfilter = dftouse['KPIName'].unique()
    #create list with all kpi names that exist in the selected group without select
    KPIListFiltered = d_kpi[
            (d_kpi["KPIGroup"].isin(KPIGroupSelect))
        ]
    KPIListFiltered.sort_values(by=['Sorting'])
    KPINameListGroupFilter = KPIListFiltered['KPIName'].unique()
    
    KPINameListIterate = []
    #enter all values that exist for the selected level 1 2 and 3
    for i in KPINameListmodelfilter:
        KPINameListIterate.append(i)
    #enter all values that exist in the whole project but not for the selected level 1 2 and 3
    for p in KPINameListGroupFilter:
        if p not in KPINameListmodelfilter:
            KPINameListIterate.append(p)       
    KPIGroupListIterate = []
    #enter all values that exist for the selected level 1 2 and 3
    for j in KPIGroupListmodelfilter:
        KPIGroupListIterate.append(j)
    #enter all values that exist in the whole project but not for the selected level 1 2 and 3
    for l in KPIGroupListFiltered:
        if l not in KPIGroupListmodelfilter:
            KPIGroupListIterate.append(l)
    #KPINameListIterate.remove(KPISelect)
    #KPINameListIterate.insert(0,KPISelect)
    outputactual =[]
    outputactualtxt =[]
   # outputlasttxt =[]
   # outputlast = []
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
    code_executed = False
    stylegroup = {'color':buttonlogocolor,'background-color':buttoncolor}
    sidemenulist.append(
      f"""html.Li(html.A([
                 html.I('category',className='material-icons icon'),
                 html.Span('All categories',className='text nav-text')],style={stylegroup if len(KPIGroupSelect)>1 else {}},href='#',id=dict(type='kpigroup-ex3',index ='kpigroup0'))
                ,className='nav-link')"""
    )
    for i,kpigroup in enumerate(KPIGroupListIterate):
        numbertmp= i
        numberidtmp= i+1
        number=str(numbertmp)
        numberid=str(numberidtmp)
        GroupImage2 = GroupImage[numbertmp]
        print(KPIGroupSelect)
        print(kpigroup)
        if KPIGroupSelect[0] == kpigroup:
            stylegroup1 = {'color':buttonlogocolor,'background-color':buttoncolor}
        else:
            stylegroup1 = {}
        KPIGroupList2 = KPIGroupList[numbertmp]
        if kpigroup in KPIGroupListmodelfilter:
            if kpigroup in KPIGroupListmodelfilter: 
                sidemenulist.append(
                    f"""html.Li(html.A([
                            html.I('{GroupImage2}',className='material-icons icon'),
                            html.Span('{KPIGroupList2}',className='text nav-text')],href='#',id=dict(type='kpigroup-ex3',index ='{kpigroup}'),style={stylegroup1 if len(KPIGroupSelect)==1 else {}})
                            ,className='nav-link')"""
                ) 
        else:
            sidemenulist.append(
                f"""html.Li(html.A([
                            html.I('{GroupImage2}',className='material-icons icon'),
                            html.Span('{KPIGroupList2}',className='text nav-text')],href='#',id=dict(type='kpigroup-ex3-reset',index ='{kpigroup}'))
                            ,style = {{'opacity':'25%'}},className='nav-link')"""
            ) 
    sidemenulist2=','.join(sidemenulist)
    sidemenulist3.append(sidemenulist2)
    for i,kpi in enumerate(KPINameListIterate):
        if kpi in KPINameListmodelfilter:  
            enum = str(i + 1)
            dataCompare1 = dftouse[
                (dftouse["KPIName"] == kpi)
            ]
            df_by_LevelName = dataCompare1[["Denominator","Numerator"]]#"Denominator_LP","Numerator_LP"

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
            #value_lp = []
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
           # agnumlp = "df_by_LevelName['Numerator_LP']." + str(eval(AggregateNum)) +"("+meannum[0]+")"
           # agdenomlp = "df_by_LevelName['Denominator_LP']." + str(eval(AggregateDenom)) +"("+meandenom[0]+")"
            df_by_LevelName = df_by_LevelName.assign(Aggnum=eval(agnum))
            valueNum.append(df_by_LevelName['Aggnum'].iloc[0]) 
            df_by_LevelName = df_by_LevelName.assign(Aggdenom=eval(agdenom))
            valueDenom.append(df_by_LevelName['Aggdenom'].iloc[0]) 
            #df_by_LevelName = df_by_LevelName.assign(Aggnum_LP=eval(agnumlp))
            #valueNumLP.append(df_by_LevelName['Aggnum_LP'].iloc[0])
            #df_by_LevelName = df_by_LevelName.assign(Aggdenom_LP=eval(agdenomlp))
            #valueDenomLP.append(df_by_LevelName['Aggdenom_LP'].iloc[0])
            twee = [i / j for i, j in zip(valueNum, valueDenom)]
            #twee_lp = [i / j for i, j in zip(valueNumLP, valueDenomLP)]
            if Calculation == 2:
                CalculationString = twee[0]
               # CalculationStringlp = twee_lp[0]
                value.append(CalculationString)
               # value_lp.append(CalculationStringlp)
            elif Calculation == 1:
                CalculationString = sum(valueNum)
               # CalculationStringlp = sum(valueNumLP)
                value.append(CalculationString)
               # value_lp.append(CalculationStringlp)
            #if value_lp[0]==value[0]:
            #    arrow = "'arrow_right'"
            #elif value_lp[0]<value[0]:
            #    arrow = "'arrow_drop_up'"
            #else:
            #    arrow = "'arrow_drop_down'"
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
            outputactualtxt =str(eval(Notationlist).format(value[0])) 
           # outputlasttxt = str(eval(Notationlist).format(value_lp[0]))
            Card.append(kpi)
            style = {'display': Displayprevious[0] , 'color' : logopositive if HigherIs[kpi]==1 else logonegative if HigherIs[kpi]==2 else logoneutral}
            popbody.append(kpi)
            value.clear()
          #  value_lp.clear()
            notation.clear()
            numbertmp= i+1
            number=str(numbertmp)
            numberi=str(numbertmp)
            carousellistnew.append(
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
                        html.Div(id=dict(type='output-ex3',index = '{kpi}')),
                        dcc.Textarea(value=f'{kpi}',
                                     disabled=True,
                                     draggable=False,
                                     contentEditable=False,
                                     id='Card{number}',
                                     className='col-12 h6'),
                        html.Div(children=[
                            dcc.Textarea(value=f'{outputactualtxt}',
                                id='indicator-graph{number}TXT',
                                contentEditable=False,
                                disabled=True,
                                readOnly=True,
                                draggable=False,
                                className='col-12 h6'
                            ),
                            #html.Div([
                            #     dcc.Textarea(value=f'', 
                            #         id="indicatorlast-graph{number}TXT",
                            #         contentEditable =False,
                            #         disabled=True,
                            #         readOnly=True,
                            #         draggable=False,
                            #         className='col-8 h7',
                            #     ),
                            #     html.I({arrow},className="material-icons icon",id="arrow{number}")
                            #    ],id="indicatorlast-graph{number}TXTLogo",style={style})
                            ])
                    	],id='CardContent{number}'),id=dict(type='filter-dropdown-ex3',index = '{kpi}'),style={style111},className='carddiv')"""
            ) 
        else:
            accordionlist.append(
                f"""html.Div('{kpi}',id=dict(type='filter-dropdown-ex3-reset',index='{kpi}'),className ='KPIRemainingbox h7')"""
            ) 
            if i == len(KPINameListGroupFilter) - 1:
                accordionliststring = str(accordionlist)
                accordionliststring2 = accordionliststring.replace('"', '')
                accordionlist2=','.join(accordionlist)
                accordionlist3.append(accordionlist2)
                lastlistaccordionstring = []
                lastlistaccordionstring.append(eval(accordionlist3[0]))
                carousellistnew.append("html.Div(className='KPIRemainingcontainer',children="+accordionliststring2+")")
            #carousellistnew.append(
            #f"""html.Div(
            #   ,id=dict(type='filter-dropdown-ex3',index = '{kpi}'),style={style111},className='carddiv')"""
            #) 
    accordionlist.clear()
    accordionlist3.clear()
    carousellist2new=','.join(carousellistnew)
    carousellist3new.append(carousellist2new)
    #print(carousellist3new)
    #print(carousellist3new[0])
    if widthBreakpoint =='sm':
        slides_to_showfinal = 1
        slides_to_scrollfinal = 1
    else:
        slides_to_showfinal = slides_to_show
        slides_to_scrollfinal = slides_to_scroll
    divlist=[[html.Div([dbc.Spinner(size='md',delay_hide=1500,children=[dtc.Carousel(eval(carousellist3new[0])
        ,
        slides_to_scroll=slides_to_scrollfinal,
        slides_to_show=slides_to_showfinal,
        center_padding='10px',
        swipe_to_slide=True,
        autoplay=False,
        dots=True,
        speed=120,
       # variable_width=True,
        center_mode=False,
        id='slickthinky',
        className='col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12',
        responsive=[
            ],
        )])])],[html.Nav([html.Header([
                    html.Div([
                    #    html.Div(Radiograin,className="col-sm-12 col-md-12 col-lg-12 col-xl-12 text logo-text")
                    ],className="image-text"),
                    html.I("chevron_right",className='material-icons toggle',id='Opennavbar')
                    ]),
                    html.Div([
                        html.Div([
                          html.Div(html.Span("Performace category",className='text nav-text')),
                          html.Ul(eval(sidemenulist2)
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
                    ],className="sidebar close",id='nav')]
                    ]
    return divlist[0],divlist[1]


@app.callback([Output('tabscontainer', 'style'),
             Output('graph-level1compare', 'style'),
             Output('graphoveralltime', 'style'),
             Output('tabscompare', 'style'),
             Output('graph-compare-kpi', 'style'),
             Output('Tab0drilldown', 'label'),
             Output('Tab1drilldown', 'label'),
             Output('Tab2drilldown', 'label'),
             Output('Tab0drilldown', 'tab_class_name'),
             Output('Tab1drilldown', 'tab_class_name'),
             Output('Tab2drilldown', 'tab_class_name')             
             ],
             [#Input({'type': 'kpigroup-ex3', 'index': ALL}, 'n_clicks'),
              Input('KPISelect','value')
              ])
def hide_graph(KPISelect):
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
    return msg,msg,msg,msg2,msg2,Levelattrr[0],Levelattrr[1],Levelattrr[2],tab_class_name[0],tab_class_name[1],tab_class_name[2]


@app.callback([
             Output('NavItem1', 'style'),
             Output('NavItem2', 'style'),
             Output('NavItem3', 'style'),      
             ],
             [#Input({'type': 'kpigroup-ex3', 'index': ALL}, 'n_clicks'),
              Input('NavItem1','n_clicks'),
              Input('NavItem2','n_clicks'),
              Input('NavItem3','n_clicks'),
              ])
def hide_graph(NavItem1,NavItem2,NavItem3):
    print('execute hide_graph')
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'NavItem1' in changed_id:
        color1 = {'color':buttonlogocolor,'background-color':buttoncolor}
        color2 = {}
        color3 = {}
    elif 'NavItem2' in changed_id:
        color1 = {}
        color2 = {'color':buttonlogocolor,'background-color':buttoncolor}
        color3 = {}
    elif 'NavItem3' in changed_id:
        color1 = {}
        color2 = {}
        color3 = {'color':buttonlogocolor,'background-color': buttoncolor}
    else:
        color1 = {'color':buttonlogocolor, 'background-color': buttoncolor}
        color2 = {}
        color3 = {}
    return color1,color2,color3

#graphlevel0
@app.callback(
    Output('graphlevel0', 'figure'),
   # Output("Category1Select", "value"),
  #  Output("Level0NameSelect", "options"),
   # Output('animatedbar', 'figure'),
    
     Input('dfl0', 'data'),
     Input('GrainSelect', 'value'),
     Input("KPISelect", "value"),
     Input("CumulativeSwitch", "label"),
     Input("PercentageTotalSwitch", "label"),
     Input("ShowValueSwitch", "label"),
     State("breakpoints", "widthBreakpoint"),
)

def update_kpiagg(data00,GrainSelect,KPISelect,CumulativeSwitch,PercentageTotalSwitch,ShowValueSwitch,widthBreakpoint):  #,*args ,Level2NameSelect,toggle, relayoutData
    print('execute update_kpiagg')
    #update_filter_l0(data0, GrainSelect, KPISelect)  # ,Level2NameSelect
    data0 = data00.to_pandas() # pd.DataFrame(data00)
    dff = data0
    #level0options=[{'label': html.Span([i],style={'background-color': Level0NameColor[i]}), 'value': i} for i in dff["LevelName_0"].unique()]#dff["LevelName_0"].unique()
    #level1options=dfll2[0]["LevelName_1"].unique()
    #level2options=dfll2[0]["LevelName_1"].unique()
    #level0filteroptions=[{'label': html.Span([i],style={'background-color': ProjectOrange}), 'value': i}  for i in dff["Filter1_0"].unique()] #dff["Filter1_0"].unique()
    #level1filteroptions=dff["Filter1_1"].unique()
    #level2filteroptions=dff["Filter1_2"].unique()
    traces3 = []
    dataframe = Cumloop0(CumulativeSwitch)
    Notation = KPISelectedStyle(KPISelect)
    Calculation = CalculationDEF(KPISelect)
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
    for i in data0['LevelName_0'].unique():
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
                width=3,
                shape="spline",
            ),
            marker=dict(
                size=5,
                line=dict(width=0.1
                          ),
                color=Level0NameColor[i] #
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
    #print(traces3)
    #animatedreturn = {
    #   px.bar(traces3, x='LevelName_0', y=y, color='LevelName_0', 
    #       animation_frame='Period_int', animation_group='LevelName_0', 
    #       range_y=[0,4000000000]
    #       )
    #}
    if not traces3:
        return {"layout": dict(
        xaxis = dict(visible=False),
        yaxis = dict(visible=False),
        style={'background-color': 'red', 'color': 'white'},
        annotations=[
                        dict(
                            xref="paper",
                            yref="paper",
                            x=0.5,
                            y=0.5,
                            text="No data available",
                            showarrow=False,
                            font=dict(size=26,color=fontcolor),
            )
        ],
        plot_bgcolor='transparent',
        paper_bgcolor='transparent' 
        )
        }
    else:
        return {
            'data': traces3,
            'layout': dict(
                barmode='stack',
                showlegend=False,
                barnorm=eval(PercentageTotalSwitchDEF(PercentageTotalSwitch)),
                xaxis=dict(type='string',
                           title='',
                           showgrid=False,
                           gridwidth=0,
                          # showspikes=True,
                           showline=False,
                           color=fontcolor,
                           rangeselector=dict(
                               buttons=rangeselector(GrainSelect)
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
                          # showspikes=True,
                           color=fontcolor,
                           gridwidth=0.5,
                           font=dict(
                               size=14,
                           )
                           ),
                margin={'l': 60, 'b': 45, 't': 37, 'r': 40}, 
                modebar = dict(
                            bgcolor='transparent',
                            color=BeautifulSignalColor,
                ),
                autosize=True,
                plot_bgcolor=graphcolor,
                paper_bgcolor=graphcolor,
                legend=legend,
                title=title,
                font=dict(
                ),
                images=dict(
                    x = 0,
                    y = 1,
                    sizex=0.2,
                    sizey=0.2,
                ),
                hovermode='x-unified',
                transition={'duration': 50},
            )
        }#,level0filteroptions,level0options#,animatedreturn


@app.callback(
    Output('graph-level0compare', 'figure'),
    [Input('dfl0notime', 'data'),
    # Input('dfl1', 'data'),
     State("KPISelect", "value"),

    # Input('graphlevel0', 'selectedData'),
     Input("Totaalswitch", "label"),
     State("breakpoints", "widthBreakpoint"),
    # eval(kpigrouplistinput3[0]),  
     ]
)
def update_level0Graph(data00,KPISelect,Totaalswitch,widthBreakpoint): #,hoverData,*args
    print('update_level0Graph')
    dff0 = data00.to_pandas() #pd.DataFrame(data00)
    #dff0 = pd.read_json(data00, orient='split')
    traces = []
    if widthBreakpoint=='sm':
        title = ''
    else:
        title = dict(text=str(KPISelect),
                       font=dict(size=22,
                                 color=fontcolor,
                        ),
        ) 
    Notation = KPISelectedStyle(KPISelect)
    Calculation = CalculationDEF(KPISelect)
    AggregateNum = NumaggregateDEF(KPISelect)
    AggregateDenom = DenomaggregateDEF(KPISelect)
    for j in dff0.LevelName_0.unique():
        df_by_Level0Name = dff0[dff0['LevelName_0'] == j]
        x2 = eval(CalculationLogic0(Calculation))
        traces.append(dict(
            #df_by_Level0Name,
            y=df_by_Level0Name.LevelName_0,
            x=x2,
            text=x2,
            text_auto=True,
            texttemplate="%{value:" + eval(Notation[0]) + "}",  # "%{value:.01%}",
            textformat=eval(Notation[0]),
            type='bar',
            marker=dict(
                opacity=1,
                color=Level0NameColor[j],
                color_discrete_map='identity',
                line=dict(width=0.1,
                          color=Level0NameColor[j],
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
    if dff0.empty:
        return {"layout": dict(
            xaxis = dict(visible=False),
            yaxis = dict(visible=False),
            annotations=[
                            dict(
                                xref="paper",
                                yref="paper",
                                x=0.5,
                                y=0.5,
                                text="No data available",
                                showarrow=False,
                                font=dict(size=26,color=fontcolor),
                )
            ],
            plot_bgcolor=graphcolor,
            paper_bgcolor=graphcolor
        )
        }
    else:
        return {
            'data': traces,
            'layout': dict(
                dragmode='select',
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
                hovermode='x-unified',
                transition={'duration': 500},
                style={'overflow': 'auto'}
            )
        }

######################################################################################################################
######################################################################################################################
################################################----tab 1 aanmaken----###############################################
######################################################################################################################
######################################################################################################################

#graphoveralltime
@app.callback(
    Output('graphoveralltime', 'figure'),
 #   Output('Level2NameSelect', 'options'),
    [Input('dfl0', 'data'),
     Input('dfl1', 'data'),
     Input('dfl2', 'data'),
     State('GrainSelect', 'value'),
     State("KPISelect", "value"),
     Input("Totaalswitch", "label"),
     Input("CumulativeSwitch", "label"),
     Input("PercentageTotalSwitch", "label"),
     Input("ShowValueSwitch", "label"),
     State("breakpoints", "widthBreakpoint"),
     #eval(kpigrouplistinput3[0]),  
   #  Input("DBColorVar", "value"),
     ]
)
def update_mainfigure(data00,data11,data22,GrainSelect,KPISelect,Totaalswitch,CumulativeSwitch,PercentageTotalSwitch,ShowValueSwitch,widthBreakpoint):#,*args
    print('execute update_mainfigure')
    data0 =data00.to_pandas()# pd.DataFrame(data00)#(data00, orient='split')
    data1 =data11.to_pandas()# pd.DataFrame(data11) #pd.read_json(data11, orient='split')
    data2 =data22.to_pandas()# pd.DataFrame(data22) #pd.read_json(data22, orient='split')
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
                 width=3,
                 shape="spline",
                 color=Level1NameColor[i],
               ),
               marker=dict(
                   size = 5,
                   line = dict(width=0.1
                               ),
                   color=Level1NameColor[i],
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
                    color=Level0NameColor[v],
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
    if not tracestotal:
        return {"layout": dict(
        xaxis = dict(visible=False),
        yaxis = dict(visible=False),
        style={'background-color': 'red', 'color': 'white'},
        annotations=[
                        dict(
                            xref="paper",
                            yref="paper",
                            x=0.5,
                            y=0.5,
                            text="No data available",
                            showarrow=False,
                            font=dict(size=26,color=fontcolor),
            )
        ],
        plot_bgcolor='transparent',
        paper_bgcolor='transparent' 
        )
        }
    else:
        return {
            'data': tracestotal,
            'layout': dict(
                showlegend=False,
                barmode='stack',
                barnorm=eval(PercentageTotalSwitchDEF(PercentageTotalSwitch)),
                xaxis=dict(type='string',
                           title='',
                           autorange=True,
                           showgrid=False,
                           rangeselector=dict(
                               buttons=rangeselector(GrainSelect)
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
                hovermode='x-unified',
                transition={'duration': 500},
            )
        }#,options


@app.callback(
    Output('graph-level1compare', 'figure'),
    [Input('dfl0notime', 'data'),
     Input('dfl1notime', 'data'),
     State("KPISelect", "value"),
  #   Input("KPIGroupSelect", "value"),
  #   Input("Level1NameSelect", "value"),
  #   Input("Level2NameSelect", "value"),
   #  Input('graphoveralltime', 'clickData'),
     Input("Totaalswitch", "label"),
     State("breakpoints", "widthBreakpoint"),
    # eval(kpigrouplistinput3[0]),  
     ]
)
def update_level1Graph(data00,data11,KPISelect,Totaalswitch,widthBreakpoint): #,KPIGroupSelect,Level1NameSelect,Level2NameSelect,hoverData,*args
    print('execute update_level1Graph')
    data0 =data00.to_pandas()#pd.DataFrame(data00)
    data1 =data11.to_pandas()#pd.DataFrame(data11)
    #data0 = pd.read_json(data00, orient='split')
    #data1 = pd.read_json(data11, orient='split')
    dff1tmp = data1 
    dff0tmp = data0 
   # dff0tmp['Period_int'] = pd.to_datetime(dff0tmp['Period_int']).dt.tz_localize(None)
   # dff1tmp['Period_int'] = pd.to_datetime(dff1tmp['Period_int']).dt.tz_localize(None)
    dff0 = []
    dff1 = []
    dff0 = dff0tmp
    dff1 = dff1tmp
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
    for j in data1['LevelName_1'].unique():
        df_by_Level1Name = dff1[dff1['LevelName_1'] == j]
        x = eval(CalculationLogic1(Calculation))
        for g in appendList1:
            g.append(dict(
                df_by_Level1Name,
                y=df_by_Level1Name.LevelName_1,
                x=x,
                text=x,
                ticktext=df_by_Level1Name.LevelName_1,
                texttemplate="%{value:" + eval(Notation[0]) + "}",
                text_auto=True,
                type='bar',
                marker=dict(
                    color=Level1NameColor[j],
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
    for j in data0.LevelName_0.unique():
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
                    color=Level0NameColor[j],
                    color_discrete_map='identity',
                    line=dict(width=0.1,
                              color=Level0NameColor[j],
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
    if data1.empty:
        return {"layout": dict(
            xaxis = dict(visible=False),
            yaxis = dict(visible=False),
            annotations=[
                            dict(
                                xref="paper",
                                yref="paper",
                                x=0.5,
                                y=0.5,
                                text="No data available",
                                showarrow=False,
                                font=dict(size=26,color=fontcolor),
                )
            ],
            plot_bgcolor=graphcolor,
            paper_bgcolor=graphcolor
            )
        }
    else:
        return {
            'data': tracestotal,
            'layout': dict(
                dragmode='select',
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
                hovermode='x-unified',
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
     Output('graph-with-slider', 'figure')
   # Output('Level2NameSelect','options')
    ,
    [Input('dfl1', 'data'),
     Input('dfl2', 'data'),
     State('GrainSelect', 'value'),
     State("KPISelect", "value"),
     Input("Totaalswitch", "label"),
     Input("CumulativeSwitch", "label"),
     Input("PercentageTotalSwitch", "label"),
     Input("ShowValueSwitch", "label"),
     State("breakpoints", "widthBreakpoint"),
     #eval(kpigrouplistinput3[0]),  
     ]

)


def update_figure(data11,data22,GrainSelect, KPISelect,Totaalswitch,CumulativeSwitch,PercentageTotalSwitch,ShowValueSwitch,widthBreakpoint):#,*args
    print('execute update_figure')
    data1 =data11.to_pandas()# pd.DataFrame(data11) #pd.read_json(data11, orient='split')
    data2 =data22.to_pandas()# pd.DataFrame(data22)
    #data1 = pd.read_json(data11, orient='split')
    #data2 = pd.read_json(data22, orient='split')
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
    #options = [{'label': str(i), 'value': str(i)} for i in Level2NameList]
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
                    width=3,
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
                    color=Level1NameColor[v],
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
            showlegend=False,
            clickmode='event+select',
            barmode='stack',
            barnorm=eval(PercentageTotalSwitchDEF(PercentageTotalSwitch)),
            activeselection = dict(color='red'
                                   ,opacity=0.2),
            xaxis=dict(type='string',
                       title='',
                       rangeselector=dict(
                               buttons=rangeselector(GrainSelect)
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
            hovermode='x-unified',
            transition={'duration': 500},
            fixedrange=False,
        )
    }

#graph-level2compare
@app.callback(
    Output('graph-level2compare', 'figure'),
    [Input('dfl1notime', 'data'),
     Input('dfl2notime', 'data'),
   #  Input('GrainSelect', 'value'),
     State("KPISelect", "value"),
     Input("Totaalswitch", "label"),
     State("breakpoints","widthBreakpoint")
    # eval(kpigrouplistinput3[0]),  
     ]
)
def update_level2Graph(data11,data22,KPISelect,Totaalswitch,widthBreakpoint):#,clickData,*args
    print('execute update_level2Graph')
    data1 =data11.to_pandas()# pd.DataFrame(data11)
    data2 =data22.to_pandas()# pd.DataFrame(data22)
    #data1 = pd.read_json(data11, orient='split')
    #data2 = pd.read_json(data22, orient='split')
    dff2tmp = data2 
    dff1tmp = data1 
   # dff1tmp['Period_int'] = pd.to_datetime(dff1tmp['Period_int']).dt.tz_localize(None)
   # dff2tmp['Period_int'] = pd.to_datetime(dff2tmp['Period_int']).dt.tz_localize(None)
    dff2 = []
    dff1 = []
    dff2 = dff2tmp
    dff1 =  dff1tmp
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
    for i in data2.LevelName_2.unique():
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
                        color=Level2NameColor[i],
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
    for j in dff1['LevelName_1'].unique():
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
                    color=Level1NameColor[j],
                    color_discrete_map='identity',
                    line=dict(color=Level1NameColor[j],
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
    if data2.empty:
        return {"layout": dict(
            xaxis = dict(visible=False),
            yaxis = dict(visible=False),
            annotations=[
                            dict(
                                xref="paper",
                                yref="paper",
                                x=0.5,
                                y=0.5,
                                text="No data available",
                                showarrow=False,
                                font=dict(size=26,color=fontcolor),
                )
            ],
            plot_bgcolor=graphcolor,
            paper_bgcolor=graphcolor
            )
        }
    else:
        return {
            'data': tracestotal,
            'layout': dict(
                dragmode='select',
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
                hovermode='x-unified',
                transition={'duration': 500},
            )
        }


######################################################################################################################
######################################################################################################################
################################################----comparetegel aanmaken----###############################################
######################################################################################################################
######################################################################################################################

"""
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
  #   Input("KPIGroupSelect", "value"),
     Input("KPISelectCompare", "value"),
     Input("Level0NameSelect", "value"),
     Input("Level1NameSelect", "value"),
     Input("Level2NameSelect", "value"),
     Input('tabsdrilldown','active_tab'),
    # eval(kpigrouplistinput3[0]),  
     ]
)


def update_kpicompare(data00,data11,data22,GrainSelect, KPISelect, KPISelectCompare,Level0NameSelect,Level1NameSelect, Level2NameSelect,tabsdrilldown):#,*args
    print('update update_kpicompare')
    data0 = pd.read_json(data00, orient='split')
    data1 = pd.read_json(data11, orient='split')
    data2 = pd.read_json(data22, orient='split')
    if tabsdrilldown == 'tab-0':
        dfftmp = pd.DataFrame(update_filter_l0(data0, GrainSelect, KPISelect,Level0NameSelect))
        dffcomptmp = pd.DataFrame(update_filter_compare_l0(dfl0Compare, GrainSelect, KPISelectCompare))
        TopImageName = dfftmp['LevelName_0'].unique().astype(str)
    elif tabsdrilldown == 'tab-1':
        dfftmp = pd.DataFrame(update_filter_l1(data1, GrainSelect, KPISelect,Level0NameSelect,Level1NameSelect))
        dffcomptmp = pd.DataFrame(update_filter_compare_l1(dfl1Compare, GrainSelect, KPISelectCompare, Level1NameSelect))
        if dfftmp['LevelName_1'].nunique() == 1:
            TopImageName = dfftmp['LevelName_1'].unique().astype(str)
        else:
            TopImageName = dfftmp['LevelName_0'].unique().astype(str)
    elif tabsdrilldown == 'tab-2':
        dfftmp = pd.DataFrame(update_filter_l2(data2, GrainSelect, KPISelect,Level0NameSelect,Level1NameSelect, Level2NameSelect))
        dffcomptmp = pd.DataFrame(update_filter_compare_l2(dfl2Compare, GrainSelect, KPISelectCompare, Level1NameSelect, Level2NameSelect))
        if dfftmp['LevelName_2'].nunique() == 1:
            TopImageName = dfftmp['LevelName_2'].unique().astype(str)
        else:
            TopImageName = dfftmp['LevelName_1'].unique().astype(str)
    else:
        dfftmp = pd.DataFrame(update_filter_l0(data0, GrainSelect, KPISelect,Level0NameSelect))
        dffcomptmp = pd.DataFrame(update_filter_compare_l0(dfl0Compare, GrainSelect, KPISelectCompare))
        TopImageName = dfftmp['LevelName_0'].unique().astype(str)
    TopImageURL = f'assets/Attributes/Images/{TopImageName[0]}.png' if len(TopImageName) == 1 else '' 
    TopImageURLCheck =[]
    if os.path.exists(TopImageURL):
        TopImageURLCheck.append(TopImageURL)
    else:
        TopImageURLCheck.append(f'assets/Attributes/Images/ethereum.png')
    TopImage= 'data:image/png;base64,{}'.format(base64.b64encode(open(TopImageURLCheck[0], 'rb').read()).decode())
    AggregateNum = NumaggregateDEF(KPISelect)
    AggregateDenom = DenomaggregateDEF(KPISelect)
    AggregateNumcomp = NumaggregateDEF(KPISelectCompare)
    AggregateDenomcomp = DenomaggregateDEF(KPISelectCompare)
    dfftmp.fillna(value=0, inplace=True)
    dffcomptmp.fillna(value=0, inplace=True)
    dff = dfftmp.groupby(columnsdftotal, as_index=False, sort=False).agg(
        {'Denominator': [eval(AggregateNumDenom(AggregateDenom))], 'Numerator': [eval(AggregateNumDenom(AggregateNum))]},dtype=object);
    dffcomp = dffcomptmp.groupby(columnsdftotal, as_index=False, sort=False).agg(
        {'Denominator': [eval(AggregateNumDenom(AggregateDenomcomp))], 'Numerator': [eval(AggregateNumDenom(AggregateNumcomp))]},dtype=object);
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
                width=3,
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
                width=3,
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
            hovermode='x-unified',
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
     Input("KPISelectCompare", "value"),
     Input('dflcomparekpi', 'data'),
     #eval(kpigrouplistinput3[0]),  
     ]
)


def update_kpicompare(data00,data11,data22,GrainSelect, KPISelect, KPISelectCompare,dflcomparekpi):#,*args
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
        {'Denominator': [eval(AggregateNumDenom(AggregateDenom))], 'Numerator': [eval(AggregateNumDenom(AggregateNum))]},dtype=object)
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
                width=3,
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
            hovermode='x-unified',
            transition={'duration': 500},
            autosize=True,
        )
    }
"""
#app.config['suppress_callback_exceptions'] = True


@app.callback(
    Output("modal", "is_open"),
    [Input("open-settings", "n_clicks"), Input("close-settings", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("modalfilter", "is_open"),
    [Input("Opennavbar-right", "n_clicks"), Input("close-filter", "n_clicks")],
    [State("modalfilter", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


#app.clientside_callback(
#    """
#    function(className) {
#        var selectValue = document.querySelector('.' + className);
#        selectValue.addEventListener('click', function(e) {
#            if (e.target.classList.contains('Select-value')) {
#                e.target.remove();
#            }
#        });
#    }
#    """,
#    Output("Level0DD", "children"),
#    Input("Level0DD", "id"),
#)

app.clientside_callback(
    """window.onload=function () {
        addListeners()
        return 0
    }""",
    
    Output('nav','n_clicks'),
    Input('nav','children')
)

if __name__ == "__main__":
    print('application loaded')
    app.run_server(debug=True) #,config=config


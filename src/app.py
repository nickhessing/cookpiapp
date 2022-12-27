

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
keys = ['d_kpi_id', 'd_level0_id', 'd_level1_id', 'd_level2_id']  # 'd_date_id',
keysl0 = ['d_kpi_id', 'd_level0_id']
keysl1 = ['d_kpi_id', 'd_level0_id', 'd_level1_id']
ListGrain = ['int_day', 'int_month', 'int_quarter', 'int_year']

# Dataframes
# f_kpi           = pd.read_sql("select * from kpiframework.f_kpi", dbConnection);

KPIFramework = pd.DataFrame(
    pd.read_csv(r'assets/Attributes/dashboard_data/KPIFramework_Python.csv'));
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

KPIFrameworkl0 = KPIFramework.groupby(columnsdf0, as_index=False).agg(
    {'Denominator': 'sum', 'Numerator': 'sum', 'Denominator_LP': 'sum', 'Numerator_LP': 'sum'})

KPIFrameworkl1 = KPIFramework.groupby(columnsdf1, as_index=False).agg(
    {'Denominator': 'sum', 'Numerator': 'sum', 'Denominator_LP': 'sum', 'Numerator_LP': 'sum'})
KPIFrameworkl2 = KPIFramework.groupby(columnsdf2, as_index=False).agg(
    {'Denominator': 'sum', 'Numerator': 'sum', 'Denominator_LP': 'sum', 'Numerator_LP': 'sum'})

KPIFrameworkl0.to_csv(r'assets/Attributes/dashboard_data/KPIFrameworkl0.csv',
                      index=False)
KPIFrameworkl1.to_csv(r'assets/Attributes/dashboard_data/KPIFrameworkl1.csv',
                      index=False)
KPIFrameworkl2.to_csv(r'assets/Attributes/dashboard_data/KPIFrameworkl2.csv',
                      index=False)

d_kpi_tmp = pd.DataFrame(
    pd.read_csv("assets/Attributes/dashboard_data/d_kpi_synthetix.csv", sep=';',
                index_col=False));

d_kpi = d_kpi_tmp[(d_kpi_tmp.live == 1)] #& (df.carrier == "B6")

d_level0 = pd.DataFrame(
    pd.read_csv(r'assets/Attributes/dashboard_data/LEVEL0_Synthetix_Library.csv',
                sep=';', index_col=False));

d_level1 = pd.DataFrame(
    pd.read_csv(r'assets/Attributes/dashboard_data/LEVEL1_Synthetix_Library.csv',
                sep=';', index_col=False));
d_level2 = pd.DataFrame(
    pd.read_csv(r'assets/Attributes/dashboard_data/LEVEL2_Synthetix_Library.csv',
                sep=';', index_col=False));

df_list_l0 = [KPIFrameworkl0, d_kpi, d_level0]
df_list_l1 = [KPIFrameworkl1, d_kpi, d_level0, d_level1]
df_list = [KPIFrameworkl2, d_kpi, d_level0, d_level1, d_level2]  # d_date


dfl0 = df_list_l0[0]
for i, x in zip(df_list_l0[1:], range(len(keysl0))):
    dfl0 = dfl0.merge(i, on=keysl0[x])

dfl0Compare = df_list_l0[0]   
for g, t in zip(df_list[1:], range(len(keysl0))):
    dfl0Compare = dfl0Compare.merge(g, on=keysl0[t])

dfl0["Period_int"] = pd.to_datetime(dfl0["Period_int"])
dfl0Compare["Period_int"] = pd.to_datetime(dfl0Compare["Period_int"])

dfl0.to_csv(r'assets/Attributes/dashboard_data/dfl0.csv', index=False)


dfl1 = df_list_l1[0]
for i, x in zip(df_list_l1[1:], range(len(keysl1))):
    dfl1 = dfl1.merge(i, on=keysl1[x])

dfl1Compare = df_list_l1[0]
for g, t in zip(df_list[1:], range(len(keysl1))):
    dfl1Compare = dfl1Compare.merge(g, on=keysl1[t])

dfl1["Period_int"] = pd.to_datetime(dfl1["Period_int"])
dfl1Compare["Period_int"] = pd.to_datetime(dfl1Compare["Period_int"])

dfl1.to_csv(r'assets/Attributes/dashboard_data/dfl1.csv', index=False)


dfl2 = df_list[0]
for g, t in zip(df_list[1:], range(len(keys))):
    dfl2 = dfl2.merge(g, on=keys[t])


dfl2Compare = df_list[0]
for g, t in zip(df_list[1:], range(len(keys))):
    dfl2Compare = dfl2Compare.merge(g, on=keys[t])

dfl2["Period_int"] = pd.to_datetime(dfl2["Period_int"])
dfl2Compare["Period_int"] = pd.to_datetime(dfl2Compare["Period_int"])

dfl2.to_csv(r'assets/Attributes/dashboard_data/dfl2.csv', index=False)
#href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"

KPINameList =  dfl0['KPIName'].unique()
KPIGroupList = dfl0['KPIGroup'].unique()
GrainNameList = dfl0['Grain'].unique()
Level1NameList = dfl1['Level1Name'].unique()
Level2NameList = dfl2['Level2Name'].unique().tolist()

Level0Name = d_level0['Level0Entitytype'].unique()
Level1Name = d_level1['Level1Entitytype'].unique()
Level2Name = d_level2['Level2Entitytype'].unique()


KPINameListCompare = dfl2Compare['KPIName'].unique()
GrainNameListCompare = dfl2Compare['Grain'].unique()
Level1NameListCompare = dfl1Compare['Level1Name'].unique()
Level2NameListCompare = dfl2Compare['Level2Name'].unique().tolist()

KPINameColor = dict(d_kpi.set_index('d_kpi_id')['KPIName'].to_dict())
Level0NameColor = dict(d_level0.set_index('Level0Name')['Level0Color'].to_dict())
Level1NameColor = dict(d_level1.set_index('Level1Name')['Level1Color'].to_dict())
Level2NameColor = dict(d_level2.set_index('Level2Name')['Level2Color'].to_dict())
KPINotation = dict(d_kpi.set_index('KPIName')['Notation'].to_dict())
KPICalculation = dict(d_kpi.set_index('KPIName')['Calculation'].to_dict())
KPICum = dict(d_kpi.set_index('KPIName')['IsCum'].to_dict())
KPINumAgg = dict(d_kpi.set_index('KPIName')['AggregateNum'].to_dict())
KPIDenomAgg = dict(d_kpi.set_index('KPIName')['AggregateDenom'].to_dict())
KPIColor = dict(d_kpi.set_index('KPIName')['kpicolor'].to_dict())
visual = dict(d_kpi.set_index('KPIName')['visual'].to_dict())
Level0attr = dict(d_kpi.set_index('KPIName')['Level0_Attribuut'].to_dict())
Level1attr = dict(d_kpi.set_index('KPIName')['Level1_Attribuut'].to_dict())
Level2attr = dict(d_kpi.set_index('KPIName')['Level2_Attribuut'].to_dict())
KPIGroupImage = dict(d_kpi.set_index('KPIGroup')['GroupImage'].to_dict())
GroupImage = d_kpi['GroupImage'].unique()
KPICountPerGroup = dict(d_kpi.groupby('KPIGroup')['KPIName'].count().to_dict())

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
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY

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

kpigrouplistinput.append(
        f"""Input('kpigroup0', 'n_clicks')"""
)

for i in range(4):
    numbertmp= i
    numberidtmp= i+1
    number=str(numbertmp)
    numberid=str(numberidtmp)
    kpigrouplistinput.append(
        f"""Input('kpigroup{numberidtmp}','n_clicks')"""
    )

kpigrouplistinput2=','.join(kpigrouplistinput)
kpigrouplistinput3.append(kpigrouplistinput2)

carddivnclicks=[]
carddivnclicks3= []

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


@app.callback([
             Output('KPIGroupSelect', 'value'),
             ],
            eval(kpigrouplistinput3[0])
            )
def KPIgrouplighter(*args):
    kpicountout.clear() 
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    KPIGroup =[]
    KPIGroup.clear()
    KPIGroupList = d_kpi['KPIGroup'].unique().tolist()
    if changed_id =='kpigroup0.n_clicks':
        for i in range(len(KPIGroupList)):
            KPIGroup.append(KPIGroupList[i])
        kpicountout.append(len(KPINameList))
        print('A')
        print(len(KPINameList))
    elif changed_id[0:8] == 'kpigroup':
        listnumber = int(int(changed_id[8])-1)
        KPIGroup.append(KPIGroupList[listnumber])
        kpicountout.append(KPICountPerGroup[KPIGroupList[listnumber]])
        print('B')
        print(KPICountPerGroup[KPIGroupList[listnumber]])
    else:
        for i in range(len(KPIGroupList)):
            KPIGroup.append(KPIGroupList[i])
        kpicountout.append(len(KPINameList))
        print('C')
        print(len(KPINameList))
    kpigrouparray = np.asarray(KPIGroup) 
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
    return [KPIGroup]


KPIdropdownCompare = html.Div([
    dbc.Select(
        id="KPISelectCompare",
        options=[{'label': i, 'value': i} for i in KPINameListCompare],
        value="Ziekteverzuim",
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
                html.Span("All categories",className='text nav-text')],href='#')
                ,id='kpigroup0',className='nav-link')"""
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
                html.Span('{KPIGroupList2}',className='text nav-text')],href='#')
                ,id='kpigroup{numberidtmp}',className='nav-link')"""
    )
navbarlist2=','.join(navbarlist)

navbar = html.Nav([html.Header([
                    html.Div([
                        html.Span(
                            html.Img(src="https://cdn0.iconfinder.com/data/icons/social-media-2091/100/social-32-512.png",alt=''),
                        className='image'),
                        html.Div(
                            html.Span("COOKPI",className='name')
                        ,className="text logo-text")
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
                                ],href='#',id='NavItem1'
                                ),className='nav-link')
                            ,
                            html.Li(html.A(
                                [html.I("balance",className='material-icons icon'),
                                 html.Span("Compare",className='text nav-text')
                                ],href='#',id='NavItem2'
                                ),className='nav-link'
                            ),
                            html.Li(html.A(
                                [html.I("bolt",className='material-icons icon'),
                                html.Span("Predict",className='text nav-text')
                                ],href='#',id='NavItem3'
                                ),className='nav-link'
                            ),
                    ],className='menu-links'
                            )
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

def AggregateNumerator(Calculation):
    if Calculation == 1:
        CalculationString = "'sum'"
        return CalculationString
    elif Calculation == 2:
        CalculationString = "'mean'"
        return CalculationString
    elif Calculation == 3:
        CalculationString = "'max'"
        return CalculationString


def AggregateDenominator(Calculation):
    if Calculation == 1:
        CalculationString = "'sum'"
        return CalculationString
    elif Calculation == 2:
        CalculationString = "'mean'"
        return CalculationString
    elif Calculation == 3:
        CalculationString = "'max'"
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
        & (dfl2["Level1Name"].isin(Level1NameSelect))
        & dfl2["Level2Name"].isin(Level2NameSelect)
        ]
    return dff

def update_filter_compare_l2(dfl2Compare, GrainSelect, KPISelectCompare,Level1NameSelect, Level2NameSelect):
    dffcomp = dfl2Compare[
        (dfl2Compare["Grain"] == GrainSelect)
        & (dfl2Compare["KPIName"] == KPISelectCompare)
        & (dfl2Compare["Level1Name"].isin(Level1NameSelect))
        & dfl2Compare["Level2Name"].isin(Level2NameSelect)
        ]
    return dffcomp

def update_filter_compare_l1(dfl1Compare, GrainSelect, KPISelectCompare,Level1NameSelect):
    dffcomp = dfl1Compare[
        (dfl1Compare["Grain"] == GrainSelect)
        & (dfl1Compare["KPIName"] == KPISelectCompare)
        & (dfl1Compare["Level1Name"].isin(Level1NameSelect))
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
        & (dfl1["Level1Name"].isin(Level1NameSelect))
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
    [dbc.Tab(label=Level0Name, children=[dbc.CardBody(
        dbc.Row([
        dbc.Col(
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
                      ),className="col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12 empty_tab"
        ),
        ],className="row-cols-sm-12 row-cols-md-12 row-cols-lg-12 row-cols-xl-12"
        ),className="row-cols-sm-12 row-cols-md-12 row-cols-lg-11 row-cols-xl-11 pretty_tab"
    )],id="Tab0drilldown"),
    dbc.Tab(label=Level1Name, children=[dbc.CardBody(
    dbc.Row([
    dbc.Col(
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
                  ),className="col-12 col-sm-12 col-md-12 col-lg-8 col-xl-8 empty_tab"
    ),
    dbc.Col(html.Div([
        html.I("delete_sweep",n_clicks=0,id='sweepl1',className="material-icons md-48",style={'position':'absolute','top':'1px','right':'12px','z-index': '1'}),
        dcc.Graph(id='graph-level1compare',
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
                  )
    ],className="col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12 pretty_graph2"
    ),className="col-12 col-sm-12 col-md-12 col-lg-4 col-xl-4 empty_tab2"
    )
    ],className="row-cols-sm-12 row-cols-md-12 row-cols-lg-12 row-cols-xl-12"
    ),className="row-cols-sm-12 row-cols-md-12 row-cols-lg-11 row-cols-xl-11 pretty_tab"
)
],id="Tab1drilldown"),
    dbc.Tab(label=Level2Name, children=[dbc.CardBody(
    dbc.Row([
    dbc.Col(
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
                  ),className="col-12 col-sm-12 col-md-12 col-lg-8 col-xl-8 empty_tab",
    ),
    dbc.Col(dcc.Graph(id='graph-level2compare',
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
                ),className="col-12 col-sm-12 col-md-12 col-lg-4 col-xl-4 empty_tab2"
),
],className="row-cols-sm-12 row-cols-md-12 row-cols-lg-12 row-cols-xl-12"
),className="row-cols-sm-12 row-cols-md-12 row-cols-lg-11 row-cols-xl-11 pretty_tab"
)],id="Tab2drilldown"),
            ],id="tabsdrilldown",active_tab="tab-0")
),


tabscompare = dbc.Tabs(
    [dbc.Tab(label="Compare two",children=[dbc.CardBody(
    dbc.Row([
        dbc.Col(KPIdropdownCompare,
                id='KPICompare'),
        dbc.Col(
            dcc.Graph(id='graph-compare-kpi',
                      config={
                          'modeBarButtonsToRemove': ['pan', 'lasso2d', 'select', 'zoom2d', 'zoomIn', 'zoomOut',
                                                     'hoverCompareCartesian', 'logo', 'autoScale'],
                          'displaylogo': False,
                          'scrollZoom': True,
                      }, className="col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12 pretty_graph",
                      ), className="col-12 col-sm-11 col-md-11 col-lg-12 col-xl-12 empty_tab2",
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
            dcc.Graph(id='graph-compare-kpi2',
                      config={
                          'modeBarButtonsToRemove': ['pan', 'lasso2d', 'select', 'zoom2d', 'zoomIn', 'zoomOut',
                                                     'hoverCompareCartesian', 'logo', 'autoScale'],
                          'displaylogo': False,
                          'scrollZoom': True,
                      }, className="col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12 pretty_graph",
                      ), className="col-12 col-sm-11 col-md-11 col-lg-12 col-xl-12 empty_tab2",
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


app.layout = html.Div([
    dbc.Row([
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
            html.I("filter_alt", id='dropdowncontrol', className="material-icons",style={'text-align': 'left !important'}, n_clicks=0),
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

            html.I("settings_suggest",id='graphset',className="material-icons", style={'text-align': 'left !important'},n_clicks=0),
            dbc.Popover(
                [dbc.PopoverBody(children=[
                        dbc.Col(Radiograin,className="col-sm-12 col-md-12 col-lg-12 col-xl-12"),
                        dbc.Col([Totaalaggregaatswitch], className="col-sm-12 col-md-12 col-lg-12 col-xl-12"),
                        dbc.Col([CumulativeSwitch], className="col-sm-12 col-md-12 col-lg-12 col-xl-12"),
                        dbc.Col([TargetSwitch], className="col-sm-12 col-md-12 col-lg-12 col-xl-12"),
                        dbc.Col([PercentageTotalSwitch], className="col-sm-12 col-md-12 col-lg-12 col-xl-12"),
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
            html.Div(navbar),
          #  html.Div(KPI_Group,className="col-sm-11 col-md-11 col-lg-4 col-xl-3"),

    ]
    ),
    html.Span(html.I(''),style={'margin-top': '5em','display': 'block'}),
    dcc.Store(id='dfl0',data=[],storage_type='memory'),
    dcc.Store(id='dfl1',data=[],storage_type='memory'),
    dcc.Store(id='dfl2',data=[],storage_type='memory'),
    dcc.Store(id='dffcomparefilter',data=[],storage_type='memory'),
    dcc.Store(id='dflcomparekpi',data=[],storage_type='memory'),
    dcc.Store(id='selectedkpigroup',data=[],storage_type='memory'),
    dbc.Row([
        #html.Div([dcc.DatePickerRange(
        #            id='my-date-picker-range',
        #            min_date_allowed=date(2010, 1, 1),
        #            max_date_allowed=date(2030, 12, 31),
        #            initial_visible_month=date(2020, 1, 1),
        #            end_date=date(2022, 10, 31),
        #            style={"color": "red"}
        #         ),
        html.Div(id='output-container-date-picker-range',
                 style={'margin-left': '20px'},
                 className='h6')
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


@app.callback([
        Output('KPISelect', 'options'),
        ],
     Input("KPIGroupSelect", "value"),
     eval(kpigrouplistinput3[0]),
)

def update_KPI_Options(KPIGroupSelect,*args):
    dff = dfl2[
        (dfl2["KPIGroup"].isin(KPIGroupSelect))
    ]
    KPINameListOptions = dff['KPIName'].unique()
    options = [{'label': i, 'value': i} for i in KPINameListOptions],
    return options 


@app.callback([
    Output('KPISelect', 'value'),
    ],
    
    Input('KPIGroupSelect', 'value'),
    eval(carddivnclicks3[0]),
    eval(kpigrouplistinput3[0])
    
)

def update_df_KPIGroup(KPIGroupSelect,*args): 
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    dff = dfl2[
        (dfl2["KPIGroup"].isin(KPIGroupSelect))
    ]
    KPINameList = dff['KPIName'].unique()
    options = [{'label': i, 'value': i} for i in KPINameList],
    dffkpi = dff["KPIName"].drop_duplicates()
    kpi =[]
    kpi.clear()
    
    if 'kpigroup' in changed_id[0:8]:
        kpi.append(dffkpi.iloc[0])
    elif 'carddiv' in changed_id[0:7]:
        listnumber = int(int(changed_id[7])-1)
        kpi.append(dffkpi.iloc[listnumber])
        carddivselected = changed_id[0:8]
         #   carddivstyle.append(f"""Output("{carddivselected}", "style")""")        
    else:
        kpi.append(dffkpi.iloc[0])
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
    return kpi

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
             Output('NavItem3', 'style')],
             [Input('NavItem1','n_clicks'),
              Input('NavItem2','n_clicks'),
              Input('NavItem3','n_clicks'),
              Input('KPISelect','value'),
              ])
def hide_graph(NavItem1,NavItem2,NavItem3,KPISelect):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
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
    return msg,msg,msg,msg2,msg2,color1,color2,color3




datefromtmp = []
datetotmp = []
datefromtmp.append(str(dfl2['Period_int'].min())[0:10])
datetotmp.append(str(dfl2['Period_int'].max())[0:10])

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
             # Input('graphlevel0', 'selectedData'),
             # Input('graphoveralltime', 'selectedData'),
             # Input('graph-with-slider', 'selectedData'),
              Input('graphlevel0', 'clickData'),
              Input('graphoveralltime', 'clickData'),
              Input('graph-with-slider', 'clickData'),
              Input('tabsdrilldown','active_tab'),
              Input("Level1NameSelect", "value"),
              Input("Level2NameSelect", "value"),
              Input('graph-level1compare', 'clickData'),
              Input('graph-level2compare', 'clickData'),
              Input('sweepl1','n_clicks'),
              eval(kpigrouplistinput3[0]),
              )
def clean_data(GrainSelect,KPISelect,relayoutDatal0,relayoutDatal1,relayoutDatal2,clickdatal0,clickdatal1,clickdatal2,tabsdrilldown,Level1NameSelect,Level2NameSelect,clickdatal1bar,clickdatal2bar,sweepl1,*args):
    dfll0 = []
    dfll1 = []
    dfll2 = []
    
    dfllCompare = []
    dff0 = update_filter_l0(dfl0, GrainSelect, KPISelect)
    dff1 = update_filter_l1(dfl1, GrainSelect, KPISelect, Level1NameSelect)
    dff2 = update_filter_l2(dfl2, GrainSelect, KPISelect, Level1NameSelect, Level2NameSelect)
    dffcompare0 = dfl0[
        (dfl0["Grain"] == GrainSelect)
        ]
    dffcompare1 = dfl1[
        (dfl1["Grain"] == GrainSelect)
        & (dfl1["Level1Name"].isin(Level1NameSelect))
        ]
    dffcompare2 = dfl2[
        (dfl2["Grain"] == GrainSelect)
        & (dfl2["Level1Name"].isin(Level1NameSelect))
        & (dfl2["Level2Name"].isin(Level2NameSelect))
        ]
    dffcompare = []
    if tabsdrilldown == 'tab-0':
        relayoutdata1 = relayoutDatal0
        clickdatabar1 = clickdatal1bar
        clickdata1 = clickdatal0
        changeid = 'graphlevel0.relayoutData'
        dffcompare.append(dffcompare0)
    elif tabsdrilldown == 'tab-1':
        relayoutdata1 = relayoutDatal1
        clickdatabar1 = clickdatal1bar
        clickdata1 = clickdatal1
        changeid = 'graphoveralltime.relayoutData'
        dffcompare.append(dffcompare1)
    elif tabsdrilldown == 'tab-2':
        relayoutdata1 = relayoutDatal2
        clickdatabar1 = clickdatal2bar
        clickdata1 = clickdatal2
        changeid = 'graph-with-slider.relayoutData'
        dffcompare.append(dffcompare2)
    else:
        relayoutdata1 = relayoutDatal0
        changeid = 'graphlevel0.relayoutData'
        clickdatabar1 = clickdatal1bar
        clickdata1 = clickdatal0
        dffcompare.append(dffcompare0)
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if relayoutdata1 == {'autosize': True} or relayoutdata1 == None:
        ''
    elif changed_id == changeid:
        datefromtmp.append(relayoutdata1['xaxis.range[0]'][0:10])
        datetotmp.append(relayoutdata1['xaxis.range[1]'][0:10])
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
    else:
        datefromtmp.append(relayoutdata1['xaxis.range[0]'][0:10])
        datetotmp.append(relayoutdata1['xaxis.range[1]'][0:10])

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
    if clickdatabar1 == "{'autosize': True}" or clickdatabar1 == None:
        dffl0click.append(dffl0)
        dffl1click.append(dffl1)
        dffl2click.append(dffl2)
    elif changed_id  == 'sweepl1.n_clicks':
        dffl0click.append(dffl0)
        dffl1click.append(dffl1)
        dffl2click.append(dffl2)
    elif changed_id  == 'graph-level1compare.clickData': 
        dffl0click.append(dffl0[dffl0['Level0Name'] == clickdatabar1['points'][0]['y']])
        dffl1click.append(dffl1[dffl1['Level1Name'] == clickdatabar1['points'][0]['y']])
        dffl2click.append(dffl2[dffl2['Level2Name'] == clickdatabar1['points'][0]['y']])
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
        Displaypreviouscount.append() 
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

    return dffl0json,dffl1json,dffl2json,dffcomparejson,comparejson,string_prefix#,style,style,style,style,style#,clickdatasend

datefromtmp.clear()
datetotmp.clear()  

@app.callback(
    Output('cardsid', 'children')
    ,
    Input('dflcomparekpi', 'data'),
    Input('dfl0','data'),
    Input('dffcomparefilter', 'data'),
    Input('tabsdrilldown','active_tab'),
    Input("KPIGroupSelect", "value"),
    #Input("Perioddropdown", "value"),
    Input('graphlevel0', 'clickData'),
    Input('graphoveralltime', 'clickData'),
    Input('graph-with-slider', 'clickData'),
    eval(kpigrouplistinput3[0]),  
)

def updatekpiindicator(compareset,dfl0,dffcomparefilter,tabsdrilldown,KPIGroupSelect,clickData0,clickDatal1,clickDatal2,*args): #KPISelect
   # dfl0 = pd.read_json(dfl0, orient='split')
    dffcomparefilter = pd.read_json(dffcomparefilter, orient='split')
   # dfl2 = pd.read_json(dfl2click, orient='split')
    dataCompare = pd.read_json(compareset, orient='split')
   # if tabsdrilldown == 'tab-0':
   #     dftouse = dfl0
   # elif tabsdrilldown == 'tab-1':
   #     dftouse = dfl1
   # elif tabsdrilldown == 'tab-2':
   #     dftouse = dfl2
   # else:
   #     dftouse = dfl0
    #carousellist = []
    #carousellist3 = []
    carousellist.clear()
    carousellist3.clear()
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    KPIGroup =[]
    KPIGroupList = d_kpi['KPIGroup'].unique().tolist()
    for i in range(len(KPIGroupList)):
        KPIGroup.append(KPIGroupList[i])
    if changed_id =='kpigroup0.n_clicks':
        KPIGroup.clear()
        for i in range(len(KPIGroupList)):
            KPIGroup.append(KPIGroupList[i])
        kpicountout.append(len(KPINameList))
    elif changed_id[0:8] == 'kpigroup':
        KPIGroup.clear()
        listnumber = int(int(changed_id[8])-1)
        KPIGroup.append(KPIGroupList[listnumber])
        kpicountout.append(KPICountPerGroup[KPIGroupList[listnumber]])
    else:
        KPIGroup.clear()
        for i in range(len(KPIGroupSelect)):
            KPIGroup.append(KPIGroupSelect[i])
    print('----------------------------')
    print(KPIGroupSelect)
    print('----------------------------')
    print(KPIGroup)
    print('----------------------------')
    print(changed_id)
    print('----------------------------')
    if kpicountout[0]<slides_to_show_ifenough:
        slides_to_show = kpicountout[0]
    else:
        slides_to_show = slides_to_show_ifenough
    
    dftouse = dffcomparefilter[
            (dffcomparefilter["KPIGroup"].isin(KPIGroup))
        ]
    KPINameList2 = dftouse['KPIName'].unique()
    outputactual =[]
    outputactualtxt =[]
    outputlasttxt =[]
    outputlast = []
    Card = []
    Cardstyle = []
    popbody = []
    carddivstyle = []
    outputlasttxtlogo = []
    arrow= []
    outputactual.clear()
    outputactualtxt.clear()
    Card.clear()
    Cardstyle.clear()
    carddivstyle.clear()
    arrow.clear()
    popbody.clear()
    outputlasttxtlogo.clear()
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
        style = {'display': Displayprevious[0]}
        logopositive = {"color": "green"}
        logonegative = {'color' : 'red'}
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
        AggregateNum = AggregateNumerator(Calculation)
        AggregateDenom = AggregateDenominator(Calculation)
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
        elif value_lp[0]==value[0]:
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
        style111 = {'box-shadow': f'0px -0px 5px 2px {Highlightcardcolor}'}
        stylempty = {}
        style222 = {'color': f'{BeautifulSignalColor}'}
        outputactualtxt =str(eval(Notationlist).format(value_lp[0])) #value[0]#eval(Notationlist).format(value[0]),
        outputlasttxt = str(eval(Notationlist).format(value[0])) #value[0]#eval(Notationlist).format(value[0]),
        Card.append(kpi)
        Cardstyle.append(style222)
        popbody.append(kpi)
        outputlasttxtlogo = logopositive
        if kpi==kpi:   #KPISelect:
            carddivstyle.append(style111)
        else:
            carddivstyle.append(stylempty)
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
                	],id='CardContent{number}'),id='carddiv{number}',className='carddiv')"""
        ) 
   # print(outputactualtxt[0])
   # print(outputlasttxt[0])
   # print(Card[0])
   # print(popbody[0])
    carousellist2=','.join(carousellist)
    carousellist3.append(carousellist2)
    print(changed_id)
    return [html.Div(dtc.Carousel(eval(carousellist3[0])
        ,
        slides_to_scroll=slides_to_scroll,
        slides_to_show=slides_to_show,
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
    ))
    ]


######################################################################################################################
######################################################################################################################
################################################----tab 0 aanmaken----###############################################
######################################################################################################################
######################################################################################################################


@app.callback(
    eval(carddivstyle3[0])
    , 
    [   
    Input("KPISelect", "value"),
    Input("KPIGroupSelect", "value"),
    eval(kpigrouplistinput3[0]),
    eval(carddivnclicks3[0])
    ]
)

def update_df_KPI(KPISelect,KPIGroupSelect,*args):
    dff1 = dfl1[
    (dfl1["KPIName"] == KPISelect)
    ]
    dff = dfl1[
        (dfl1["KPIGroup"].isin(KPIGroupSelect))
    ]
    KPINameList = dff['KPIName'].unique()
    print('00000000000')
    print('00000000000')
    print(KPISelect)
    print(KPIGroupSelect)
    print('00000000000')
    print('00000000000')
    listtop =[{'label': i, 'value': i} for i in dff1["Level1Name"].unique()]
    cardstyle = []
    cardstyle.clear()
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    for i in KPINameList:
        if i == KPISelect:
            cardstyle.append({'box-shadow': f'0px -0px 9px 0px {BeautifulSignalColor}'})
        else:
            cardstyle.append({'box-shadow':'0px 0px 9px 0px transparent'})
    if IsCum(KPISelect) == 1:
        IsCumStyle= {'display': 'block'}
    else:
        IsCumStyle= {'display': 'none'}
    return eval(carddivstylereturn3[0])

#graphlevel0
@app.callback(
    Output('graphlevel0', 'figure'),
     
     Input('dfl0', 'data'),
     Input('GrainSelect', 'value'),
     Input("KPISelect", "value"),
     Input("CumulativeSwitch", "label"),
     Input("PercentageTotalSwitch", "label"),
     eval(kpigrouplistinput3[0]),  
   #  eval(carddivnclicks3[0]),
   #  eval(kpigrouplistinput3[0])
 #    Input('graphoveralltime', 'relayoutData'),
 #    Input('graph-with-slider', 'relayoutData'),
   #  Input("graphlevel0","relayoutData"),
     
)

def update_kpiagg(data00,GrainSelect,KPISelect,CumulativeSwitch,PercentageTotalSwitch,*args):  # ,Level2NameSelect,toggle, relayoutData
    data0 = pd.read_json(data00, orient='split')
    dff = data0 #update_filter_l0(data0, GrainSelect, KPISelect)  # ,Level2NameSelect
    traces3 = []
    dataframe = Cumloop0(CumulativeSwitch)
    Notation = KPISelectedStyle(KPISelect)
    Calculation = CalculationDEF(KPISelect)
    Notation = KPISelectedStyle(KPISelect)
    Calculation = CalculationDEF(KPISelect)
    for i in dff.Level0Name.unique():
        df_by_Level0Name = dff[dff['Level0Name'] == i]
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
            text=y,
            text_auto=True,
            mode=linesormarkers(GrainSelect),
            opacity=1,
            customdata=eval(dataframe[0]).Level0Name,
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
                    dict(target='Numerator', func=AggregateNumerator(Calculation)),  # , enabled=True
                    dict(target='Denominator', func=AggregateDenominator(Calculation))  # , enabled=True
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
                ),
                orientation="h",
                yanchor="top",
                y=0.99,
                x=0.01,
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
     #Input("Level1NameSelect", "value"),
     #Input("Level2NameSelect", "value"),
     Input("Totaalswitch", "label"),
     Input("CumulativeSwitch", "label"),
     Input("PercentageTotalSwitch", "label"),
     eval(kpigrouplistinput3[0]),  
   #  Input("DBColorVar", "value"),
     ]
)
def update_mainfigure(data00,data11,data22,GrainSelect,KPISelect,Totaalswitch,CumulativeSwitch,PercentageTotalSwitch,*args):#
    data0 = pd.read_json(data00, orient='split')
    data1 = pd.read_json(data11, orient='split')
    data2 = pd.read_json(data22, orient='split')
    dff = data1  
    dff2 = data2 
    dff0 = data0 
    Level2NameList = dff2['Level2Name'].unique().tolist()
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
    for z in appendList1:
        for i in dff.Level1Name.unique():
           df_by_Level1Name = dff[dff['Level1Name'] == i]
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
               text=y,
               text_auto=True,
               mode=linesormarkers(GrainSelect),
               opacity=1,
               customdata=eval(dataframe1[0]).Level1Name,
               line=dict(
                 width=2,
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
                       dict(target='Numerator', func=AggregateNumerator(Calculation)),  # , enabled=True
                       dict(target='Denominator', func=AggregateDenominator(Calculation))  # , enabled=True
                   ]
               ),
           )
           )
    for d in appendList2:
        for v in dff0.Level0Name.unique():
            df_by_Level0Name = dff0[dff0['Level0Name'] == v]
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
                customdata=eval(dataframe0[0]).Level0Name,
                mode=linesormarkers(GrainSelect),
                opacity=1,
                marker=dict(
                    size = 5,
                    color=eval(dataframe0[0]).Level0Color,
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
                        dict(target='Numerator', func=AggregateNumerator(Calculation)),  # , enabled=True
                        dict(target='Denominator', func=AggregateDenominator(Calculation))  # , enabled=True
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
            title=dict(text=str(KPISelect) + ' per '+str(Level1Name[0]),  # +' -     selected: '+str(Level2NameSelect),
                       font=dict(size=22,
                                 color=fontcolor,
                           ),
                       ),
            hovermode='closest',
            transition={'duration': 500},
        )
    },options


@app.callback(
    Output('graph-level1compare', 'figure'),
    [Input('dfl0', 'data'),
     Input('dfl1', 'data'),
     Input("KPISelect", "value"),
     Input('graphoveralltime', 'clickData'),
     Input("Totaalswitch", "label"),
     eval(kpigrouplistinput3[0]),  
     ]
)
def update_level1Graph(data00,data11,KPISelect,clickData,Totaalswitch,*args): #,hoverData
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
    totaaljanee = Totaalloop(Totaalswitch)
    appendList1 = [tracestotal, traces]
    appendList2 = eval(totaaljanee)
    Notation = KPISelectedStyle(KPISelect)
    Calculation = CalculationDEF(KPISelect)
    AggregateNum = NumaggregateDEF(KPISelect)
    AggregateDenom = DenomaggregateDEF(KPISelect)
    for j in dfl1.Level1Name.unique():
        df_by_Level1Name = dff1[dff1['Level1Name'] == j]
        x = eval(CalculationLogic1(Calculation))
        for g in appendList1:
            g.append(dict(
                df_by_Level1Name,
                y=df_by_Level1Name.Level1Name,
                x=x,
                text=x,
                texttemplate="%{value:" + eval(Notation[0]) + "}",
                text_auto=True,
                type='bar',
                marker=dict(
                    color=df_by_Level1Name.Level1Color,
                    color_discrete_map='identity',
                ),
                orientation="h",
                name=i,
                transforms=[dict(
                    type='aggregate',
                    groups=df_by_Level1Name.Level1Name,
                    aggregations=[
                        dict(target='Numerator', func=AggregateNumerator(Calculation)),  # , enabled=True
                        dict(target='Denominator', func=AggregateDenominator(Calculation))  # , enabled=True
                    ]
                ),
                ]
            ))
    for j in dfl1.Level0Name.unique():
        df_by_Level0Name = dff0[dff0['Level0Name'] == j]
        x2 = eval(CalculationLogic0(Calculation))
        for g in appendList2:
            g.append(dict(
                df_by_Level0Name,
                y=df_by_Level0Name.Level0Name,
                x=x2,
                text=x2,
                text_auto=True,
                texttemplate="%{value:" + eval(Notation[0]) + "}",  # "%{value:.01%}",
                textformat=eval(Notation[0]),
                type='bar',
                marker=dict(
                    opacity=1,
                    color=df_by_Level0Name.Level0Color,
                    color_discrete_map='identity',
                    line=dict(width=0.1,
                              color=df_by_Level0Name.Level0Color,
                              color_discrete_map='identity',
                              opacity=1,
                              ),
                ),
                orientation="h",
                name=j,
                transforms=[dict(
                    type='aggregate',
                    groups=df_by_Level0Name.Level0Name,
                    aggregations=[
                        dict(target='Numerator', func=AggregateNumerator(AggregateNum)),  
                        dict(target='Denominator', func=AggregateDenominator(AggregateDenom))  
                    ]
                ),
                ]
            ))
    return {
        'data': tracestotal,
        'layout': dict(
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
            title=dict(text='Compare over level 2',
                       font=dict(size=22,
                                 color=fontcolor,
                           )),
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
    # Input("Level1NameSelect", "value"),
   #  Input("Level2NameSelect", "value"),
     Input("Totaalswitch", "label"),
     Input("CumulativeSwitch", "label"),
     Input("PercentageTotalSwitch", "label"),
     eval(kpigrouplistinput3[0]),  
     ]

)


def update_figure(data11,data22,GrainSelect, KPISelect,Totaalswitch,CumulativeSwitch,PercentageTotalSwitch,*args):
    data1 = pd.read_json(data11, orient='split')
    data2 = pd.read_json(data22, orient='split')
    dff = data2 
    dff2 = data1
    Level2NameList = dff['Level2Name'].unique().tolist()
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
        for i in dfl2.Level2Name.unique():
            df_by_Level2Name = dff[dff['Level2Name'] == i]
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
                text=y,
                text_auto=True,
                customdata=eval(dataframe2[0]).Level2Name,
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
                        dict(target='Numerator', func=AggregateNumerator(Calculation)),   
                        dict(target='Denominator', func=AggregateDenominator(Calculation))
                    ]
                ),
                ]
            ))
    for d in appendList2:
        for v in dfl1.Level1Name.unique():
            df_by_Level1Name = dff2[dff2['Level1Name'] == v]
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
                customdata=eval(dataframe[0]).Level1Name,
                mode=linesormarkers(GrainSelect),
                marker=dict(
                    size = 5,
                    color=eval(dataframe[0]).Level1Color,
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
                        dict(target='Numerator', func=AggregateNumerator(Calculation)),    
                        dict(target='Denominator', func=AggregateDenominator(Calculation)) 
                    ]
                ),
                ]
            ))
    return {
        'data': tracestotal,
        'layout': dict(
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
            title=dict(text=str(KPISelect) + ' per '+str(Level2Name[0]),# + Level2Entitytype,
                       # +' -     selected: '+str(Level2NameSelect),
                       font=dict(#family='Montserrat',
                                 size=22,
                                 color=fontcolor,
                        ),
                       ),
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
    # Input('graph-with-slider', 'hoverData'),
     Input('graph-with-slider', 'clickData'),
  #   Input('Perioddropdown', 'value'),
    # Input("Level1NameSelect", "value"),
    # Input("Level2NameSelect", "value"),
     Input("Totaalswitch", "label"),
     eval(kpigrouplistinput3[0]),  
     ]
)
def update_level2Graph(data11,data22,KPISelect,clickData,Totaalswitch,*args):
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
    totaaljanee = Totaalloop(Totaalswitch)
    appendList1 = [tracestotal, traces]
    appendList2 = eval(totaaljanee)
    Notation = KPISelectedStyle(KPISelect)
    Calculation = CalculationDEF(KPISelect)
    AggregateNum = NumaggregateDEF(KPISelect)
    AggregateDenom = DenomaggregateDEF(KPISelect)
    for i in dfl2.Level2Name.unique():
        df_by_Level2Name = dff2[dff2['Level2Name'] == i]
        x = eval(CalculationLogic2(Calculation))
        for z in appendList1:
            z.append(dict(
                df_by_Level2Name,
                y=df_by_Level2Name.Level2Name,
                x=x,
                text=x,
                texttemplate="%{value:"+eval(Notation[0])+"}",#"%{value:.01%}",
                textformat=eval(Notation[0]),
                text_auto=True,
                marker = dict(
                        color=df_by_Level2Name.Level2Color,
                        color_discrete_map='identity',
                        line = dict(width=0.1)
                ),
                type='bar',
                orientation="h",
                name=i,
                transforms=[dict(
                    type='aggregate',
                    groups=df_by_Level2Name.Level2Name,
                    aggregations=[
                        dict(target='Numerator', func=AggregateNumerator(AggregateNum)),  # , enabled=True
                        dict(target='Denominator', func=AggregateDenominator(AggregateDenom))  # , enabled=True
                    ]
                ),
                ]
            ))
    for j in dfl1.Level1Name.unique():
        df_by_Level1Name = dff1[dff1['Level1Name'] == j]
        x2 = eval(CalculationLogic1(Calculation))
        for g in appendList2:
            g.append(dict(
                df_by_Level1Name,
                y=df_by_Level1Name.Level1Name,
                x=x2,
                text=x2,
                texttemplate="%{value:" + eval(Notation[0]) + "}",  # "%{value:.01%}",
                textformat=eval(Notation[0]),
                text_auto=True,
                type='bar',
                marker=dict(
                    opacity=1,
                    color=df_by_Level1Name.Level1Color,
                    color_discrete_map='identity',
                    line=dict(color=df_by_Level1Name.Level1Color,
                              width=0.1
                              ),
                ),
                orientation="h",
                name=j,
                transforms=[dict(
                    type='aggregate',
                    groups=df_by_Level1Name.Level1Name,
                    aggregations=[
                        dict(target='Numerator', func=AggregateNumerator(AggregateNum)),  # , enabled=True
                        dict(target='Denominator', func=AggregateDenominator(AggregateDenom))  # , enabled=True
                    ]
                ),
                ]
            ))
    return {
        'data': tracestotal,
        'layout': dict(
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
            title=dict(text='Compare over level 2',
                       font=dict(size=22,
                                 color=fontcolor,
                           )),
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
     Input("KPISelectCompare", "value"),
     Input("Level1NameSelect", "value"),
     Input("Level2NameSelect", "value"),
     Input('tabsdrilldown','active_tab'),
     eval(kpigrouplistinput3[0]),  
     ]
)


def update_kpicompare(data00,data11,data22,GrainSelect, KPISelect, KPISelectCompare,Level1NameSelect, Level2NameSelect,tabsdrilldown,*args):
    data0 = pd.read_json(data00, orient='split')
    data1 = pd.read_json(data11, orient='split')
    data2 = pd.read_json(data22, orient='split')
    if tabsdrilldown == 'tab-0':
        dfftmp = pd.DataFrame(update_filter_l0(data0, GrainSelect, KPISelect))
        dffcomptmp = pd.DataFrame(update_filter_compare_l0(dfl0Compare, GrainSelect, KPISelectCompare))
        TopImageName = dfftmp['Level0Name'].unique().astype(str)
    elif tabsdrilldown == 'tab-1':
        dfftmp = pd.DataFrame(update_filter_l1(data1, GrainSelect, KPISelect,Level1NameSelect))
        dffcomptmp = pd.DataFrame(update_filter_compare_l1(dfl1Compare, GrainSelect, KPISelectCompare, Level1NameSelect))
        if dfftmp['Level1Name'].nunique() == 1:
            TopImageName = dfftmp['Level1Name'].unique().astype(str)
        else:
            TopImageName = dfftmp['Level0Name'].unique().astype(str)
    elif tabsdrilldown == 'tab-2':
        dfftmp = pd.DataFrame(update_filter_l2(data2, GrainSelect, KPISelect,Level1NameSelect, Level2NameSelect))
        dffcomptmp = pd.DataFrame(update_filter_compare_l2(dfl2Compare, GrainSelect, KPISelectCompare, Level1NameSelect, Level2NameSelect))
        if dfftmp['Level2Name'].nunique() == 1:
            TopImageName = dfftmp['Level2Name'].unique().astype(str)
        else:
            TopImageName = dfftmp['Level1Name'].unique().astype(str)
    else:
        dfftmp = pd.DataFrame(update_filter_l0(data0, GrainSelect, KPISelect))
        dffcomptmp = pd.DataFrame(update_filter_compare_l0(dfl0Compare, GrainSelect, KPISelectCompare))
        TopImageName = dfftmp['Level0Name'].unique().astype(str)
    TopImageURL = f'assets/attributes/Images/{TopImageName[0]}.png' 
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
        {'Denominator': [eval(AggregateDenominator(AggregateDenom))], 'Numerator': [eval(AggregateNumerator(AggregateNum))], 'Denominator_LP': [eval(AggregateDenominator(AggregateDenom))], 'Numerator_LP': [eval(AggregateNumerator(AggregateNum))]},dtype=object);
    dffcomp = dffcomptmp.groupby(columnsdftotal, as_index=False, sort=False).agg(
        {'Denominator': [eval(AggregateDenominator(AggregateDenomcomp))], 'Numerator': [eval(AggregateNumerator(AggregateNumcomp))], 'Denominator_LP': [eval(AggregateDenominator(AggregateDenomcomp))], 'Numerator_LP': [eval(AggregateNumerator(AggregateNumcomp))]},dtype=object);
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
                    dict(target='Numerator', func=AggregateNumerator(Calculation)),  
                    dict(target='Denominator', func=AggregateDenominator(Calculation))  
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
                    dict(target='Numerator', func=AggregateNumerator(CalculationComp)),  # , enabled=True
                    dict(target='Denominator', func=AggregateDenominator(CalculationComp))  # , enabled=True
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
     Input("KPISelectCompare", "value"),
     Input("Level1NameSelect", "value"),
     Input("Level2NameSelect", "value"),
     Input('tabsdrilldown','active_tab'),
     Input('dffcomparefilter', 'data'),
     eval(kpigrouplistinput3[0]),  
     ]
)


def update_kpicompare(data00,data11,data22,GrainSelect, KPISelect, KPISelectCompare,Level1NameSelect, Level2NameSelect,tabsdrilldown,dflcomparekpi,*args):
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
        {'Denominator': [eval(AggregateDenominator(AggregateDenom))], 'Numerator': [eval(AggregateNumerator(AggregateNum))], 'Denominator_LP': [eval(AggregateDenominator(AggregateDenom))], 'Numerator_LP': [eval(AggregateNumerator(AggregateNum))]},dtype=object)
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

#import dash_leaflet as dl
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from jupyter_dash import JupyterDash
from datetime import datetime, timedelta
import dash
import plotly.graph_objs as go
import numpy as np
import country_converter as coco
import dash_auth
import plotly.figure_factory as ff
import chart_studio.plotly as py
from chart_studio.grid_objs import Column, Grid
from IPython.display import IFrame
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash('auth')
VALID_USERNAME_PASSWORD_PAIRS = [
    ['aeropuntual', 'proyectolatam']
]
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
server = app.server
@server.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'),
                               'favicon.ico', mimetype='image/png')
app.title = 'AEROPUNTUAL'
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

df_importance1 = pd.read_csv('latam_features.csv')
df_importance1 = df_importance1[df_importance1['importance'] >= 0.04]

df_importance2 = pd.read_csv('nolatam_features.csv')
df_importance2 = df_importance2[df_importance2['importance'] >= 5.5]
# see https://plotly.com/python/px-arguments/ for more options
df_bar = pd.read_csv('data_final.csv')

df_bar['atraso2'] = df_bar['atraso'].replace([0, 1], ['puntual', 'atrasado'])

df_bar_atraso = df_bar[df_bar['atraso'] == 1]

df_bar_puntual = df_bar[df_bar['atraso'] == 0]

df_bar_atraso_chile = df_bar_atraso[df_bar_atraso['dest_pais'] == 'CL']

df_chile = df_bar[df_bar['dest_pais'] == 'CL']

data1 = [
    go.Bar(
        x=df_bar_puntual['mes'].value_counts().sort_index(),
        y=['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],
        orientation='h',
        text="",
        name='Puntual',
    ),
    go.Bar(
        x=df_bar_atraso['mes'].value_counts().sort_index(),
        y=['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],
        orientation='h',
        text="",
        name='Atrasado',
    )]
layout1 = go.Layout(
    height=450,
    width=450,
    title='Vuelos nacionales e internacionales mensuales',
    hovermode='closest',
    xaxis=dict(title='Cantidad de vuelos', ticklen=5, zeroline=False, gridwidth=2, domain=[0.1, 1]),
    yaxis=dict(title='Meses', ticklen=5, gridwidth=2),
    showlegend=True
)
fig1 = go.Figure(data=data1, layout=layout1)

data2 = [
   
    go.Pie(labels=df_bar['atraso2'].value_counts().keys(), values=df_bar['atraso2'].value_counts())
]

layout2 = go.Layout(
    height=500,
    width=500,
    title='Cantidad porcentual de vuelos atrasados',
    hovermode='closest',
    xaxis=dict(title='Atraso', ticklen=5, zeroline=False, gridwidth=2, domain=[0.1, 1]),
    yaxis=dict(title='Porcentaje %', ticklen=5, gridwidth=2),
    showlegend=True

)


fig2 = go.Figure(data=data2, layout=layout2)
 
data3 = [
    go.Bar(
        y=df_bar_puntual['opera'].value_counts().keys(),
        x=df_bar_puntual['opera'].value_counts(),
        orientation='h',
        text=df_bar_puntual['opera'].value_counts().keys(),
        name="Puntual"
    ),
    go.Bar(
        y=df_bar_atraso['opera'].value_counts().keys(),
        x=df_bar_atraso['opera'].value_counts(),
        orientation='h',
        text=df_bar_puntual['opera'].value_counts().keys(),
        name="Atraso"
    )]
layout3 = go.Layout(
    height=500,
    width=500,
    title='Cantidad de vuelos por Aerolíneas',
    hovermode='closest',
    xaxis=dict(title='Aerolineas', ticklen=5, zeroline=False, gridwidth=2, domain=[0.1, 1]),
    yaxis=dict(title='', ticklen=5, gridwidth=2),
    showlegend=True
)
fig3 = go.Figure(data=data3, layout=layout3)


layout4 = go.Layout(
    height=500,
    width=350,
    title='',
    hovermode='closest',
    xaxis=dict(title='', ticklen=5, zeroline=False, showgrid=True, domain=[0.2, 1], tickangle = 270),
    yaxis=dict(title='Variables importantes en modelo Latam', ticklen=5,  showgrid=False),
    showlegend=False
)
layout5 = go.Layout(
    height=500,
    width=350,
    title='',
    hovermode='closest',
    xaxis=dict(title='', ticklen=5, zeroline=False, showgrid=True, domain=[0.2, 1], tickangle = 270),
    yaxis=dict(title='Variables importantes en modelo no Latam', ticklen=5,  showgrid=False),
    showlegend=False
)


fig4 = go.Figure(data=go.Scatter(
    x=df_importance1['var'],
    y=df_importance1['importance'],
    mode='markers',
    marker=dict(size=df_importance1['var2'],
                color=[0,  3,  6,  9, 12])
),layout=layout4)

fig5 = go.Figure(data=go.Scatter(
    x=df_importance2['var'],
    y=df_importance2['importance'],
    mode='markers',
    marker=dict(size=df_importance2['var2'],
                color=[0,  3,  6,  9, 12])
),layout=layout5)

def prepare_daily_report(aerolinea,mes,dia):

    current_date = (datetime.today() - timedelta(days=1)).strftime('%m-%d-%Y')

    #df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/' + current_date + '.csv')
    df_bar = pd.read_csv('data_final.csv')
    #df_country = df.groupby(['Country_Region']).sum().reset_index()
    #df_country.replace('US', 'United States', inplace=True)
    df_aero = df_bar[df_bar['opera']== aerolinea]
    df_mes = df_aero[df_aero['mes']== mes]
    df_dia = df_mes[df_mes['dia_nomi']== dia]
    

    #atraso+puntual
    df_dia['atraso_total'] = df_dia['atraso'].replace([0], [1])
    
    df_country = df_dia.groupby(['dest_pais']).sum().reset_index()

    df_country = df_country[df_country['dest_pais']!= 'CL']

    
    #code_df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')
    code_df = pd.read_csv('code.csv')
    df_country['pais']= coco.convert(names=df_country.dest_pais.tolist(), to='name_short', not_found=None)
    df_country_code = df_country.merge(code_df, left_on='pais', right_on='COUNTRY', how='left')
    
    return(df_country_code)

app.layout = html.Div(children=[
    

    html.Div(html.Img(src=app.get_asset_url('white_logo_color_background.jpg'), style={'height':'100%', 'width':'100%'})),
    
    html.Div([
        html.Div([
            html.H3(children=''
                ),

            dcc.Graph(
                id='graph1',
                figure=fig1
            ),
            html.Div(children='''
                .
            '''),
        ], className='six columns'),
         html.Div([
        html.Div(children='''En un viaje siempre hay riesgo de que el vuelo no salga a tiempo o que por el clima u otras posibles situaciones sea cancelado. Si bien las aerolíneas dan compensaciones y explicaciones a los pasajeros, pocas veces expresan con claridad el motivo real del atraso.
        Para ofrecer una solución a este problema es que proponemos AEROPUNTUAL, cuyo objetivo es generar una herramienta de software utilizando técnicas de Data Science que contribuya a las aerolíneas a mejorar la experiencia del consumidor y permitir proactividad a la hora de gestionar la planificación aérea, mediante la detección temprana de retraso en el servicio.
        Estos atrasos se puede deber a distintos factores tanto internos como externos como:
        ''',
         style={'paddingTop':40, "textAlign":'justify',"paddingRight": 60}),
        html.Div([
          html.Ul([
            html.Li(children='''Mantenimiento de último minuto.'''),
            html.Li(children='''Cambios de avión.'''),
            html.Li(children='''Tiempos de abordaje no cuantificables.'''),
            html.Li(children='''Precipitación '''),
            html.Li(children='''Velocidad del Viento '''),
            html.Li(children='''Temperaturas o Clima extremas '''),
          ]),
        ],style={}),

        ], className='six columns'),
    
        

    ], className='row',style={"paddingBottom": 60,"fontSize":14}),
    html.Div([
      html.Div([
            html.H3(children=''
                ),

            dcc.Graph(
                id='graph2',
                figure=fig2
            ),
            html.Div(children='''
            '''),
        ], className='six columns'),
        html.Div([
            
            dcc.Graph(
                id='graph3',
                figure=fig3
            ),
           
        ], className='three columns'),
    ], className='row'),
    html.Div([
        html.Div([
            
            dcc.Graph(
                id='graph4',
                figure=fig4
            ),

        ], className='three columns'),
        html.Div([

            dcc.Graph(
                id='graph5',
                figure=fig5
            ),
           
        ], className='three columns'),
        html.Div([
            html.P(children=''' AEROPUNTUAL entrega dos modelos, siendo uno de ellos específico para el Grupo Latam quien maneja aproximadamente el 60% de los vuelos realizados para el año 2017. 
                Ambos modelos se construyeron utilizando técnicas de Machine Learning avanzadas, para obtener la mejor predicción de vuelos atrasados.''',
                style={ "paddingTop":80, "paddingLeft": "25%", "textAlign":'justify',"padding-right": 60}),
            html.Div([
              html.Ul([
                html.Li(children='''La clasificación de atraso para la Aerolínea Grupo Latam se basa en un modelo de   AdaBoost Classifier, con un 57% predicciones correctas.  '''),
                html.Li(children='''Por otro lado, la predicción de atraso para las demás Aerolíneas se basa en un modelo de tipo CatBoost Classifier, con el que se alcanza un 61% de predicción de atrasos correcta.''')
              ]),
                ],style={  "paddingLeft": "25%","padding-right": 60}),
            html.P(children='''A través de este modelo usted podrá determinar si su vuelo tendrá un atraso.
                A continuación puede realizar la consulta.
            ''', style={ "paddingBottom": 60, "paddingLeft": "25%", "textAlign":'justify',"padding-right": 60})
        ], className='six columns'),
        
    ], className='row',style={"paddingBottom": 60,"fontSize":14, "paddingTop":60}),
    
    html.H1(children='Averigua si tu vuelo podría tener un atraso',style={'textAlign':'center'}),

    
    html.Div([html.Span("Métrica : ", className="six columns",
                                           style={"textAlign": "right", 
                                           "width": "30%"}),
                                 dcc.Dropdown(id="value-selected1", value='atraso',
                                              options=[{'label': "Vuelos atrasados (datos reales 2017) ", 'value': 'atraso'},
                                                       {'label': "Vuelos atrasados (resultados del modelo) ", 'value': 'y_pred'},
                                                       ],
                                              style={"display": "block", "marginLeft": "auto", "marginRight": "auto",
                                                     "width": "80%"},
                                              className="six columns")], className="row"),

    html.Div([html.Span("Tipo : ", className="six columns",
                                           style={"textAlign": "right", 
                                           "width": "30%"}),
                                 dcc.Dropdown(id="value-selected2", value='Internacional',
                                              options=[{'label': "Nacional ", 'value': 'Nacional'},
                                                       {'label': "Internacional ", 'value': 'Internacional'},
                                                       ],
                                              style={"display": "block", "marginLeft": "auto", "marginRight": "auto",
                                                     "width": "80%"},
                                            className="six columns")], className="row"),
    html.Div([html.Span("Aerolínea : ", className="six columns",
                                         style={"textAlign": "right", 
                                         "width": "30%"}),
                               dcc.Dropdown(id="value-selected3", value='Grupo LATAM',
                                            options=[{'label': "Grupo LATAM ", 'value': 'Grupo LATAM'},
                                                     {'label': "Sky Airline ", 'value': 'Sky Airline'},
                                                     {'label': "Aerolineas Argentinas ", 'value': 'Aerolineas Argentinas'},
                                                     {'label': "Copa Air ", 'value': 'Copa Air'},
                                                     {'label': "Latin American Wings ", 'value': 'Latin American Wings'},
                                                     {'label': "Avianca ", 'value': 'Avianca'},
                                                     {'label': "JetSmart SPA ", 'value': 'JetSmart SPA'},
                                                     {'label': "Gol Trans ", 'value': 'Gol Trans'},
                                                     {'label': "American Airlines ", 'value': 'American Airlines'},
                                                     {'label': "Air Canada ", 'value': 'Air Canada'},
                                                     {'label': "Iberia ", 'value': 'Iberia'},
                                                     {'label': "Delta Air ", 'value': 'Delta Air'},
                                                     {'label': "Air France ", 'value': 'Air France'},
                                                     {'label': "Aeromexico ", 'value': 'Aeromexico'},
                                                     {'label': "United Airlines ", 'value': 'United Airlines'},
                                                     {'label': "Oceanair Linhas Aereas ", 'value': 'Oceanair Linhas Aereas'},
                                                     {'label': "Alitalia ", 'value': 'Alitalia'},
                                                     {'label': "K.L.M. ", 'value': 'K.L.M.'},
                                                     {'label': "British Airways ", 'value': 'British Airways'},
                                                     {'label': "Qantas Airways ", 'value': 'Qantas Airways'},
                                                     {'label': "Lacsa ", 'value': 'Lacsa'},
                                                     {'label': "Austral ", 'value': 'Austral'},
                                                     {'label': "Plus Ultra Lineas Aereas ", 'value': 'Plus Ultra Lineas Aereas'}],
                                            style={"display": "block", "marginLeft": "auto", "marginRight": "auto",
                                                   "width": "80%"},
                                            className="six columns")], className="row"),

    html.Div([html.Span("Mes : ", className="six columns",
                                           style={"textAlign": "right", 
                                           "width": "30%"}),
                                 dcc.Dropdown(id="value-selected4", value=1,
                                              options=[{'label': "Enero ", 'value': 1},
                                                       {'label': "Febrero ", 'value': 2},
                                                       {'label': "Marzo ", 'value': 3},
                                                       {'label': "Abril ", 'value': 4},
                                                       {'label': "Mayo ", 'value': 5},
                                                       {'label': "Junio ", 'value': 6},
                                                       {'label': "Julio ", 'value': 7},
                                                       {'label': "Agosto ", 'value': 8},
                                                       {'label': "Septiembre ", 'value': 9},
                                                       {'label': "Octubre ", 'value': 10},
                                                       {'label': "Noviembre ", 'value': 11},
                                                       {'label': "Diciembre ", 'value': 12}],
                                              style={"display": "block", "marginLeft": "auto", "marginRight": "auto",
                                                     "width": "80%"},
                                              className="six columns")], className="row"),

    html.Div([html.Span("Día : ", className="six columns",
                                           style={"textAlign": "right", 
                                           "width": "30%"}),
                                 dcc.Dropdown(id="value-selected5", value='Lu',
                                              options=[{'label': "Lunes ", 'value': 'Lu'},
                                                       {'label': "Martes ", 'value': 'Ma'},
                                                       {'label': "Miércoles ", 'value': 'Mi'},
                                                       {'label': "Jueves ", 'value': 'Ju'},
                                                       {'label': "Viernes ", 'value': 'Vi'},
                                                       {'label': "Sábado ", 'value': 'Sa'},
                                                       {'label': "Domingo ", 'value': 'Do'}
                                                       ],
                                              style={"display": "block", "marginLeft": "auto", "marginRight": "auto",
                                                     "width": "80%"},
                                              className="six columns")], className="row"),


   
   
    html.Div([
     
        
    ], className='three columns',style={'textAlign':'center','paddingLeft':'5%'}),
  
    html.Div([
      html.Div([
        html.Div(html.Img(src=app.get_asset_url('sun_026.jpg'), 
          style={'height':'20%', 'width':'20%'})),
        html.H3(children=[
          dcc.Markdown(''' ''',id='my-temperature',style={"fontSize":14, "paddingLeft":'0%', 'paddingRight':'0%','textAlign':'center'})
        ]),
        html.P('Temperatura promedio')
      ], className='four columns',style={'textAlign':'center','paddingLeft':'5%'}),
      html.Div([
          html.Div(html.Img(src=app.get_asset_url('pngtree-rain-cloud-vector-icon-png-image_1027023.jpg'), 
            style={'height':'20%', 'width':'20%'})),
          html.H3(children=[
                dcc.Markdown(''' ''',id='my-precipitation', style={"fontSize":14, "paddingLeft":'0%', 'paddingRight':'5%','textAlign':'center'})
              ]),
          html.P('Precipitación promedio')

          
      ], className='four columns',style={'textAlign':'center','paddingLeft':'5%'}),
      html.Div([
          html.Div(html.Img(src=app.get_asset_url('el-viento.jpg'), 
            style={'height':'20%', 'width':'20%'})),
          html.H3(children=[
                dcc.Markdown(''' ''',id='my-wind', style={"fontSize":14, "paddingLeft":'0%', 'paddingRight':'5%','textAlign':'center'})
              ]),
          html.P('Velocidad del viento promedio')

          
      ], className='four columns',style={'textAlign':'center','paddingLeft':'5%'}),
    ], className='row',style={'paddingTop':20}),
    
            
    html.H3(children=[
              dcc.Markdown(''' ''',id='no-data', style={"fontSize":18, "paddingLeft":'10%', 'paddingRight':'10%','textAlign':'center'})
            ]),
    html.Div(html.Img(src=app.get_asset_url('leyenda.png'), 
          style={'height':'20%', 'width':'20%', "paddingLeft":'40%', 'paddingRight':'40%'})),
   
     
        
    dcc.Graph(
            id='my-graph'

        ),
    
  
            
        
    html.Div(html.Img(src=app.get_asset_url('equipo2.png'), style={'height':'60%', 'width':'60%', 'paddingLeft':'20%'})),
    

   
])

@app.callback(
    [#dash.dependencies.Output("my-title", "children"),
    dash.dependencies.Output("my-graph", "figure"),
    dash.dependencies.Output("my-temperature", "children"),
    dash.dependencies.Output("my-precipitation", "children"),
    dash.dependencies.Output("my-wind", "children"),
    dash.dependencies.Output("no-data", "children")],
    [dash.dependencies.Input("value-selected1", "value"),
    dash.dependencies.Input("value-selected2", "value"),
    dash.dependencies.Input("value-selected3", "value"),
    dash.dependencies.Input("value-selected4", "value"),
    dash.dependencies.Input("value-selected5", "value")]
)


def update_multioutput(selected1,selected2,selected3,selected4,selected5):
    #dff = prepare_confirmed_data()
    df_bar = pd.read_csv('data_final.csv')
    if selected2 == 'Internacional':
      dff = prepare_daily_report(selected3,selected4,selected5)
      #print(len(dff[selected1]))
      dff['hover_text'] = dff["pais"] + " Probabilidad de atraso : " + (round(dff[selected1]/dff['atraso_total'],3)).apply(str)
      if dff[selected1].sum() == 0:
        data =''' No hay información disponible para esta búsqueda '''
      else:
        data ='''Busca en el mapa tu destino y averigua los resultados de probabilidad de atraso para tu vuelo.'''
      trace = go.Choropleth(locations=dff['CODE'],
                            z=dff[selected1]/dff['atraso_total'],
                            zmin=0,
                            zmax=1,
                            text=dff['hover_text'],
                            hoverinfo="text",
                            marker_line_color='white',
                            autocolorscale=False,
                            reversescale=True,
                            colorscale="Viridis",
                            marker={'line': {'color': 'rgb(180,180,180)','width': 0.5}},
                            colorbar={"thickness": 10,"len": 0.3,"x": 0.9,"y": 0.7,
                                      'title': {"text": 'atrasos', "side": "bottom"},
                                      'tickvals': [0, 1],
                                      'ticktext': ['0','1']}
                            )   
      layout = go.Layout(height=800,
              geo={'showframe': False,'showcoastlines': True,'projection': {'type': "miller"}})
      
      
      df_mes = df_bar[df_bar['mes']== selected4]
      df_dia = df_mes[df_mes['dia_nomi']== selected5]
      
      temperature = str(round(df_dia.orig_tas.mean(),2))+' ºC'
      precipitation = str(round(df_dia.ori_pr.mean(),2))+' mm'
      wind = str(round(df_dia.vel_viento_mod_orig.mean(),2))+' m/s ' +(df_mes.wind_dir.value_counts().keys().tolist()[0])

    elif selected2 == 'Nacional':

      df_aero = df_chile[df_chile['opera']== selected3]
      df_mes = df_aero[df_aero['mes']== selected4]
      df_dia = df_mes[df_mes['dia_nomi']== selected5]

      df_dia['atraso_total'] = df_dia[selected1].replace([0], [1])
      df_bar_atraso_chile = df_dia.groupby(['dest_ciudad']).sum().reset_index()
      list_count = []
      list_count_total =[]
      for n in range(len(df_bar_atraso_chile[selected1])):
        for m in df_dia['dest_ciudad']:
          if m == df_bar_atraso_chile['dest_ciudad'][n]:
            list_count.append(df_bar_atraso_chile[selected1][n])
            list_count_total.append(df_bar_atraso_chile['atraso_total'][n])

      df_dia['atraso5'] = list_count
      df_dia['atraso5_total'] = list_count_total
      df_dia['text'] =  df_dia['dest_ciudad'] + ', '  + '' + ' Probabilidad de atraso: ' + (round(df_dia['atraso5']/df_dia['atraso5_total'],3)).astype(str).astype(str)
      if df_dia[selected1].sum() == 0:
        data =''' No hay información disponible para esta búsqueda '''
      else:
        data ='''Busca en el mapa tu destino y averigua los resultados de probabilidad de atraso para tu vuelo.'''
      trace = go.Scattergeo(
              lon = df_dia['dest_lon'],
              lat = df_dia['dest_lat'],
              text = df_dia['text'],
              mode = 'markers',
              marker_color = round(df_dia['atraso5']/df_dia['atraso5_total'],3),
              
              marker={'colorscale': 'Viridis','reversescale': True,'line': {'color': 'rgb(180,180,180)'},'cmax':1,'cmin':0},
              showlegend=False,
              marker_size=15,
              )

      layout= go.Layout(
              
              geo_scope='south america'
          )

      df_dia = df_bar[df_bar['dia_nomi']== selected5]
      df_mes = df_dia[df_dia['mes']== selected4]
      temperature = str(round(df_mes.orig_tas.mean(),2))+' ºC'
      precipitation = str(round(df_mes.ori_pr.mean(),2))+' mm'
      wind = str(round(df_mes.vel_viento_mod_orig.mean(),2))+' m/s ' +(df_mes.wind_dir.value_counts().keys().tolist()[0])


    figure ={"data": [trace],
            "layout": layout}

    return  figure, temperature, precipitation, wind, data




if __name__ == '__main__':
    app.run_server(debug=True)

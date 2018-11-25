import dash
import dash_core_components as dcc 
import dash_html_components as html 
import pandas as pd 
import plotly.graph_objs as go
from dash.dependencies import Input,Output
from categoryplot import getPlot, catgory
import numpy as np
from plotly import tools

app = dash.Dash()
app.title = 'Purwadhika Dash Plotly'
mydata = pd.read_csv('data')
dataT = pd.read_csv('jointdata')

data = {
    'After_Preparation' : dataT,
    'Before_Preparation' : mydata
}

estiFunc = {
    'count': len,
    'sum': sum,
    'mean': np.mean,
    'std': np.std
}

color_set = {
    'Gender': ['#ff3fd8','#4290ff'],
    'Education': ['#32fc7c','#ed2828','#ddff00','#f2e200','#0059a3'],
    'NumberChildrenAtHome': ['#0059a3','#f2e200','#ddff00','#3de800','#00c9ed'],
    'Occupation': ['#ff8800','#ddff00','#3de800','#00c9ed','#ff3fd8'],
    'CountryRegionName':['#32fc7c','#ed2828','#ddff00','#0059a3','#00c9ed','#ff3fd8'],
    'Catage' : ['#ff8800','#ddff00','#3de800','#00c9ed','#ff3fd8','#3de800','#00c9ed']
}

app.layout = html.Div(children=[
    dcc.Tabs(id='tabs', value='tab1', className='h1firstTab',
    style={
         'fontFamily': 'system-ui'
    },
    content_style={
        'fontFamily': 'Arial',
        'borderLeft': '1px solid #d6d6d6',
        'borderRight': '1px solid #d6d6d6',
        'borderBottom': '1px solid #d6d6d6',
        'padding': '44px'
    },
    children=[
        dcc.Tab(label='Data Set Overview', value='tab1', children=[
            html.Div([
                html.Table([
                    html.Tr([
                        html.Td(html.P('Table : ')),
                        html.Td([
                            dcc.Dropdown(
                                id='dd-table',
                                options=[{'label':'Dataset Before', 'value':'Before_Preparation'},
                                        {'label':'Dataset After', 'value':'After_Preparation'}],
                                value='Before_Preparation'
                            )]
                        )
                    ])
                ],style={ 'width': '300px', 'paddingBottom': '20px' }),
                    html.Div(id='tampil_table')
            ])
        ]),
        dcc.Tab(label='Categorical Fiture with target Overview', value='tab2', children=[
            html.Div([
                html.H1('View Data Pie Plot',className='h1firstTab'),
                html.Table([
                    html.Tr([
                        html.Td(html.P(['Hue : ',
                                dcc.Dropdown(
                                    id='ddl-fiture-plot',
                                    options=[{'label': 'Gender', 'value': 'Gender'},
                                            {'label': 'Education', 'value': 'Education'},
                                            {'label': 'Number Children At Home', 'value': 'NumberChildrenAtHome'},
                                            {'label': 'Occupation', 'value': 'Occupation'},
                                            {'label': 'Country Region Name', 'value': 'CountryRegionName'},
                                            {'label': 'Age', 'value': 'catAge'}],
                                    value='Gender'
                                )
                            ]),style={'width': '900px'}),
                        html.Td(html.P(['Column : ',
                                dcc.Dropdown(
                                    id='ddl-target-plot',
                                    options=[{'label': 'Yearly Income', 'value': 'YearlyIncome'},
                                            {'label': 'Average Month Spend', 'value': 'AveMonthSpend'}],
                                    value='YearlyIncome'
                                )
                            ]),style={'width': '400px'})
                    ]),
                ],style={ 'width': '1200px', 'paddingBottom': '20px'}),
            html.Table(id='tr_bar', children=[])
            ])
        ]),
            dcc.Tab(label='Plot fiture', value='tab-3', children=[
                html.Div([
                    html.H1('Categorical Plot Tips Data Set',className='h1firstTab'),
                    html.Table([
                        html.Tr([
                            html.Td([
                                html.P('Jenis : '),
                                dcc.Dropdown(
                                    id='ddl-jenis-plot-category',
                                    options=[{'label': 'Bar', 'value': 'bar'},
                                            {'label': 'Violin', 'value': 'violin'},
                                            {'label': 'Box', 'value': 'box'}],
                                    value='bar'
                                )
                            ]),
                            html.Td([
                                html.P('X Axis : '),
                                dcc.Dropdown(
                                    id='ddl-x-plot-category',
                                    options=[{'label': 'Gender', 'value': 'Gender'},
                                            {'label': 'Education', 'value': 'Education'},
                                            {'label': 'Number Children At Home', 'value': 'NumberChildrenAtHome'},
                                            {'label': 'Occupation', 'value': 'Occupation'},
                                            {'label': 'Country Region Name', 'value': 'CountryRegionName'},
                                            {'label': 'Age', 'value': 'catAge'}],
                                    value='Gender'
                                )
                            ])
                        ])
                    ], style={ 'width' : '700px', 'margin': '0 auto'}),
                    dcc.Graph(
                        id='categoricalPlot',
                        figure={
                            'data': []
                        }
                    )
                ])
            ])
    ])
], 
style={'maxWidth' : '1300px',
'margin' : '0 auto'  })

#callback untuk table 
@app.callback(
    Output('tampil_table','children'),
    [Input('dd-table','value')]
)
def tampil_table(table):
    dataset = data[table]
    return[
        html.H1(children = table,className='h1firstTab'),
        html.H4('Total Row :'+str(len(dataset))),
        html.H4("Total columns : "+str(len(dataset.columns))),
        dcc.Graph(
                id='table_go',
                figure={
                        'data':[ go.Table(
                                header=dict(
                                    values=['<b>'+col.capitalize()+'<b>' for col in dataset.columns],
                                    fill = dict(color='#C2D4FF'),
                                    font = dict(size=11),
                                    height= 30,
                                    align = ['center']),
                                cells=dict(
                                    values=[dataset[col] for col in dataset.columns],
                                    fill= dict(color='#F5F8FF'),
                                    font=dict(size=11),
                                    height= 25,
                                    align = ['right']*5)    
                        )],
                        'layout':go.Layout(height=500, margin={'l': 40, 'b': 40, 't': 10, 'r': 10})
                }
        )
    ]

@app.callback(
    Output('tr_bar', 'children'),
    [Input('ddl-fiture-plot', 'value'),
    Input('ddl-target-plot','value')]
)

def update_graph(fiture,target):
    xtable = mydata.groupby(fiture).mean()[target].sort_values(ascending=False).reset_index()
    return[
        html.Td([
            dcc.Graph(
                id='table_go',
                figure={
                    'data':[
                        go.Bar(
                        x=xtable[fiture],
                        y=xtable[target],
                        text=xtable[target],
                        name='try',
                        marker=dict(color='blue'),
                        legendgroup = 'target'
                    )],
                    'layout': go.Layout(
                        xaxis={'title': fiture.capitalize()}, yaxis={'title': target.capitalize()},
                        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                        width=700,
                        height=500,
                        legend={'x': 0, 'y': 1.2}, hovermode='closest',
                        boxmode='group',violinmode='group',
                        #plot_bgcolor= 'black', paper_bgcolor= 'black'
                    )
                }
            )   
        ],colSpan='2',style={'width': '900px'}),
        html.Td([
                dcc.Graph(
                id='table_go2',
                figure={
                        'data':[ go.Table(
                                header=dict(
                                    values=['<b>'+col.capitalize()+'<b>' for col in xtable.columns],
                                    fill = dict(color='#C2D4FF'),
                                    font = dict(size=11),
                                    height= 30,
                                    align = ['center']),
                                cells=dict(
                                    values=[xtable[col] for col in xtable.columns],
                                    fill= dict(color='#F5F8FF'),
                                    font=dict(size=11),
                                    height= 25,
                                    align = ['right']*5)    
                        )],
                        'layout':go.Layout(width = 300,height=300, margin={'l': 10,'b': 40, 't': 10, 'r': 10})
                }
        )
        ],style={'position': 'absolute', 'width': '300px'})
    ]

@app.callback(
    Output('categoricalPlot', 'figure'),
    [Input('ddl-jenis-plot-category', 'value'),
    Input('ddl-x-plot-category', 'value')])
def update_category_graph(ddljeniscategory, ddlxcategory):
    return {
            'data': getPlot(ddljeniscategory,ddlxcategory),
            'layout': go.Layout(
                xaxis={'title': ddlxcategory.capitalize()}, yaxis={'title': 'US$'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1.2}, hovermode='closest',
                boxmode='group',violinmode='group'
                # plot_bgcolor= 'black', paper_bgcolor= 'black',
            )
    }




if __name__ == '__main__':
    # run server on port 1997
    # debug=True for auto restart if code edited
    app.run_server(debug=True, port=1907) 


import dash
import dash_core_components as dcc 
import dash_html_components as html 
import pandas as pd 
import plotly.graph_objs as go
import plotly.plotly as py
from dash.dependencies import Input,Output
from categoryplot import getPlot, catgory
import numpy as np
from plotly import tools

app = dash.Dash()
app.title = 'Purwadhika Dash Plotly'
mydata = pd.read_csv('data')
dataT = pd.read_csv('jointdata')

data = {
    'After_Preperesion' : dataT,
    'Before_Preperesion' : mydata
}

# estiFunc = {
#     'count': len,
#     'sum': sum,
#     'mean': np.mean,
#     'std': np.std
# }

color_set = {
    'Gender': ['#ff3fd8','#4290ff'],
    'Education': ['#32fc7c','#ed2828','#ddff00','#f2e200','#0059a3'],
    'NumberChildrenAtHome': ['#0059a3','#f2e200','#ddff00','#3de800','#00c9ed'],
    'Occupation': ['#ff8800','#ddff00','#3de800','#00c9ed','#ff3fd8'],
    'CountryRegionName':['#32fc7c','#ed2828','#ddff00','#0059a3','#00c9ed','#ff3fd8'],
    'Catage' : ['#ff8800','#ddff00','#3de800','#00c9ed','#ff3fd8','#3de800','#00c9ed']
}

app.layout = html.Div(children=[
    dcc.Tabs(id='tabs', value='tab2', className='h1firstTab',
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
        dcc.Tab(label='Categorical Fiture Overview', value='tab2', children=[
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
                                            {'label': 'City', 'value': 'City'}],
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
        ])
    ])
])

@app.callback(
    Output('tr_bar', 'children'),
    [Input('ddl-fiture-plot', 'value'),
    Input('ddl-target-plot','value')]
)

def update_graph(fiture,target):
    xtable = mydata.groupby(fiture).mean()[target].reset_index()
    return[
        html.Td([
            dcc.Graph(
                id='table_go',
                figure={
                    'data':[
                        go.Bar(
                        x=mydata[fiture],
                        y=mydata[target],
                        text=mydata[target],
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
                        'layout':go.Layout(width=300, height=300, margin={'l': 40, 'b': 40, 't': 10, 'r': 10})
                }
        )
        ],style={'position': 'absolute', 'width': '300px'})
    ]


if __name__ == '__main__':
    # run server on port 1997
    # debug=True for auto restart if code edited
    app.run_server(debug=True, port=2907)
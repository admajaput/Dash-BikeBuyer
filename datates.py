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
    'After_Preperesion' : dataT,
    'Before_Preperesion' : mydata
}

# color_set = {
#     'Gender': ['#ff3fd8','#4290ff'],
#     'Education': ['#32fc7c','#ed2828','#ddff00','#f2e200','#0059a3'],
#     'NumberChildrenAtHome': ['#0059a3','#f2e200','#ddff00','#3de800','#00c9ed'],
#     'Occupation': ['#ff8800','#ddff00','#3de800','#00c9ed','#ff3fd8'],
#     'City':['#32fc7c','#ed2828','#ddff00','#0059a3'],
#     'Catage' : ['#ff8800','#ddff00','#3de800','#00c9ed','#ff3fd8',]
    
# }

app.layout = html.Div(children=[
    dcc.Tab(id='tabs', value='tab3', className='h1firstTab',
    tyle={
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
        dcc.Tabs(label='Categori X Continues Value', value='tab3', children=[
            html.Div([
                html.H1('View Data Explanation', className='h1firstTab'),
                html.Table([
                    html.Tr([
                        html.Td(html.P(['Hue : ',
                                dcc.Dropdown(
                                    id='ddl-fiture-plot',
                                    options=[{'label': 'Gender', 'value': 'Gender'},
                                            {'label': 'Education', 'value': 'Education'},
                                            {'label': 'NumberChildrenAtHome', 'value': 'NumberChildrenAtHome'},
                                            {'label': 'Occupation', 'value': 'Occupation'}],
                                    value='Gender'
                                )
                            ]),style={'border-style':'solid','width': '600px'}),
                        html.Td(html.P(['Column : ',
                                dcc.Dropdown(
                                    id='ddl-target-plot',
                                    options=[{'label': 'Yearly Income', 'value': 'YearlyIncome'},
                                            {'label': 'Average Month Spend', 'value': 'AveMonthSpend'}],
                                    value='YearlyIncome'
                                )
                            ]),style={'border-style':'solid','width': '400px'})
                    ]),
                ],style={ 'width': '100px', 'paddingBottom': '20px'}),
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

def bar_catx(x,y):
    return[
        html.Td([
            dcc.Graph(
                id='categoricalPlot',
                figure={
                    'data': catgory(x,y),
                    'layout': go.Layout(
                            xaxis={'title': x.capitalize()}, yaxis={'title': y.capitalize()},
                            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                            legend={'x': 0, 'y': 1.2}, hovermode='closest',
                            boxmode='group',violinmode='group'
                            # plot_bgcolor= 'black', paper_bgcolor= 'black',
                    )
                })
            ],style={'border-style':'solid','width': '600px'}),
        html.Td([

        ],style={'border-style':'solid','width': '400px'}),
    ]
if __name__ == '__main__':
    # run server on port 1997
    # debug=True for auto restart if code edited
    app.run_server(debug=True, port=1607) 
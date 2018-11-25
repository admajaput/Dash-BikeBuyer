import plotly.graph_objs as go
from data import dataT, mydata

listGoFunc = {
    'bar': go.Bar,
    'violin': go.violin,
    'box': go.Box
}


def getPlot(jenis, xCategory):
    return [
        listGoFunc[jenis](
            x=mydata[xCategory],
            y=mydata['AveMonthSpend'],
            text=mydata['AveMonthSpend'],
            opacity=0.7,
            name='Ave Month Spend',
            marker=dict(color='blue'),
            legendgroup = 'total_bill'
        )
    ]

def catgory(fiture, target):
    return [
        go.Bar(
            x=dataT[fiture],
            y=dataT[target],
            text=dataT['catAge'],
            opacity=0.7,
            name='try',
            marker=dict(color='blue'),
            legendgroup = 'target'
        )
    ]
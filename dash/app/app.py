import os
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from time import sleep 
print('Waiting for the python server...')
sleep(200)
print('plot server Starting...')

debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True

app = Dash(__name__)

server = app.server

data = pd.read_csv('./input/out.csv') 

df_time = pd.read_csv('./input/df_time.csv')
df_month = pd.read_csv('./input/df_month.csv')
df_Dayofweek = pd.read_csv('./input/df_Dayofweek.csv')
df_year_mean = pd.read_csv('./input/df_year_mean.csv')
df_year_sum = pd.read_csv('./input/df_year_sum.csv')




graph = px.line(data, x="date", y="price", color='country')
scatter_plot = px.scatter(data[['demand_supply_gap','price','country']],
                 x='demand_supply_gap',y = 'price',
    color="country")


graph_df_time = px.line(df_time, x="Time", y="price", color='country')
graph_df_month = px.line(df_month, x="Month", y="price", color='country')
graph_df_Dayofweek = px.line(df_Dayofweek, x="Dayofweek", y="price", color='country')
graph_df_year_mean = px.line(df_year_mean, x="Year", y="price", color='country')
graph_df_year_sum = px.line(df_year_sum, x="Year", y="price", color='country')






aggs = ["count","sum","avg","median","mode","rms","stddev","min","max","first","last"]

agg = []
agg_func = []
for i in range(0, len(aggs)):
    agg = dict(
        args=['transforms[0].aggregations[0].func', aggs[i]],
        label=aggs[i],
        method='restyle'
    )
    agg_func.append(agg)

data_map = [dict(
  type = 'choropleth',
  locationmode = 'country names',
  locations = data['country'],
  z = data['price'],
  autocolorscale = False,
  colorscale = 'Portland',
  reversescale = True,
  transforms = [dict(
    type = 'aggregate',
    groups = data['country'],
    aggregations = [dict(
        target = 'z', func = 'sum', enabled = True)
    ]
  )]
)]

layout_map = dict(
  title = '<b>Plotly Aggregations</b><br>use dropdown to change aggregation',
  xaxis = dict(title = 'Subject'),
  yaxis = dict(title = 'Score', range = [0,22]),
  height = 600,
  width = 900,
  updatemenus = [dict(
        x = 0.85,
        y = 1.15,
        xref = 'paper',
        yref = 'paper',
        yanchor = 'top',
        active = 1,
        showactive = False,
        buttons = agg_func
  )]
)

fig_dict = dict(data=data_map, layout=layout_map)


app.layout = html.Div(
    children=[
        html.H1(
            children="Some analytical plots"
        ),
        html.Div(children="""Price Time graph"""),
        dcc.Graph(id="example-graph", figure=graph),

        html.Div(children="""scatterplot between price and demand supply difference """),
        dcc.Graph(id="scatter-plot", figure=scatter_plot),

        html.Div(children="""Price on country basis"""),
        dcc.Graph(id="map-plot", figure=fig_dict),

        html.Div(children="""Price day Time graph"""),
        dcc.Graph(id="graph_df_time", figure=graph_df_time),

        html.Div(children="""Price by month graph"""),
        dcc.Graph(id="graph_df_month", figure=graph_df_month),

        html.Div(children="""Price Time graph"""),
        dcc.Graph(id="graph_df_Dayofweek", figure=graph_df_Dayofweek),

        html.Div(children="""Mean Price by year graph"""),
        dcc.Graph(id="graph_df_year_mean", figure=graph_df_year_mean),

        html.Div(children="""total Price by year graph"""),
        dcc.Graph(id="graph_df_year_sum", figure=graph_df_year_sum),
    ]
)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8050", debug=debug)

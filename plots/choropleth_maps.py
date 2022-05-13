import json
import plotly.express as px
from utils.config import colors, font

from utils.decorator import style_plot


@style_plot
def plot_consumption_map(df):
    with open('data/countries-simplified.json') as response:
        countries = json.load(response)

    range_color = (0, df.consumption.quantile(0.99))

    map_args = dict(
        geojson=countries,
        featureidkey='properties.ISO_A3',
        locations="Code",
        color="consumption",  # lifeExp is a column of gapminder
        hover_name="country",  # column to add to hover information
        animation_frame='Year',
        mapbox_style="carto-positron",
        color_continuous_scale='YlOrRd',
        range_color=range_color,
        title='Fish consumption (kg / capita) from 1961 to 2017',
        center={'lat': 12, 'lon': 5}
    )

    fig = px.choropleth_mapbox(df, zoom=0.5, **map_args)
    fig.update_layout(width=800,
                      height=600,
                      margin=dict(
                          l=60,
                          r=0,
                          b=60,
                          t=100,
                          pad=4,
                          autoexpand=True
                      ),
                      coloraxis=dict(
                          colorbar=dict(
                              title=dict(
                                  text='Consumption<br>(kg/capita)',
                                  font=dict(
                                      size=17
                                  )
                              )
                          )
                      ),
                      updatemenus=[
                          {
                              'buttons': [
                                  {
                                      "args": [None, {
                                          "frame": {
                                              "duration": 100,
                                              "redraw": True
                                          },
                                          "fromcurrent": True,
                                          "transition": {
                                              "duration": 200,
                                              "easing": "quadratic-in-out"
                                          }
                                      }],
                                      "label": "Play",
                                      "method": "animate"
                                  },
                                  {
                                      "args": [[None], {
                                          "frame": {
                                              "duration": 0,
                                              "redraw": True
                                          },
                                          "mode": "immediate",
                                          "transition": {"duration": 0}
                                      }],
                                      "label": "Pause",
                                      "method": "animate"
                                  }
                              ],
                              'xanchor': 'left',
                              'yanchor': 'top',
                              'x': 0,
                              'y': 0.01,
                              'pad': {
                                  'r': 0,
                                  't': 10,
                              }
                          }
                      ],
                      sliders=[
                          {
                              "active": 0,
                              "yanchor": "top",
                              "xanchor": "left",
                              "currentvalue": {
                                  "font": {"size": 25},
                                  "prefix": "Year: ",
                                  "visible": True,
                                  "xanchor": "right",
                                  'offset': 20
                              },
                              "transition": {"duration": 200, "easing": "cubic-in-out"},
                              "pad": {"b": 10, "t": 50},
                              "len": 0.9,
                              "x": 0.1,
                              "y": 0,
                          }
                      ])
    return fig


@style_plot
def plot_industry_map(df, title, quantile=0.975, **kwargs):
    """ Plot Import Export Supply Production """
    with open('data/countries-simplified.json') as response:
        countries = json.load(response)

    type = title.split(' ')[0]
    df = df.rename({'value_pr_capita_2017': type}, axis=1)
    range_color = (0, df[type].quantile(quantile))

    map_args = dict(
        geojson=countries,
        featureidkey='properties.ISO_A3',
        locations='Country Code',
        color=type,
        hover_name='Country',
        mapbox_style="carto-positron",
        color_continuous_scale='YlOrRd',
        range_color=range_color,
        title=title,
    )

    fig = px.choropleth_mapbox(df,
                               zoom=0.5,
                               **map_args,
                               **kwargs
                               )

    fig.update_layout(width=800,
                      height=600,
                      coloraxis={
                          'colorbar': {
                              'title': type + ' kg / capita'
                          }
                      })
    return fig

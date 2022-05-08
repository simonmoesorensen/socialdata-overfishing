import json
import plotly.express as px
from utils.config import colors, font

from web.utils.decorator import style_plot


@style_plot
def plot_consumption_map(df):
    with open('../data/countries-simplified.json') as response:
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
        title='Fish consumption (kg / capita / yr) from 1961 to 2017',
    )

    fig = px.choropleth_mapbox(df, zoom=0.5, **map_args)
    fig.update_layout(width=1000,
                      height=700,
                      font_color=colors['text'],
                      font_family=font,
                      font_size=20,
                      coloraxis={
                          'colorbar': {
                              'title': 'Consumption'
                          }
                      },
                      updatemenus=[
                          {
                              'buttons': [
                                  {
                                      "args": [None, {
                                          "frame": {
                                              "duration": 500,
                                              "redraw": True
                                          },
                                          "fromcurrent": True,
                                          "transition": {
                                              "duration": 300,
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
                              ]
                          }
                      ])
    return fig


@style_plot
def plot_industry_map(df, title, quantile=0.975, **kwargs):
    """ Plot Import Export Supply Production """
    with open('../data/countries-simplified.json') as response:
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

    fig.update_layout(width=1000,
                      height=700,
                      font_color=colors['text'],
                      font_family=font,
                      font_size=20,
                      coloraxis={
                          'colorbar': {
                              'title': type
                          }
                      })
    return fig

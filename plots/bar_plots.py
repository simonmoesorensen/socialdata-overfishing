import pandas as pd

from utils.decorator import style_plot
import plotly.express as px


@style_plot
def plot_protein(protein):
    protein_sum = protein.sum(axis=1)

    protein_cds = {'countries': list(protein.index.values)}
    for food in list(protein.columns):
        protein_cds[food] = list((protein[food].values / protein_sum) * 100)

    df_plot = pd.DataFrame.from_dict(protein_cds)
    df_plot = pd.melt(df_plot, ['countries'], df_plot.columns[1:],
                      var_name='Protein source',
                      value_name='Protein amount')
    df_plot = df_plot.sort_values('Protein source', ascending=False)

    fig = px.bar(df_plot,
                 x='Protein amount',
                 y='countries',
                 color='Protein source',
                 orientation='h')

    fig.update_layout(
        title='Distribution of protein sources<br><sup>China vs Norway</sup>',
        xaxis=dict(
            title='Protein distribution (%)',
            showgrid=True
        ),
        yaxis=dict(
            title='Country'
        ),
        width=1200
    )

    return fig


@style_plot
def plot_protein_ghg(df):
    df = df.sort_values('Protein source', ascending=False)

    fig = px.bar(df,
                 x='Protein source',
                 y='Emissions',
                 color='Protein source',
                 )

    fig.update_layout(
        title='Protein source GHG emissions per 100g protein from 2017',
        xaxis=dict(
            title='Protein source'
        ),
        yaxis=dict(
            title='GHG emissions (kgCO₂eq) <br>pr 100g protein',
            showgrid=True
        )
    )

    return fig


@style_plot
def plot_aquaculture_emissions(df):
    fig = px.bar(df,
                 x='Amount',
                 y='Entity',
                 color='Greenhouse Gas',
                 orientation='h',
                 )

    fig.update_layout(
        title='Emissions from aquaculture farming different species',
        xaxis=dict(
            title='Amount (kg / tonne edible weight)'
        ),
        yaxis=dict(
            title='Farmed species'
        ),
        width=800,
    )

    return fig

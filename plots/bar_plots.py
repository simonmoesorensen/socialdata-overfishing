import pandas as pd

from utils.decorator import style_plot
import plotly.express as px


@style_plot
def plot_protein(protein):
    protein_sum = protein.sum(axis=1)

    protein_cds = {}
    protein_cds['countries'] = list(protein.index.values)
    for food in list(protein.columns):
        protein_cds[food] = list((protein[food].values / protein_sum) * 100)

    df_plot = pd.DataFrame.from_dict(protein_cds)
    df_plot = pd.melt(df_plot, ['countries'], df_plot.columns[1:],
                      var_name='Protein source',
                      value_name='Protein amount')

    fig = px.bar(df_plot,
                 x='Protein amount',
                 y='countries',
                 color='Protein source',
                 orientation='h')

    fig.update_layout(
        title='Distribution of protein sources<br><sup>China vs Norway</sup>',
        xaxis=dict(
            title='Protein amount (%)',
            showgrid=True
        ),
        yaxis=dict(
            title='Country'
        ),
        width=1200
    )

    return fig

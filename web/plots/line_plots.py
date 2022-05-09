import pandas as pd
import plotly.graph_objects as go

from utils.decorator import style_plot
import plotly.express as px
from sklearn.linear_model import LinearRegression


def plot_trend(df_cons, df_sust):
    fig_cons = plot_avg_global_consumption(df_cons)
    fig_sust = plot_sustainability(df_sust)


@style_plot
def plot_avg_global_consumption(df):
    df_agg = df.groupby(["Year"]).mean().reset_index()

    lr = LinearRegression()
    lr.fit(df_agg['Year'].values.reshape(-1, 1), df_agg['consumption'])

    df_preds = pd.DataFrame(df_agg['Year'].copy())

    df_preds['consumption'] = lr.predict(df_agg['Year'].values.reshape(-1, 1))

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df_preds['Year'], y=df_preds['consumption'],
                   name='Trend')
    )
    fig.add_trace(
        go.Scatter(x=df_agg['Year'], y=df_agg['consumption'],
                   name='Consumption')
    )

    equation = f"Consumption = {lr.coef_[0]:.2f} * Year - {abs(lr.intercept_):.2f}"

    fig.add_annotation(
        x=1994,
        y=df_preds.query('Year == 1994')['consumption'].iloc[0],
        text=equation,
        font=dict(
            size=13
        ),
        ax=-100,
        ay=-70,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        borderwidth=2,
        bordercolor="#c7c7c7",
        borderpad=4,
        arrowcolor='#c7c7c7'
    )

    fig.update_layout(
        title='Average global fish-seafood consumption from 1967 to 2017',
        xaxis=dict(
            title='Year',
            showgrid=False
        ),
        yaxis=dict(
            title='Fish-seafood (kg / capita)',
            showgrid=True),
        width=800,
        height=600,
        font_size=20,
        margin=dict(
            t=100
        )
    )

    return fig


@style_plot
def plot_sustainability(df):
    df_world = df[df["Entity"] == "World"]

    df_plot = pd.melt(df_world, ['Entity', 'Year'], ['sustainable', 'overexploited'], var_name='Type', value_name='Share')

    fig = go.Figure()

    x = df_plot.query('Type == "sustainable"')['Year']
    y = df_plot.query('Type == "sustainable"')['Share']

    fig.add_trace(go.Scatter(x=x, y=y,
                             fill='tozeroy',
                             stackgroup='one',
                             name='Sustainable'))

    x = df_plot.query('Type == "overexploited"')['Year']
    y = df_plot.query('Type == "overexploited"')['Share']

    fig.add_trace(go.Scatter(x=x, y=y,
                             fill='tonexty',
                             stackgroup='one',
                             name='Overexploited'))

    fig.update_layout(
        width=800,
        height=600,
        title=dict(
            text='Percentage of overexploited fishing vs sustainable fishing'
        ),
        xaxis=dict(
            title='Year'
        ),
        yaxis=dict(
            title='Share (%)'
        ),
        margin=dict(
            t=100
        ),
        font_size=20,
    )

    return fig

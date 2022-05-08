from dash import Dash, dcc, html, Output, Input, callback_context
import sd_material_ui as sd

from web.plots.data import get_consumption, group_by_elements, get_population, get_industry_data
from web.plots.choropleth_maps import plot_consumption_map, plot_industry_map

app = Dash(__name__)

year = '2017'

# Data
df_consumption = get_consumption()

df_population = get_population()
df_industry = get_industry_data()

industry_dict = {
    'production': group_by_elements(df_industry, df_population, ['Production'], year),
    'import': group_by_elements(df_industry, df_population, ['Import Quantity'], year),
    'supply': group_by_elements(df_industry, df_population, ['Domestic supply quantity'], year),
    'export': group_by_elements(df_industry, df_population, ['Export Quantity'], year)
}

# Callbacks
@app.callback(
    Output('fish-industry-map', 'figure'),
    Input('btn-production', 'n_clicks'),
    Input('btn-import', 'n_clicks'),
    Input('btn-export', 'n_clicks'),
    Input('btn-supply', 'n_clicks'),
)
def animate_fish_industry_maps(btn1, btn2, btn3, btn4):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]

    if 'btn-import' in changed_id:
        # Default to production
        plot = plot_industry_map(
            industry_dict['import'].reset_index(),
            title="Import in kg / capita in year 2017"
        )
    elif 'btn-export' in changed_id:
        # Default to production
        plot = plot_industry_map(
            industry_dict['export'].reset_index(),
            title="Export in kg / capita in year 2017"
        )
    elif 'btn-supply' in changed_id:
        # Default to production
        plot = plot_industry_map(
            industry_dict['supply'].reset_index(),
            title="Supply in kg / capita in year 2017"
        )
    else:
        # Default to production
        plot = plot_industry_map(
            industry_dict['production'].reset_index(),
            title="Production in kg / capita in year 2017"
        )
    return plot


app.layout = html.Div(children=[
    html.Div([
        html.H1(
            children='Sustainability in fishing habits',
            className='title fade-left'
        ),
        html.H2(
            children='A story on the best and worst fisheries of the world',
            className='text-subtitle fade-left'
        )
    ]),

    html.Div(className='two-column', style={'marginTop': '5rem'}, children=[
        dcc.Loading(dcc.Graph(
            id='fish-consumption-map',
            className='fade-left',
            figure=plot_consumption_map(df_consumption)
        )),
        dcc.Markdown(className="text-box fade-right", children="""
        ## Some nice text
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
        Aliquam elementum velit a vestibulum feugiat. Aliquam ut justo risus. 
        Morbi tincidunt nisl sem, a dapibus massa sollicitudin id. Sed quis arcu nunc. 
        Nunc accumsan odio leo, in consequat purus cursus sit amet. 
        Quisque feugiat sodales neque sed feugiat. Quisque eros metus, 
        imperdiet vitae accumsan quis, varius ac ligula. Praesent iaculis ornare vestibulum.
         Suspendisse sit amet sodales ante, vitae rutrum elit. 
         Aenean porttitor facilisis pretium. Aliquam sit amet augue justo.
        """)
    ]),

    html.Div(className='two-column', style={'marginTop': '5rem'}, children=[
        html.Div(className='two-row', children=[
            dcc.Markdown(className="text-box", style={'textAlign':'justify'}, children="""
                ## Some nice text
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                Aliquam elementum velit a vestibulum feugiat. Aliquam ut justo risus. 
                Morbi tincidunt nisl sem, a dapibus massa sollicitudin id. Sed quis arcu nunc. 
                Nunc accumsan odio leo, in consequat purus cursus sit amet. 
                Quisque feugiat sodales neque sed feugiat. Quisque eros metus, 
                imperdiet vitae accumsan quis, varius ac ligula. Praesent iaculis ornare vestibulum.
                 Suspendisse sit amet sodales ante, vitae rutrum elit. 
                 Aenean porttitor facilisis pretium. Aliquam sit amet augue justo.
                """),
            html.Div(style={'display': 'flex',
                            'justifyContent': 'space-around',
                            'margin': '2rem 4rem 0 4rem'}, children=[
                sd.Button('Production',
                          id='btn-production',
                          variant='outlined',
                          n_clicks=0,
                          style={
                              'background-color': 'cornflowerblue',
                              'color': 'var(--text-color-dark)'
                          }),
                sd.Button('Supply',
                          id='btn-supply',
                          variant='outlined',
                          n_clicks=0,
                          style={
                              'background-color': 'forestgreen',
                              'color': 'var(--text-color-dark)'
                          }),
                sd.Button('Import',
                          id='btn-import',
                          variant='outlined',
                          n_clicks=0,
                          style={
                              'background-color': 'indianred',
                              'color': 'var(--text-color-dark)'
                          }),
                sd.Button('Export',
                          id='btn-export',
                          variant='outlined',
                          n_clicks=0,
                          style={
                              'background-color': 'rebeccapurple',
                              'color': 'var(--text-color-dark)'
                          }),
            ]),
        ]),

        dcc.Loading(dcc.Graph(
            id='fish-industry-map',
            className='fade-left'
        ))
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)

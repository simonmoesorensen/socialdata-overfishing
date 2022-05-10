from dash import Dash, dcc, html, Output, Input, callback_context
import sd_material_ui as sd

from plots.bar_plots import plot_protein
from plots.line_plots import plot_avg_global_consumption, plot_sustainability, plot_fishing_type, plot_gdp_cons
from plots.data import get_consumption, group_by_elements, get_population, get_industry_data, get_sustainability, \
    get_fishing_types, get_gdp, get_protein
from plots.choropleth_maps import plot_consumption_map, plot_industry_map

app = Dash(__name__)
server = app.server
app.title = 'Fishing for sustainability'

year = '2017'

# Data
df_consumption = get_consumption()
df_sustainability = get_sustainability()
df_fish_types = get_fishing_types()
df_population = get_population()
df_industry = get_industry_data()
df_gdp = get_gdp()
df_protein = get_protein()


industry_dict = {
    'production': group_by_elements(df_industry, df_population, ['Production'], year),
    'import': group_by_elements(df_industry, df_population, ['Import Quantity'], year),
    'supply': group_by_elements(df_industry, df_population, ['Domestic supply quantity'], year),
    'export': group_by_elements(df_industry, df_population, ['Export Quantity'], year)
}


# Callbacks
@app.callback(
    Output('fish-tab-industry', 'figure'),
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


app.layout = html.Div(className='main', children=[
    html.Div([
        html.H1(
            children='Fishing for sustainability',
            className='title fade-left'
        ),
        html.H2(
            children='A story on the best and worst fisheries of the world',
            className='text-subtitle fade-left'
        )
    ]),

    html.Div(
        className='two-column',
        style={'marginTop': '5rem'},
        children=[
            dcc.Tabs(parent_className='fade-left',
                     children=[
                         dcc.Tab(label='Map',
                                 className='custom-tab fade-up',
                                 selected_className='custom-tab--selected',
                                 children=[
                                     dcc.Graph(
                                         id='fish-tab-map',
                                         figure=plot_consumption_map(df_consumption)
                                     )
                                 ]),
                         dcc.Tab(label='Trend',
                                 className='custom-tab',
                                 selected_className='custom-tab--selected',
                                 children=[
                                     dcc.Loading(dcc.Graph(
                                         id='fish-tab-trend',
                                         figure=plot_avg_global_consumption(df_consumption)
                                     ))
                                 ]),
                         dcc.Tab(label='Overfishing',
                                 className='custom-tab',
                                 selected_className='custom-tab--selected',
                                 children=[
                                     dcc.Loading(dcc.Graph(
                                         id='fish-tab-overfishing',
                                         figure=plot_sustainability(df_sustainability)
                                     ))
                                 ]),
                         dcc.Tab(label='Industry',
                                 className='custom-tab',
                                 selected_className='custom-tab--selected',
                                 children=[
                                     html.Div(className='two-row', children=[
                                         dcc.Loading(dcc.Graph(
                                             id='fish-tab-industry',
                                             figure=plot_sustainability(df_sustainability)
                                         )),
                                         html.Div([
                                             html.Div(className='button-array',
                                                      children=[
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
                                                      ])
                                         ])
                                     ])
                                 ]),
                     ]),
            html.Div(className='two-row fade-right',
                     children=[
                         dcc.Markdown(className="text-box", children="""
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
                         html.Div(className='countries fade-up',
                                  children=[
                                      html.A(html.Button(className='country-button china'),
                                             href='#china'),
                                      html.A(html.Button('', className='country-button norway'),
                                             href='#norway')
                                  ])
                     ]),
        ]),

    #######################################################################
    ###                      GDP and Consumption                       ####
    #######################################################################

    html.H2('GDP and Consumption',
            id='gdp-consumption',
            className='title-medium',
            style={'marginTop': '16rem'}),

    html.Div(className='two-column', children=[
        dcc.Markdown(className="text-box",
                     children="""
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
        dcc.Graph(id='gdp-consumption-plot',
                  figure=plot_gdp_cons(df_gdp, df_consumption))
    ]),

    #######################################################################
    ###                         Protein intake                         ####
    #######################################################################

    html.H2('Protein intake',
            id='protein-intake',
            className='title-medium',
            style={'marginTop': '8rem'}),

    dcc.Graph(id='protein-intake-plot',
              className='graph-wide',
              figure=plot_protein(df_protein),
              responsive=True),

    html.Div(className='two-column', children=[
        dcc.Markdown(className="text-box",
                     children="""
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

    #######################################################################
    ###                Aquaculture and capture production              ####
    #######################################################################

    html.H2('Aquaculture and capture production',
            id='aquaculture-capture-production',
            className='title-medium',
            style={'marginTop': '8rem'}),

    #######################################################################
    ###                          Fishing types                         ####
    #######################################################################

    html.H2('Fishing types',
            id='fishing-types',
            className='title-medium',
            style={'marginTop': '8rem'}),

    html.Div(className='two-column', children=[
        html.Div(className='two-row', children=[
            dcc.Graph(id='china-fishing-types',
                      figure=plot_fishing_type(df_fish_types, 'China')),
            dcc.Graph(id='norway-fishing-types',
                      figure=plot_fishing_type(df_fish_types, 'Norway')),
        ]),
        dcc.Markdown(className="text-box",
                     style={'marginLeft': 0},
                     children="""
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
    ]),

    html.Div(className='two-column', children=[
        html.Div(className='two-row', children=[
            dcc.Markdown(className="text-box",
                         style={'marginLeft': 0},
                         children="""
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
    ]),

    #######################################################################
    ###                     Aquaculture emissions                      ####
    #######################################################################

    html.H2('Aquaculture emissions',
            id='aquaculture-emissions',
            className='title-medium',
            style={'marginTop': '8rem'}),

])

if __name__ == '__main__':
    app.run_server(debug=True)

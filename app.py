from dash import Dash, dcc, html, Output, Input, callback_context
import sd_material_ui as sd

from plots.bar_plots import plot_protein, plot_protein_ghg, plot_aquaculture_emissions
from plots.line_plots import plot_avg_global_consumption, plot_sustainability, plot_fishing_type, plot_gdp_cons, \
    plot_aquaculture_production
from plots.data import get_consumption, group_by_elements, get_population, get_industry_data, get_sustainability, \
    get_fishing_types, get_gdp, get_protein, get_protein_ghg, get_aquaculture, get_aquaculture_emissions
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
df_ghg = get_protein_ghg()
df_aqua = get_aquaculture()
df_aqua_emissions = get_aquaculture_emissions()

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
                                     html.Div(className='two-row', children=[
                                         dcc.Graph(
                                             id='fish-tab-map',
                                             figure=plot_consumption_map(df_consumption)),
                                         dcc.Markdown(className='text-box',
                                                      children="""
# Consumption

Now text
                                                  """)
                                     ])
                                 ]),
                         dcc.Tab(label='Trend',
                                 className='custom-tab',
                                 selected_className='custom-tab--selected',
                                 children=[
                                     html.Div(className='two-row', children=[
                                         dcc.Loading(dcc.Graph(
                                             id='fish-tab-trend',
                                             figure=plot_avg_global_consumption(df_consumption)
                                         )),
                                         dcc.Markdown(className='text-box',
                                                      children="""
# Trend

because
                                                      """)
                                     ])
                                 ]),
                         dcc.Tab(label='Overfishing',
                                 className='custom-tab',
                                 selected_className='custom-tab--selected',
                                 children=[
                                     html.Div(className='two-row', children=[
                                         dcc.Loading(dcc.Graph(
                                             id='fish-tab-overfishing',
                                             figure=plot_sustainability(df_sustainability)
                                         )),
                                         dcc.Markdown(className='text-box',
                                                      children="""
# Overfishing

over
                                                      """)
                                     ])
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
# Introduction
                                 
Overfishing, meaning we catch more fish then can naturally be replenished, has a wide variety of causes. 
However the biggest and most appearent one is simply the fact that we eat to much fish. 
Since the big supply of fish can only exist if there is a big demand for it. 
According to the Dietary Guidelines for Americans, 2010 (DGA) (add link and double check):

> People are recommended to eat 227 grams of fish per week, which comes to about 11.8kg yearly.

However our data shows us (see first tab) that most countries, greatly exceed this amount.
(maybe we should add a mask to the plot to show over/under this amount)
(also mentioning a global average might be nice)
This data comes from TODO

The second tab shows us that around the 1950s-1960s our fish consumption was near the recommended amount and since then 
has increased at an alarming rate of about 0.12 kg/capita/year, nearly doubling our average global fish consumption in 60 years. 
This coupled with the fact that our global population has more then doubled in the same time means the problem is getting exponentially worse every year. 
As a results it's not surprising that the amount of overexploited fishing is drasticly increasing, 
being made possible by the technological advancements of the last decades.

It's imporant to understand that overfishing means that we are catching more fish then replenish naturally. 
Meaning that every year that we overexploit an ocean the fish population decreases. 
As a result, say we overexploit an ocean by 35% in a year. If during the next year we decide to catch the exact same 
amount of fish as we did the year prior, we would now be overexploiting the ocean by closer to 37%. 
Since the fish population has decreased and therefore the amount that can naturally be replenished has decreased. 
Unfortunately the reality is worse, since we are fishing more and more each year and therefore this issue keeps growing and growing. 

When we start to look for which countries are most responsible for creating this issue, the answer is all of them. 
Most countries don't overfish simply because they don't have a large fishing industry. 
However this results in the fact that they simply import a larger amount of fish, which shifts the problem of overfishing to the exporting country. 
And since these countries are often underdeveloped they lack the resources to tackle overfishing.

These coastal nations often have a large economical insentive to supply this demand, since they rely on 
the fishing industry for a huge portion of their gross domestic product, often on the sale taxes it generates. 
The consequences for this is that while overfishing creates an immediate boost in profits, 
it destroy the whole industry in a matter of years. Since it reduces the fish population, 
which means there are less fish left to catch each following year.

Some additional consequences of overfishing are that:
- many isolated communities, rely on fishing not for income but for dietary purposes, with fish being their main source of protein. 
With the depletion of the fish population, they find their very way of life threatened.
- many fish species are going extinct and large preditors like sharks, dolphins, whales, and tuna, who are essential to 
maintaining the balanced ecosystem, are often innocent bystanders, caught in a trawler’s nets.
- the decrease in algea eating fish, causes an increase in the amount of algea who's acidity can negatively impact fish 
population, plankton, and reefs.
- fishermen disregarding maritime law and venturing into foreign waters, can be seen as a sign of agression.

Of course there are dozens of other causes of overfishing. And it is essential to note that each region has a has their 
own political and economical reasons that are creating the crisis. We simply can’t place every country into the same boat. However a few universal causes are that:
- there is a hugh challenge in regulating fishing vessels at the ports. The amount of vassels is just to large and most 
governments lack the resources for this work. Ironically goverments created this enviroment themselves as we have an estimated three times more fleets then necessairy, due to the high subsidies for fisherman.
- there is a lack of oversight when it comes to how much individual vassels are fishing, allowing them to overfish at will.
- there are little to no regulations on international waters.
- it is hard for countries to know the current fish populations and therefore the optimal fishing quotas.
- many public officials are either ignorant to fishing regulations and problems, which allows many fishermen to get around fishing laws.
- small vassels are able to fish and unload without being detected.
- only 1.5% of the world’s oceans are protected waters, leaving the rest fair game for fisherman.

The supply graph shows us the net supply of consumed fish per country, calculated as **Production + Import - Export**. 
This shows us that the biggest fish eaters worldwide are in order Norway, Iceland, Congo and China. 
These are countries with drastically different fishing industries and fishing cultures, which begs the question: who does it better? 
With a global problem as big as overfishing what we need is to find an industry leader that fishes responsable. 
So that every other country can learn from them. So let's do just that. Let's analyze the biggest fish eating countries 
to see which fishes more responsably and what rural political and economical climate as lead to it's development.

The countries we will be looking at are Norway and China. Since these are the countries with the biggest supply that's 
self produced, which also have significant cultural and geographical differences.

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

    html.Div(className='two-column',
             style={'marginTop': '5rem'},
             children=[
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
                 dcc.Graph(id='protein-emissions-plot',
                           figure=plot_protein_ghg(df_ghg))
             ]),

    #######################################################################
    ###                Aquaculture and capture production              ####
    #######################################################################

    html.H2('Aquaculture and capture production',
            id='aquaculture-capture-production',
            className='title-medium',
            style={'marginTop': '8rem'}),

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
        dcc.Graph(id='aquaculture-capture-production-plot',
                  figure=plot_aquaculture_production(df_aqua))
    ]),
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
        html.Div(className='two-row', children=[
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
        ]),

    ]),

    #######################################################################
    ###                     Aquaculture emissions                      ####
    #######################################################################

    html.H2('Aquaculture emissions',
            id='aquaculture-emissions',
            className='title-medium',
            style={'marginTop': '8rem'}),

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
        dcc.Graph(id='aquaculture-emissions-plot',
                  figure=plot_aquaculture_emissions(df_aqua_emissions))
    ]),

    html.H2('Conclusion',
            className='title-medium',
            id='conclusion',
            style={'marginTop': '8rem'}
            ),

    html.H2('References',
            className='title-medium',
            id='references',
            style={'marginBottom': 0,
                   'marginTop': '8rem'},
            ),

    html.Ol([
        html.Li([
            html.P([
                'Some textt ',
                html.Cite('George Citer'),
                ' More text from george'
            ])
        ]),
        html.Li([
            html.P([
                'Some textt ',
                html.Cite('George Citer'),
                ' More text from george'
            ])
        ]),
    ],
        className='references')

])

if __name__ == '__main__':
    app.run_server(debug=True)

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
    html.Div(className='navbar',
             children=[
                 html.Ul([
                     html.Li(html.A('Conclusion', href='#conclusion')),
                     html.Li(html.A('Aquaculture Emissions', href='#aquaculture-emissions')),
                     html.Li(html.A('Fishing Types', href='#fishing-types')),
                     html.Li(html.A('Aquaculture and Capture production', href='#aquaculture-capture-production')),
                     html.Li(html.A('Protein intake', href='#protein-intake')),
                     html.Li(html.A('GDP and Consumption', href='#gdp-consumption')),
                     html.Li(html.A('Introduction', href='#introduction')),
                 ])
             ]),

    html.Div(id='title',
             children=[
                 html.H1(
                     children='Fishing for sustainability',
                     className='title fade-left'
                 ),
                 html.H2(
                     children='A story on the best and worst fisheries of the world',
                     className='text-subtitle fade-left'
                 ),
                 html.Div(
                     className='contact-info fade-left',
                     children=[
                         html.H4(
                             'By: Niels Jansen (s217149), Yufan Du (s210356), and Simon Moe Sørensen (s174420)',
                             style={
                                 'color': 'var(--text-secondary-color-dark)'
                             }
                         ),
                         html.A(
                             html.Img(
                                src='./assets/github-icon.png',
                                style={
                                    'width': '25px',
                                    'height': '25px',
                                }),
                             target='_blank',
                             href='https://github.com/simonmoesorensen/socialdata-overfishing',
                             style={
                                 'marginLeft': '1rem'
                             })
                     ])

             ]),

    html.Div(
        id='introduction',
        className='two-column',
        style={'marginTop': '5rem'},
        children=[
            dcc.Tabs(parent_className='fade-left flex-0',
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

By clicking `Play` in the map above, you will see a video of how the consumption of fish has developed from 1961 to 2017.
It is clear that in the recent past, 2010 and above, the consumption of fish has increased with significant speed.
Especially in the **Nordic** and **East / South East Asia** regions we see a lot of consumption pr capita. 
As representatives of each region, we observe in 2017, that Norway has a consumption of `51.35` kg pr capita and `China` has
a consumption of `38.17` kg pr capita. Other worthy mentions of high consumption pr capita is Iceland with `90.71`,
Maldives with `90.41`, Portugal with `56.84`, and a collection of countries in the south east pacific ranging around 40 to 60.

We have chosen to focus primarily on **Norway** and **China** as representatives for the European region and the South
East Pacific region respectively. This is due to the size of the country with respect to neighbouring countries, that
leads to a higher absolute impact on the fishing industry. 
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

Around the 1960s-1970s our fish consumption was near the recommended amount and since then 
has increased at an alarming rate of about 0.12 kg/capita/year, nearly doubling our average global fish consumption in 60 years. 
This coupled with the fact that our global population has more then doubled in the same time means the problem is getting exponentially worse every year. 
As a result, it's not surprising that the amount of overexploited fishing is drastically increasing, 
being made possible by the technological advancements over the last decades.
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

Every year that we overexploit an ocean, the fish population decreases. 
As a result, say we overexploit an ocean by 35% in a year. If during the next year we decide to catch the exact same 
amount of fish as we did the year prior, we would now be overexploiting the ocean by closer to 37%. 
Since the fish population has decreased and therefore the amount that can naturally be replenished has decreased. 
Unfortunately the reality is worse, since we are fishing more and more each year and therefore this issue keeps growing and growing. 

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
                                             html.Div(className='two-row',
                                                      children=[
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
                                                                   ]),
                                                          dcc.Markdown(className='text-box',
                                                                       children="""
# Industry 

When we start to look for which countries are most responsible for creating this issue, the answer is all of them. 
Most countries don't overfish simply because they don't have a large fishing industry. 
However this results in the fact that they simply import a larger amount of fish, which shifts the problem of overfishing to the exporting country. 
And since these countries are often underdeveloped they lack the resources to tackle overfishing.

These coastal nations often have a large economical insentive to supply this demand, since they rely on 
the fishing industry for a huge portion of their gross domestic product, often on the sale taxes it generates. 
The consequences for this is that while overfishing creates an immediate boost in profits, 
it destroy the whole industry in a matter of years. Since it reduces the fish population, 
which means there are less fish left to catch each following year.

The supply graph shows us the net supply of consumed fish per country, calculated as **Production + Import - Export**. 
This shows us that the biggest fish eaters worldwide are in order Norway, Iceland, Congo and China. 
These are countries with drastically different fishing industries and fishing cultures, which begs the question: who does it better? 
With a global problem as big as overfishing what we need is to find an industry leader that fishes responsable. 
So that every other country can learn from them. So let's do just that. Let's analyze the biggest fish eating countries 
to see which fishes more responsably and what rural political and economical climate as lead to it's development.

The countries we will be looking at are Norway and China. Since these are the countries with the biggest supply that's 
self produced, which also have significant cultural and geographical differences.
                                                                       """)
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

## Old text

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
                     
The graph shows us that the relationship between per capita seafood consumption and average GDP per capita. 
What we can see is that they are strong positive correlated. The more money people earn, the more seafood they eat.

According to Nestle et al., annual household income influences food choices, particularly costly foods such as fish. 
Namely, fish is expected to be less accessible in ‘poor urban and rural communities’, and even if it is available, 
insufficient capital potentially generates a barrier for acquisition and consumption (Nestle et al., 1998).

As we can see, Norway's per capita GDP is significantly higher than china's, hence every Norwegian eats more seafood per year. 
Overall, both countries tend to get richer and eat more seafood.
 
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

    dcc.Markdown(className="text-box",
                 style={'marginTop': '2rem'},
                 children="""
## Distribution of protein sources

As we mentioned before, the per capita GDP in both China and Norway is growing year by year, 
it means that people can improve their living quality on the basis of meeting their basic needs. 
They are now more concerned about diet health and nutrient intake.

Seafood contains a high-quality protein that includes all of the essential amino acids for human health, 
making it a complete protein source. The protein in seafood is also easier to digest because it has less connective 
tissue than red meats and poultry. For certain groups of people such as the elderly who may have difficulty chewing or 
digesting their food, seafood can be a good choice to help them obtain their daily protein needs.[]

We can see in the graph that Chinese people intake protein mainly from pork and seafood while Norwegian people prefer 
milk and seafood. It accounts for around 24% of protein consumption in both countries, it means people in China and 
Norway has similar seafood protein intake habit. Interesting thing is that Norway per capita GDP is more than four times 
China's in recent years, however, the differences in seafood consumption between the two countries are not much like that. 
Hence, it means that China has a high production volume which can meet people demand with relatively low prices.
            """),

    html.Div(className='two-column',
             style={'marginTop': '5rem'},
             children=[

                 dcc.Graph(id='protein-emissions-plot',
                           figure=plot_protein_ghg(df_ghg)),
                 dcc.Markdown(className='text-box',
                              children="""
## Greenhouse Gas Emission

Human behaviours are causing several global environmental disruptions. 
Greenhouse gas emission is one of the most important environmental problems, causing global temperatures to rise. 
With the increasing people's awareness of environmental protection. More and more people want to reduce the carbon 
footprint of their food, hence they prefer to eat foods that have lower greenhouse gas emissions.

Ensuring everyone in the world has access to a nutritious diet in a sustainable way is one of the greatest challenges 
we face. Food production contributes around 37 percent of global greenhouse gas (GHG) emissions, showing the huge impact
that our diets have on climate change. What’s more, animal-based foods produce roughly twice the emissions of 
plant-based ones[].

In the bar chart, we can see that beef and lamb are the main culprits of GHG emissions if we want to get 100g of protein, 
which accounts for approximately 70kg. That's because they are ruminant animals, they rely on specialized bacteria in 
their gut to break down food. These bacteria release a large amount of methane, a potent GHG that strongly contributes
to global warming[].However, it only discharges 6kg GHG to get the same amount of protein by eating fish and seafood,
which is a good way to get enough nutrition in a sustainable way.
  
                              """)
             ]),

    #######################################################################
    ###                Aquaculture and capture production              ####
    #######################################################################

    html.H2('Aquaculture and Capture production',
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

    html.H2('Fishing Types',
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

    html.H2('Aquaculture Emissions',
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

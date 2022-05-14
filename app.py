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
            title="Import for year 2017"
        )
    elif 'btn-export' in changed_id:
        # Default to production
        plot = plot_industry_map(
            industry_dict['export'].reset_index(),
            title="Export for year 2017"
        )
    elif 'btn-supply' in changed_id:
        # Default to production
        plot = plot_industry_map(
            industry_dict['supply'].reset_index(),
            title="Supply for year 2017"
        )
    else:
        # Default to production
        plot = plot_industry_map(
            industry_dict['production'].reset_index(),
            title="Production for year 2017"
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
        style={'marginTop': '5rem'},
        children=[
            dcc.Tabs(parent_className='fade-left flex-0',
                     children=[
                         dcc.Tab(label='Consumption',
                                 className='custom-tab fade-up',
                                 selected_className='custom-tab--selected',
                                 children=[
                                     html.Div(className='two-column', children=[
                                         dcc.Graph(
                                             id='fish-tab-consumption',
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
                                     html.Div(className='two-column', children=[
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
                                     html.Div(className='two-column', children=[
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
                                     html.Div(className='two-column', children=[
                                         dcc.Loading(
                                             html.Div(className='industry-container',
                                                      children=[
                                                          dcc.Graph(
                                                              id='fish-tab-industry',
                                                              figure=plot_sustainability(df_sustainability)),
                                                          html.Div(className='button-array',
                                                                   style={'gap': '1rem',
                                                                          'marginTop': '1rem'},
                                                                   children=[
                                                                       sd.Button('Production',
                                                                                 className='button',
                                                                                 id='btn-production',
                                                                                 variant='outlined',
                                                                                 n_clicks=0,
                                                                                 style={
                                                                                     'background-color': 'cornflowerblue',
                                                                                     'color': 'var(--text-color-dark)'
                                                                                 }),
                                                                       sd.Button('Supply',
                                                                                 className='button',
                                                                                 id='btn-supply',
                                                                                 variant='outlined',
                                                                                 n_clicks=0,
                                                                                 style={
                                                                                     'background-color': 'forestgreen',
                                                                                     'color': 'var(--text-color-dark)'
                                                                                 }),
                                                                       sd.Button('Import',
                                                                                 className='button',
                                                                                 id='btn-import',
                                                                                 variant='outlined',
                                                                                 n_clicks=0,
                                                                                 style={
                                                                                     'background-color': 'indianred',
                                                                                     'color': 'var(--text-color-dark)'
                                                                                 }),
                                                                       sd.Button('Export',
                                                                                 className='button',
                                                                                 id='btn-export',
                                                                                 variant='outlined',
                                                                                 n_clicks=0,
                                                                                 style={
                                                                                     'background-color': 'rebeccapurple',
                                                                                     'color': 'var(--text-color-dark)'
                                                                                 }),
                                                                   ])
                                                      ])),
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
                                 ]),
                     ]),
        ]),

    html.Div(className='two-row fade-right',
             style={'marginTop': '1rem'},
             children=[
                 dcc.Markdown(className="text-box", children="""
# Introduction
Fishing has been the most important industry for human beings since ancient times, including marine fisheries, freshwater fisheries, 
capture fisheries and aquaculture fisheries. Seafood is also one of the most common foods, such as fish and shrimp. 
It is precisely because of these factors that the development of fishery and the problems it brings have received attention.

People's demand for seafood is mainly reflected in several aspects. For developing countries, 
small-scale fishing can meet people's basic living needs, and may also become the economic backbone of the country, 
such as exporting a large number of seafood to the world's Other countries. For developed countries or relatively wealthy countries, 
they seem to pay more attention to the nutrition, taste and environmental friendliness of seafood, so they will meet the demand through fishing, 
farming and importing seafood. No matter from which point of view, it will lead to an increasing demand for seafood in the world. 
However, many countries do not pay attention to sustainable fishing, so the reserves of marine fish are getting smaller and smaller. 
Combined with many wrong fishing methods, it has brought a devastating blow to other marine life and the marine environment.

In order to alleviate the supply gap caused by the shortage of seafood resources, many countries in the world have thought of innovative methods 
such as the development of aquaculture. This can help to alleviate some of the pressure on wild fish catch. But it also brings many new problems, 
such as greenhouse gas emission and eutrophication.

Both China and Norway are big fishing nations, but their fisheries development methods are very different. But in general, 
Norway's overexploited fishing rate is much lower than China. Therefore, we want to find ways of sustainable fishing by 
comparing these two countries and find out where China's unsustainable fishing activities are. More interestingly, 
we found the advantage of seafood as a protein intake, and in order to maximize this advantage, sustainable fishing activities become more important.
                                 """),
             ]),
    #######################################################################
    ###                      GDP and Consumption                       ####
    #######################################################################

    html.H2('GDP and Consumption',
            id='gdp-consumption',
            className='title-medium'),

    html.Div(className='two-column', children=[
        dcc.Markdown(className="text-box",
                     children="""
                     
We've already established that the average person nowadays eats about twice as much fish as they did 60 years ago and the reason we eat this much fish 
is simple, it's healthy and delicious. But that begs the question, why didn't we eat this much fish previously. Well the answer won't surprise you, 
it's money. Fish as well as meat is historically one of the more expensive food items and therefore wasn't previously as easy to come by.



Indeed the graph shows us that the relationship between per capita seafood consumption and average GDP per capita. What we can see from it is that 
they are strong positively correlated. The more money people earn, the more seafood they eat.



> According to Nestle et al., "*annual household income influences food choices, particularly costly foods such as fish. Namely, fish is expected to 
be less accessible in ‘poor urban and rural communities’, and even if it is available, insufficient capital potentially generates a barrier for 
acquisition and consumption.*" (Nestle et al., 1998)


As we can see this results in the fact that since Norway's per capita GDP is significantly higher than china's, every Norwegian eats more seafood 
per year. However something else that should be noted is that the price of fish also plays a role here. Having a higher GDP is nice, 
but utterly meaningless if the price of a product also increases. And this is where the trends of countries can start to differ in the 
upcoming decades, since the growth of the aquaculture industry could start to bring down the local price of fish.

"*In other regions, particularly throughout Asia, the expansion of aquaculture has driven down real prices for farmed fish produced in large volumes, 
making them increasingly accessible to low-income consumers. Meanwhile, wild capture fish have become more expensive, both in real terms and relative 
to farmed fish, often restricting their accessibility to wealthier consumers*" (Naylor et al., 21) However this remains to be seen.

            """),
        dcc.Graph(id='gdp-consumption-plot',
                  figure=plot_gdp_cons(df_gdp, df_consumption))
    ]),

    #######################################################################
    ###                         Protein intake                         ####
    #######################################################################

    html.H2('Protein intake',
            id='protein-intake',
            className='title-medium'),

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
            className='title-medium'),

    html.Div(className='two-column', children=[
        dcc.Markdown(className="text-box",
                     children="""
The growing issue of overfishing has allowed the rapid growth of the aqaculture, or fish farming, 
industry over the last decades as can be seen in the figures. 
Fish produced from farming activities currently accounts for over one quarter of all fish directly consumed by humans.

Many people believe that aquaculture will replace a large part of wild capture production over the next decades. 
And that it will be able to reduce pressure on ocean harvests to allow the fish population to recover. 
However in reality the industry is not as efficient as it seems and the industry will have to change if it ever wants to fulfill this role.

To begin with a large part of the aquaculture production are carnivorous fish species, such as salmon, 
that require 2 to 5 times more fish protein, in the form of fish meal made from scrap fish products, 
to feed the farmed species than is supplied by the farmed product. And a lot of this protein originates from wild captured fish, 
which as you can imagine is counter-productive. 
Even herbivorous and omnivorous freshwater fish that require minimal quantities of fish meal are fed with about 15% fish meal, 
exceeding required levels. For the ten types of fish most commonly farmed, 
an average of 1.9 kg of wild fish is required for every kilogram of fish raised on compound feeds. 
So it's clear to see that the growing aquaculture industry cannot continue to rely on infinite stocks of wild-caught fish.

Currently China produces around two thirds of the global aquaculture production, with the common carp, an omnivorous, as it's biggest product. 
Whilest Norways most farmed fish is the Atlantic salmon, a carnivour. 
Should China solve it's inefficient practises it's aquaculture industry should be able to thrive and result in a greater global (net) fish supply.

Unfortunately inefficiency is not the only problem with this industry. Other include that:

* Aquaculture can also diminish wild fisheries indirectly by habitat modification
* wild caught fish are used to stock aquaculture ponds
* the creation of fish meal through over-exploitation reduces available food supplies for marine predators
* the introduction of exotic species, through farm escapees, upsets ecosystems and harms wild fish populations
* untreated wastewater of fish farms causes nutrient pollution
* Aquaculture is a lot more at risk from outside threads then the fishing industry. For example, in 2010 aquaculture production in China suffered losses of 1.7 million tonnes (worth US$3.3 thousand million) due to disease outbreaks (295 thousand tonnes), natural disasters (1.2 million tonnes), and pollution (123 thousand tonnes) (FAO 2012).
        """),
        dcc.Graph(id='aquaculture-capture-production-plot',
                  figure=plot_aquaculture_production(df_aqua))
    ]),
    #######################################################################
    ###                          Fishing types                         ####
    #######################################################################

    html.H2('Fishing Types',
            id='fishing-types',
            className='title-medium'),

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

# Fishing methods                         

There are a lot of ways to catch fish around the world. Overall, pole-and-line,
longline, and gillnet methods are more common in lower-income countries where 
much of the fishing activity is subsistence or small-scale. Purse seine and 
trawling methods are more common in industrial fishing practices, these tend 
to catch more fish per unit of effort.[].

## Trawling

Trawling methods have larger negative impacts on ecology compared to purse seine, 
especially bottom trawls, because bottom trawls are pulled directly above or on
the seabed. They are very efficient in capturing large number of fish, but give
the organisms that live there a devastating impact. Furthermore, trawling methods
generate much more discards than others, one-fifth (21%) of catch from bottom
trawls is thrown back into the ocean. Fishers will throw unwanted fish back
into the ocean, including sharks, sea turtles and juvenile fish, but the 
survival rate of these discarded animals is lower and it will lead to overfishing.

## China versus Norway

Both China and Norway are high seafood production countries, hence pole-and-line,
longline, and gillnet methods are not efficient ways to meet their demand.
It is clear to see that China and Norway use different fish catching methods, 
Norwegian people prefer to use purse seine while Chinese prefer trawl methods.
It means that China is using a pretty unsustainable way to supply fish and
seafood. As we can see, the fish catch number of all types decreased in China 
from 2015, which may be the consequence of bottom trawling.
The seabed damage and unsustainable catch lead to unhealthy fish and fish stocks
shortage. In contrast, Norway's fish catch volume is relatively stable and sustainable.
        """),
        ]),

    ]),

    #######################################################################
    ###                     Aquaculture emissions                      ####
    #######################################################################

    html.H2('Aquaculture Emissions',
            id='aquaculture-emissions',
            className='title-medium'),

    html.Div(className='two-column', children=[
        dcc.Markdown(className="text-box",
                     children="""
The food industry is a mayor driver in enviromental change, responsible for a quarter of all greenhouse gasses (GHG). 
Reducing the GHG emmisions is vital to reaching emission goals and creating a sustainable feature.

Fish and other aquatic foods (blue foods) are an effective way of reaching this sustainable diet. As the graph shows GHG emmisions, 
as well as other enviromental stressors, of most blue food groups compare favourably to industrial chicken production, 
which typically has lower stressors then other livestock. However this holds true for both aquacultere captures as well as capture fisheries.
Although generally farmed fish produce a lower or equal average emission then their captured counterpart.

Most of the emissions of aquacultere result from growing fish food, whearas in the capture fisheries fuel causes the most emission. 
For fed systems 87% of N and 94% of P occur on food farms. 
Which also means that non-fed groups such as seaweeds and bivalve remove more N and P than is emitted during production.

However since aquacuture uses land for both the fish and food farms, this creates a trade-offs with alternate uses, 
including production of other foods. And since the availability and access to freshwater inceasingly constraints the agriculture industry, 
this creates a downside to fed-systems where freshwater is largely used in feed production, 
whearas capture fisheries and unfed systems require little freshwater.

As it turns out although farmed fish does not appear to have a mayor enviromental benefit, compared to captured fish, 
at the moment it is also safe to say that the industry has not nearly reached it's full potential. 
It's still a young and rapid growing sector with many promosing technolgies and policies to improve it's efficiency. 
Where the main problem to tackle while expanding is making sure new inventions are not beond the reach of the many small producers.
    """),
        dcc.Graph(id='aquaculture-emissions-plot',
                  figure=plot_aquaculture_emissions(df_aqua_emissions))
    ]),

    html.H2('Conclusion',
            className='title-medium',
            id='conclusion'),

    html.H2('References',
            className='title-medium',
            id='references',
            style={'marginBottom': 0}),

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

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
                     html.Li(html.A('Aquaculture and Capture production', href='#aquaculture-capture-production')),
                     html.Li(html.A('Fishing Methods', href='#fishing-types')),
                     html.Li(html.A('Protein Intake', href='#protein-intake')),
                     html.Li(html.A('Consumption and GDP', href='#gdp-consumption')),
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

By clicking `Play` on the map to the left, you will see a video of how the consumption of fish has developed from 1961 to 2017.
It is clear that in the recent past, 2010 and above, the consumption of fish has increased with significant speed.
Especially in the **Nordic** and **East / South East Asia** regions we see a lot of consumption per capita. 
As we observe in 2017, that Norway has a consumption of `51.35` kg pr capita and `China` had
a consumption of `38.17` kg per capita. Other worthy mentions of high consumption per capita in Iceland with `90.71`,
The Maldives with `90.41`, Portugal with `56.84`, and a collection of countries in the south-east pacific ranging around 40 to 60.

We have chosen to focus primarily on **Norway** and **China** as representatives for the European region and the South
East Pacific region respectively. This is due to the size of the country concerning neighbouring countries, which
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
This coupled with the fact that our global population has more than doubled in the same time means the problem is getting exponentially worse every year. 
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
As a result, say we overexploit an ocean by 35% in a year. If during the next year we decide to catch the same 
amount of fish as we did the year prior, we would now be overexploiting the ocean closer to 37%. This effects the fish
population significantly since a decreased population of fish also leads to a decrease of the amount that can naturally 
be replenished. Thus it is a negative feedback loop. 
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

_Try clicking the buttons on the left_

We will start to look for which countries are most responsible for creating this issue. Most countries don't overfish 
simply because they don't have a large fishing industry. However, this results in the fact that they simply import a 
larger amount of fish rather than producing it themselves. This shifts the problem of overfishing to the exporting 
country. And since these countries are often underdeveloped they lack the resources to tackle overfishing. 

The coastal nations often have a large economical incentive to supply this demand, since they rely on 
the fishing industry for a huge portion of their gross domestic product (GDP), often on the sale taxes, it generates. 
The consequence of this is that while overfishing creates an immediate boost in profits, 
it destroys the whole industry in a matter of years. Since it reduces the fish population, 
which means there are fewer fish left to catch each following year.

The supply graph shows us the net supply of consumed fish per country, calculated as **Production + Import - Export**. 
This shows us that the biggest fish eaters worldwide are in order Norway, Iceland, Congo and China. 
These are countries with drastically different fishing industries and fishing cultures, which begs the question: who does it better? 
With a global problem as big as overfishing what we need, is to find an industry leader that fishes responsible. 
So that every other country can learn from them. So let's do just that. Let's analyze the biggest fish eating countries 
to see which fishes more responsibly and what rural political and economical climate has led to its development.

The countries we will be looking at are Norway and China. Since these are the countries with the biggest supply that's 
self-produced, which also have significant cultural and geographical differences.
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
capture fisheries and aquaculture fisheries. Seafood is also one of the most common foods, such as fish and shrimp [[7]](https://www.globalseafood.org/advocate/seafoods-newfound-retail-popularity-has-a-permanent-feel-to-it/). 
It is exactly because of these factors that the development of fishery and the problems it brings, have received attention.

People's demand for seafood is mainly reflected in several aspects. For developing countries, small-scale fishing can 
meet people's basic living needs, and may also become the economic backbone of the country, such as exporting seafood 
to the world's Other countries. For developed countries or relatively wealthy countries, they seem to pay more 
attention to the nutrition, taste and environmental friendliness of seafood, so they will meet the demand through 
fishing, farming and importing seafood. No matter from which point of view, it will lead to increasing demand for 
seafood in the world. However, many countries do not pay attention to sustainable fishing, so the reserves of marine 
fish are getting smaller and smaller. Combined with fishing methods such as bottom trawling, it has brought a devastating blow to 
other marine life and the marine environment. 

To alleviate the supply gap caused by the shortage of seafood resources, many countries in the world have thought of 
innovative methods such as the development of aquaculture. This can help to alleviate some of the pressure on wild 
fish catch. But it also brings many new problems, such as greenhouse gas emissions and eutrophication. 

Both China and Norway are big fishing nations, but their fisheries development methods are very different. But in 
general, Norway's overexploited fishing rate is much lower than China's. Therefore, we want to find ways of 
sustainable fishing by comparing these two countries and find out where China's unsustainable fishing activities are. 
More interestingly, we found the advantage of seafood as a protein intake, and to maximize this advantage, 
sustainable fishing activities become more important. 
"""),
             ]),
    #######################################################################
    ###                      GDP and Consumption                       ####
    #######################################################################

    html.H2('Consumption and GDP',
            id='gdp-consumption',
            className='title-medium'),

    html.Div(className='two-column', children=[
        dcc.Markdown(className="text-box",
                     children="""
We've already established that the average person nowadays eats about twice as much 
fish as they did 60 years ago (Trend) and the reason we eat this much fish is simple, 
it's healthy and delicious. But that begs the question, why didn't we eat this much fish 
previously. Well, the answer won't surprise you, it's money. Fish as well as meat is 
historically one of the more expensive food items and therefore wasn't previously as easy to 
come by. 

Indeed the graph shows us the relationship between per capita seafood consumption and average GDP per capita. What we 
can see from it is that they are strongly positively correlated (correlation of 0.96). The more money people earn, 
the more seafood they eat. 

> According to Nestle et al., "*annual household income influences food choices, particularly costly foods such as 
fish. Namely, fish is expected to be less accessible in ‘poor urban and rural communities, and even if it is 
available, insufficient capital potentially generates a barrier for acquisition and consumption.*" (Nestle et al., 
1998)[[1]](https://deepblue.lib.umich.edu/bitstream/handle/2027.42/75438/j.1753-4887.1998.tb01732.x.pdf?sequence=1) 

As we can see this results in the fact that since Norway's per capita GDP is significantly higher than China's, 
every Norwegian eats more seafood per year. However, something else that should be noted is that the price of fish 
also plays a role here. Having a higher GDP is nice, but utterly meaningless if the price of a product also 
increases. And this is where the trends of countries can start to differ in the upcoming decades since the growth of 
the aquaculture industry could start to bring down the local price of fish. 

> "*In other regions, particularly 
throughout Asia, the expansion of aquaculture has driven down real prices for farmed fish produced in large volumes, 
making them increasingly accessible to low-income consumers. Meanwhile, wild capture fish have become more expensive, 
both in real terms and relative to farmed fish, often restricting their accessibility to wealthier consumers*" (
Naylor et al., 21) [[2]](https://www.nature.com/articles/s41467-021-25516-4) 

In general, it's safe to say that the average global GDP will continue to rise, meaning people will continue to 
improve their living quality instead of just fulfilling their basic needs. As a result, they are now more concerned 
about dietary health and nutritional intake, which will cause the demand for protein foods, such as fish and meat to 
continue growing. Seeing as how we are already unable to supply the world's demand for protein products and rely on 
overexploiting marine life and are increasing global greenhouse gas (GHG) emissions, how will we facilitate this 
growth? 

            """),
        dcc.Graph(id='gdp-consumption-plot',
                  figure=plot_gdp_cons(df_gdp, df_consumption))
    ]),

    #######################################################################
    ###                         Protein Intake                         ####
    #######################################################################

    html.H2('Protein Intake',
            id='protein-intake',
            className='title-medium'),

    html.Div(className='two-column',
             style={'marginTop': '2rem'},
             children=[
                 dcc.Graph(id='protein-emissions-plot',
                           figure=plot_protein_ghg(df_ghg)),
                 dcc.Markdown(className='text-box',
                              children="""
## Greenhouse Gas Emissions

Human behaviours are causing several global 
environmental disruptions. Greenhouse gas emissions are one of the most important 
environmental problems, causing global temperatures to rise. With people becoming 
increasingly aware of the need for environmental protection. More and more people want 
to reduce the carbon footprint of their food, hence they prefer to eat foods that have 
lower greenhouse gas emissions. 

Ensuring everyone in the world has access to a nutritious diet sustainably is one of the greatest challenges we face. 
Food production contributes around 37 per cent of global greenhouse gas (GHG) emissions, showing the huge impact that 
our diets have on climate change. What’s more, animal-based foods produce roughly twice the emissions of plant-based 
ones [[9]](https://ourworldindata.org/environmental-impacts-of-food). 

In the bar chart, we can see that beef and lamb are the main culprits of GHG emissions. That's because they are 
ruminant animals, they rely on specialized bacteria in their gut to break down food. These bacteria release a large 
amount of methane, a potent GHG that strongly contributes to global warming [[10]](
https://sustainablefisheries-uw.org/seafood-101/cost-of-food/) . 

The bar chart also shows us that fish and seafood create the least GHG emissions for the same amount of protein, 
therefore being a better way to get enough nutrition sustainably. More seafood also has other benefits apart from 
being more environmentally friendly. 

"""
                              ),
             ]),

    dcc.Graph(id='protein-intake-plot',
              className='graph-wide',
              style={'marginTop': '2rem'},
              figure=plot_protein(df_protein),
              responsive=True),

    dcc.Markdown(className="text-box",
                 children="""
## Distribution of protein sources 
 
Seafood contains a high-quality protein that includes 
all of the essential amino acids for human health, making it a complete protein source. The protein 
in seafood is also easier to digest because it has less connective tissue than red meats and 
poultry. For certain groups of people such as the elderly who may have difficulty chewing or 
digesting their food, seafood can be a good choice to help them obtain their daily protein needs [[
11]](https://www.seafoodhealthfacts.org/nutrition/seafood-nutrition-overview/). 

We can see in the graph that Chinese people intake protein mainly from pork and seafood while Norwegian people prefer 
milk and seafood, where seafood accounts for around 24% of protein consumption in both countries. Showing us that 
people in China and Norway have similar seafood protein intake habits. However interestingly, since we've already 
established that Chinese people eat less fish per capita, that also means that at the moment they eat less protein 
overall. 

So we've established that fish is arguably the better protein source with a relatively low amount of GHG emissions. 
That still doesn't address the fact the current trend of overfishing is unsustainable. One major factor in that is 
the ineffective current fishing practices. 

            """),

    #######################################################################
    ###                          Fishing Methods                         ####
    #######################################################################

    html.H2('Fishing Methods',
            id='fishing-types',
            className='title-medium'),

    html.Div(className='two-column', children=[
        html.Div(className='two-row', children=[
            dcc.Markdown(className="text-box",
                         children="""
# Fishing methods 

There are a lot of ways to catch fish around the world. 
Overall, pole-and-line, longline, and gillnet methods are more common in lower-income 
countries where much of the fishing activity is subsistence or small-scale. Purse seine and 
trawling methods are more common in industrial fishing practices, these tend to catch more 
fish per unit of effort [[12]](https://ourworldindata.org/fish-and-overfishing). 

## Trawling 

Trawling methods have larger negative impacts on ecology compared to purse seine, especially bottom 
trawls, because bottom trawls are pulled directly above or on the seabed. They are very efficient in capturing a 
large number of fish but give the organisms that live there a devastating impact. Furthermore, trawling methods 
generate much more discards than others, one-fifth (21%) of catch from bottom trawls is thrown back into the ocean. 
Fishers will throw unwanted fish back into the ocean, including sharks, sea turtles and juvenile fish, 
but the survival rate of these discarded animals is lower and it will lead to overfishing. 

## China versus Norway

Both China and Norway are high seafood production countries, hence pole-and-line, longline, 
and gillnet methods are not efficient ways to meet their demand. It is clear to see that China and Norway use 
different fish catching methods, Norwegian people prefer to use purse seine while Chinese prefer trawl methods. It 
means that China is using an unsustainable way to supply fish and seafood. As we can see, the fish catch number 
of all types decreased in China from 2015, which may be the consequence of bottom trawling. The seabed damage and 
unsustainable catch lead to unhealthy fish and fish stocks shortage. In contrast, Norway's fish catch volume is 
relatively stable and sustainable. 

Unfortunately, China plays a big role in the fishing industry, which we can't do without. And it's safe to say that 
the methods they use need improvements, however, there is one more fishing industry that we haven't discussed yet, 
aquaculture. 
        
        """),
        ]),
        html.Div(className='two-row', children=[
            dcc.Graph(id='china-fishing-types',
                      figure=plot_fishing_type(df_fish_types, 'China')),
            dcc.Graph(id='norway-fishing-types',
                      figure=plot_fishing_type(df_fish_types, 'Norway')),
        ]),

    ]),

    #######################################################################
    ###                Aquaculture and capture production              ####
    #######################################################################

    html.H2('Aquaculture and Capture production',
            id='aquaculture-capture-production',
            className='title-medium'),

    html.Div(className='two-column', children=[
        dcc.Graph(id='aquaculture-capture-production-plot',
                  figure=plot_aquaculture_production(df_aqua)),
        dcc.Markdown(className="text-box",
                     children="""

The growing issue of overfishing has allowed the rapid growth of the aquaculture, or fish farming, industry over the 
last decades as can be seen in the figures. Fish produced from farming activities currently accounts for over 
one-quarter of all fish directly consumed by humans. 

Many people believe that aquaculture will replace a large part of wild capture production over the next decades. And 
that it will be able to reduce pressure on ocean harvests to allow the fish population to recover. However in reality 
the industry is not as efficient as it seems and the industry will have to change if it ever wants to fulfil this role. 

To begin with, a large part of the aquaculture production is carnivorous fish species, such as salmon, that require 2 
to 5 times more fish protein, in the form of fish meal made from scrap fish products, to feed the farmed species than 
is supplied by the farmed product. And a lot of this protein originates from wild captured fish, which as you can 
imagine is counter-productive. Even herbivorous and omnivorous freshwater fish that require minimal quantities of a 
fish meal is fed with about 15% fish meal, exceeding the required levels. [[3]](
https://agris.fao.org/agris-search/search.do?recordID=XF2016025408) For the ten types of fish most commonly farmed, 
an average of 1.9 kg of wild fish is required for every kilogram of fish raised on compound feeds. [[4]](
https://www.nature.com/articles/35016500) So it's clear to see that the growing aquaculture industry cannot continue 
to rely on stocks of wild-caught fish. 

Unfortunately, inefficiency is not the only problem with this industry. Others include that: 

- aquaculture can also diminish wild fisheries indirectly through habitat modification 
- wild-caught fish are used to stock aquaculture ponds 
- the creation of fish meals through over-exploitation reduces available food supplies for marine predators 
- the introduction of exotic species, through farm escapees, upsets ecosystems and harms wild fish populations 
- untreated wastewater from fish farms causes nutrient pollution 
- aquaculture is a lot more at risk from outside threads than the fishing industry. For example, in 2010 aquaculture 
production in China suffered losses of 1.7 
million tonnes (worth US$3.3 thousand million) due to disease outbreaks (295 thousand tonnes), natural disasters (1.2 
million tonnes), and pollution (123 thousand tonnes) (FAO 2012) [[8]](https://www.fao.org/home/en/). 

Currently, China produces around two-thirds of the global aquaculture production, with the common carp, 
an omnivorous, as its biggest product. Whilst Norway's most farmed fish is the Atlantic salmon, a carnivore 
[[5]](https://eurofish.dk/member-countries/norway).
Should China solve its inefficient practices, the aquaculture industry 
will be able to thrive and result in a greater global (net) fish supply. 

So far we're only talked about the negatives, so let's shine some light on one major benefit that aquaculture has 
over capture production. 


        """)
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

We've already established that fish and other aquatic foods (blue foods) are an effective way of reaching a 
sustainable diet. As the graph shows GHG emissions, as well as other environmental stressors, of most blue food 
groups, compare favourably to industrial chicken production, which typically has lower stressors than other livestock 
as we've seen in a previous figure. However, this holds for both aquaculture captures as well as capture fisheries. 
Although generally farmed fish produce a lower or equal average emission than their captured counterpart. 

Most of the emissions of aquaculture result from growing fish food, whereas in the capture fisheries fuel causes the 
most emission. For fed systems, 87% of N and 94% of P occur on food farms. This also means that non-fed groups such 
as seaweeds and bivalve remove more N and P than is emitted during production 
[[6]](https://www.nature.com/articles/s41586-021-03889-2). 

However, since aquaculture uses the land for both the fish and food farms, this creates trade-offs with alternate 
uses, including the production of other foods. And since the availability and access to freshwater increasingly 
constraints the agriculture industry, this creates a downside to fed systems where freshwater is largely used in feed 
production, whereas capture fisheries and unfed systems require little freshwater. 

As it turns out although farmed fish does not appear to have a major environmental benefit, compared to captured 
fish, at the moment it is also safe to say that the industry has not nearly reached its full potential. It's still a 
young and rapidly growing sector with many promising technologies and policies to improve its efficiency. Where the 
main problem to tackle while expanding is making sure new inventions are not beyond the reach of the many small 
producers. 
 
   """),
        dcc.Graph(id='aquaculture-emissions-plot',
                  figure=plot_aquaculture_emissions(df_aqua_emissions))
    ]),

    html.H2('Conclusion',
            className='title-medium',
            id='conclusion'),

    dcc.Markdown(
        className='text-box',
        children=
        """
We have shown that the global interest in fish and seafood follows a positive trend of 0.12 kg/capita/year which
leads to an increased environmental impact by the fishing industry, more so than ever before. In relation to this
we have also shown that fish are getting overexploited by 35% and is still on the rise.

We see that there is a strong correlation between how much a
country has of GDP per capita versus how much seafood they consume per capita. Meaning that richer countries will
eat more fish and seafood. 

Moreover, we've discussed the impact of fish and seafood with respect to other protein sources such as Beef and 
Lamb & goat. Here we found that it is a high-protein and low-impact protein source and thus suitable for a 
sustainable future, if farmed correctly.

By focusing our story on Norway and China, we have clearly highlighted the best and worst practices in the goal of 
achieving a sustainable fishing culture. The way that Norway uses primarily purse seine methods and China uses
bottom trawling shows that the two countries differ significantly in terms of sustainable fishing methods, with 
China being a culprit of poor fishing methods.

However, we also show that China is better at adopting aquaculture instead of capturing wild-fish. Meaning less 
damage to the oceans. But this solution is not perfect either, as it suffers from its own problems such as how to
supply the farmed fish with food. Usually they are fed with wild-caught fish.

Finally, we cover the emissions from aquaculture. We found that it in general is a decently sustainable source in terms 
of GHG emissions. Especially for Seaweed and Bivalves that can be used as "filters" since they remove more GHG than
they produce.

        """
    ),

    html.H2('References',
            className='title-medium',
            id='references',
            style={'marginBottom': 0}),

    dcc.Markdown(
        """
        
[1] Nestle, M., Wing, R., Birch, L., DiSogra, L., Drewnowski, A., Middleton, S., ... & Economos, C. (1998). Behavioral and social influences on food choice.

[2] Naylor, R. L., Kishore, A., Sumaila, U. R., Issifu, I., Hunter, B. P., Belton, B., ... & Crona, B. (2021). Blue food demand across geographic and temporal scales. Nature communications, 12(1), 1-14.

[3] Tacon, A. G. J., Nambiar, K. P. P., & Singh, T. (1997). Feeding tomorrow's fish: the Asian perspective.

[4] Naylor, R. L., Goldburg, R. J., Primavera, J. H., Kautsky, N., Beveridge, M., Clay, J., ... & Troell, M. (2000). Effect of aquaculture on world fish supplies. Nature, 405(6790), 1017-1024.

[5] Eurofish, international organisation for the development of fisheries and aquaculture in Europa. (2022, January 20). Overview of the Norwegian fisheries and aquaculture sector. Retrieved May 14, 2022, from https://eurofish.dk/member-countries/norway/#:~:text=Norway%20is%20the%20world's%20leading,major%20importance%20in%20the%20country.

[6] Gephart, J. A., Henriksson, P. J., Parker, R. W., Shepon, A., Gorospe, K. D., Bergman, K., ... & Troell, M. (2021). Environmental performance of blue foods. Nature, 597(7876), 360-365.

[7] Craze, M (2021, May 17). Seafood’s newfound retail popularity has a permanent feel to it. Global Seafood Alliance. Retrieved May 14, 2022, from https://www.globalseafood.org/advocate/seafoods-newfound-retail-popularity-has-a-permanent-feel-to-it/ 

[8] FAO. 2012. State of the World’s Fisheries and Aquaculture 2012. Rome, Italy: FAO.

[9] Hannah ritchie, & Max roser. (2021, June). Environmental Impacts of Food Production. https://ourworldindata.org/environmental-impacts-of-food

[10] The Environmental Impact of Food. (n.d.). Sustainable Fisheries. https://sustainablefisheries-uw.org/seafood-101/cost-of-food/

[11] Seafood Nutrition Overview. (n.d.). SEAFOOD HEALTH FACTS. https://www.seafoodhealthfacts.org/nutrition/seafood-nutrition-overview/

[12] Hannah ritchie, & Max roser. (2021, October). Fish and Overfishing. https://ourworldindata.org/fish-and-overfishing
        """
    ),

])

if __name__ == '__main__':
    app.run_server(debug=True)

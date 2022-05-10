import pandas as pd
from pathlib import Path

root = Path(__file__).parent.parent

def group_by_elements(df, df_population, elements, year):
    country_code_map, country_code_to_country = get_population_maps()

    df_production = df.query(f'Year == {year}').groupby(['Country Code', 'Element']).sum()['Value']
    df_production = df_production.reset_index().query(f'Element in {elements}').groupby(
        'Country Code').sum().reset_index()
    df_production = pd.merge(df_population[['Country Code', f'{year}']], df_production, on='Country Code').rename(
        {f'{year}': 'Population'}, axis=1)
    df_production[f'value_pr_capita_{year}'] = df_production.Value / df_production.Population * 1000
    df_production['Country'] = df_production.apply(lambda x: country_code_to_country[x['Country Code']], axis=1)
    df_production = df_production.set_index('Country')[['Country Code', 'Value', f'value_pr_capita_{year}']]
    return df_production


def get_population_maps():
    """ Population from 2017 """
    country_code_map = pd.read_csv(root / 'data/country_code_map.csv')[['Country', 'Alpha-3 code']]
    country_code_map['Alpha-3 code'] = country_code_map['Alpha-3 code'].apply(lambda x: x.split('"')[1])
    country_code_map = country_code_map.set_index('Country').to_dict(orient='index')
    country_code_to_country = {value['Alpha-3 code']: key for key, value in country_code_map.items()}
    return country_code_map, country_code_to_country


def add_population(df):
    df_population = get_population()
    country_code_map, country_code_to_country = get_population_maps()

    if 'Country Code' not in df.columns:
        df['Country Code'] = df.apply(lambda x: country_code_map[x['Area']]['Alpha-3 code'], axis=1)

    melted = pd.melt(df_population, id_vars=['Country Name', 'Country Code'], value_vars=df_population.columns[2:],
                     var_name='Year',
                     value_name='population')
    melted.Year = melted.Year.astype(int)
    df = pd.merge(melted, df, on=['Country Code', 'Year'])
    return df


def get_population():
    return pd.read_csv(root / 'data/population_total.csv')


def get_industry_data():
    df = pd.read_csv(root / 'data/FAOSTAT_country_supply_production_import_export.csv')
    df.loc[df['Area'] == "China, mainland", 'Area'] = 'China'
    df.loc[df['Area'] == 'China, Hong Kong SAR', 'Area'] = 'China'
    df.loc[df['Area'] == 'China, Macao SAR', 'Area'] = 'China'
    df.loc[df['Area'] == "China, Taiwan Province of", 'Area'] = 'Taiwan'
    df.loc[df['Area'] == "C?te d'Ivoire", 'Area'] = "Côte d'Ivoire"
    df.loc[df['Area'] == "Netherlands Antilles (former)", 'Area'] = "Netherlands"
    df.loc[df['Area'] == 'Bolivia (Plurinational State of)', 'Area'] = "Bolivia"
    df.loc[df['Area'] == 'Cabo Verde', 'Area'] = "Cape Verde"
    df.loc[df['Area'] == 'Czechia', 'Area'] = "Czech Republic"
    df.loc[df['Area'] == "Democratic People's Republic of Korea", 'Area'] = "South Korea"
    df.loc[df['Area'] == 'Democratic Republic of the Congo', 'Area'] = "Congo"
    df.loc[df['Area'] == 'Eswatini', 'Area'] = "Swaziland"
    df.loc[df['Area'] == 'Iran (Islamic Republic of)', 'Area'] = "Iran, Islamic Republic of"
    df.loc[df['Area'] == 'North Macedonia', 'Area'] = "Macedonia, the former Yugoslav Republic of"
    df.loc[df['Area'] == 'Republic of Korea', 'Area'] = "Korea, Republic of"
    df.loc[df['Area'] == 'United Kingdom of Great Britain and Northern Ireland', 'Area'] = "United Kingdom"
    df.loc[df['Area'] == 'Republic of Moldova', 'Area'] = "Moldova, Republic of"
    df.loc[df['Area'] == 'United Republic of Tanzania', 'Area'] = "Tanzania, United Republic of"
    df.loc[df['Area'] == 'United States of America', 'Area'] = 'United States'
    df.loc[df['Area'] == 'Venezuela (Bolivarian Republic of)', 'Area'] = 'Venezuela, Bolivarian Republic of'

    df = add_population(df)
    return df


def get_consumption():
    df = pd.read_csv(root / "data/fish-and-seafood-consumption-per-capita.csv")

    df = df.rename({'Fish, Seafood- Food supply quantity (kg/capita/yr) (FAO, 2020)': 'consumption',
                    'Entity': 'country'}, axis=1)

    return df


def get_sustainability():
    df = pd.read_csv(root / 'data/fish-stocks-within-sustainable-levels.csv')
    df = df.rename({
        'Share of fish stocks within biologically sustainable levels (FAO, 2020)': 'sustainable',
        'Share of fish stocks that are overexploited': 'overexploited'
    }, axis=1)
    return df


def get_fishing_types():
    fish_catch_methods = pd.read_csv(root / 'data/fish-catch-gear-type.csv')
    fcm = fish_catch_methods[((fish_catch_methods["Entity"] == 'China') | (fish_catch_methods["Entity"] == 'Norway'))]
    fcm = fcm.fillna(0)
    fcm['gear'] = fcm['other_gear'] + fcm['unknown_gear']
    fcm = fcm.drop(columns=['Code', 'unknown_gear', 'other_gear'])
    fcm = fcm.sort_values(by=['Year'])
    fcm = fcm.set_index('Year')
    return fcm


def get_gdp():
    df = pd.read_csv(root / 'data/country_gdp.csv')
    df = pd.melt(df, ['Country Name', 'Country Code'], df.columns[4:(len(df.columns) - 1)],
                 value_name='gdp', var_name='Year')
    df['Year'] = df.Year.astype(int)
    df = add_population(df)
    df = df.drop('Country Name_x', axis=1)
    df = df.rename({'Country Name_y': 'Country Name'}, axis=1)
    df['gdp_pr_capita'] = df.gdp / df.population
    return df

def get_protein():
    df = pd.read_csv('data/animal-protein-consumption.csv')
    protein = df[((df["Entity"] == 'China') | (df["Entity"] == 'Norway'))]

    protein = protein[protein["Year"] == 2017]
    protein = protein.drop(columns=['Code', 'Year', 'Other meat'])
    protein = protein.set_index('Entity')
    return protein


#########################################################

################# Enter Values Here #####################

#########################################################
data_name = ["new", "new1", "new2"]
draw_states = ["ny", "nj", "ct"]
html_name = "new"
#########################################################


input_data = ["_data/_{}_clean.csv".format(dataname) for dataname in data_name]
output_html = "_charts/_{}_analysis_by_map.html".format(html_name)

print("\n ** loading data: {}".format(input_data))

import pandas as pd
from bokeh.io import show
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LogColorMapper
)
from bokeh.palettes import Viridis6 as palette
from bokeh.plotting import figure, output_file
from bokeh.sampledata.us_counties import data as counties

df = pd.DataFrame()
for data in input_data:
    df = df.append(pd.read_csv(data))
df = df.drop_duplicates()
df.city = df.city.apply(lambda x: x.lower())

zip_codes = pd.read_csv("zip_code_database.csv", encoding='latin-1')
draw_states_upper = [state.upper() for state in draw_states]
zip_codes = zip_codes[zip_codes.state.isin(draw_states_upper)]

df = df.merge(zip_codes, left_on=["city", 'state'], right_on=["city", 'state'], how="left").drop_duplicates().dropna()
df["below_market"] = df.price - df.market_price
df.head()

df = df.groupby(['county','state']).mean()
df = df.reset_index()

counties = {
    code: county for code, county in counties.items() if county["state"] in draw_states
}

map_df = pd.DataFrame(columns=('county','temp'))
map_df.county = [county['name'] for county in counties.values()]
map_df = map_df.merge(df, on='county', how='left')

print("\n ** generating new analysis...")

palette.reverse()

county_xs = [county["lons"] for county in counties.values()]
county_ys = [county["lats"] for county in counties.values()]
county_names = [county['name'] for county in counties.values()]
price = map_df.price

color_mapper = LogColorMapper(palette=palette)

source = ColumnDataSource(data=dict(
    x=county_xs,
    y=county_ys,
    name=county_names,
    average_price=map_df.price/1000,
    average_mileage=map_df.mileage/1000,
    average_year=map_df.year,
    average_dealer_rating=map_df.dealer_rating,
    average_market_price=map_df.market_price/1000,
    average_below_market=map_df.below_market/1000
))

TOOLS = "pan,wheel_zoom,box_zoom,reset,hover,save"

p = figure(
    title="Used Car Market Around NY", tools=TOOLS,
    x_axis_location=None, y_axis_location=None
)
p.grid.grid_line_color = None

p.patches('x', 'y', source=source,
          fill_color={'field': 'average_price', 'transform': color_mapper},
          fill_alpha=0.7, line_color="white", line_width=0.5)

hover = p.select_one(HoverTool)
hover.point_policy = "follow_mouse"
hover.tooltips = [
    ("Name", "@name"),
    ('Average Year', '@average_year{int}'),
    ('Average Mileage', '@average_mileage{1.1} mi.'),
    ('Average Rating', '@average_dealer_rating{1.1} /5'),
    ("Average Price", "@average_price{1.1} K"),
    ('Average Market Price', '@average_market_price{1.1} K'),
    ('Average Below Market', '@average_below_market{1.1} K')
    #("(Long, Lat)", "($x, $y)"),
]

print("\n ** new analysis added: {}".format(output_html))

output_file(output_html)
show(p)
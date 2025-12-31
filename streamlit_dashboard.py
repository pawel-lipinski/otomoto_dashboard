# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 17:52:11 2022

@author: Pablo
"""


import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development
import pydeck as pdk # interactive data visualization
import os;

st.set_page_config(
    page_title="Otomoto.pl dashboard - prepared by Pawel Lipinski",
    layout="wide")



print(os.getcwd()) 
#fields=['lon','lat']

#@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv("otomoto_plain_data.csv", low_memory=False)

df=get_data()

df["model_count"]=df.groupby(["brand","model", "country"]).power.transform('count')
df_map=get_data()



st.title("Otomoto.pl Dashboard (as of December 10, 2025)")


df.sort_values(["brand","model"], inplace=True)

col1, col2, col3 = st.columns(3)

# --- 1. BRAND SELECTION ---
# Create list with "All" at the start
brand_options = ["All"] + sorted(pd.unique(df["brand"]).astype(str).tolist())
otomoto_brand = col1.selectbox("Select Brand to Display:", brand_options)

# Filter dataframe immediately so the Model dropdown only shows relevant models
if otomoto_brand != "All":
    df = df[df.brand == otomoto_brand]

# --- 2. MODEL SELECTION ---
# Options are now based on the ALREADY filtered 'df'
model_options = ["All"] + sorted(pd.unique(df["model"]).astype(str).tolist())
otomoto_model = col2.selectbox("Select Model:", model_options)

if otomoto_model != "All":
    df = df[df.model == otomoto_model]

# --- 3. CONDITION SELECTION ---
condition_options = ["All"] + sorted(pd.unique(df["condition"]).astype(str).tolist())
otomoto_condition = col3.selectbox("Select Vehicle Condition:", condition_options)

if otomoto_condition != "All":
    df = df[df.condition == otomoto_condition]



chart_col1, chart_col2 = st.columns(2)

  
with chart_col1:
    # ... keep your existing px.histogram line ...
    chart1 = px.histogram(data_frame=df, title="Car Mileage Distribution", 
                          labels={"mileage": "Mileage"}, marginal="box", 
                          x="mileage", nbins=60, width=800, height=500)
    
    # UPDATE THIS BLOCK
    chart1.update_layout(
        xaxis_title="Mileage in km", 
        plot_bgcolor='#2d3035', 
        paper_bgcolor='#2d3035',
        title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
        font=dict(color='#8a8d93'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        bargap=0.2  # <--- ADD THIS (0.2 means 20% gap)
    )
    
    chart1.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart1)
    
    
with chart_col2:
    
    chart2 = px.density_heatmap(
        data_frame=df, y="price", x="power", width=800, height=500, template="seaborn", title="Heatmap: Price vs. Power"
    )
    chart2.update_layout(xaxis_title='Power',
                  yaxis_title='Price PLN')
    st.write(chart2)
    
with chart_col1:
    # Logic to adjust bins dynamically based on data size
    current_nbins = min(len(df), 30) if len(df) > 5 else 5

    chart5 = px.histogram(
        data_frame=df, 
        x="price", 
        marginal="box", 
        nbins=current_nbins, # <--- Dynamic bins
        width=800, 
        height=500, 
        color_discrete_sequence=["darkblue"], 
        title="Histogram - Price"
    )
    
    chart5.update_layout(
        xaxis_title='Price PLN', 
        plot_bgcolor='#2d3035', 
        paper_bgcolor='#2d3035',
        title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
        font=dict(color='#8a8d93'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        bargap=0.2  # <--- Adds the gap between bars
    )
    
    chart5.update_traces(
        marker_color='rgb(171,220,245)', 
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1.5, 
        opacity=0.8
    )
    
    st.write(chart5)


with chart_col2:
    
    # --- FIX START ---
    # Create a copy so we don't mess up other charts
    df_scatter = df.copy()
    
    # Replace -1 (missing power) with 1 so Plotly doesn't crash.
    # These cars will appear as very small dots.
    df_scatter.loc[df_scatter['power'] <= 0, 'power'] = 1
    # --- FIX END ---

    chart4 = px.scatter(
        data_frame=df_scatter, # <--- IMPORTANT: Use the new df_scatter here
        y="price", 
        x="mileage", 
        width=800, 
        height=500, 
        color="model", 
        size="power", 
        size_max=10, 
        template="ggplot2", 
        title="Heatmap - Price vs. Mileage"
    )
    
    chart4.update_layout(xaxis_title='Mileage in km',
                  yaxis_title='Price PLN')
    st.write(chart4)
 

    
with chart_col2:
    # Logic to adjust bins dynamically based on data size
    current_nbins = min(len(df), 30) if len(df) > 5 else 5

    # Renamed to 'chart_year' to avoid conflict with the Price chart (which was also chart5)
    chart_year = px.histogram(
        data_frame=df, 
        x="year", 
        marginal="box", 
        nbins=current_nbins, 
        width=800, 
        height=500, 
        color_discrete_sequence=["darkblue"], 
        title="Histogram - Year of Manufacture"
    )
    
    chart_year.update_layout(
        xaxis_title='Year of Manufacture', 
        plot_bgcolor='#2d3035', 
        paper_bgcolor='#2d3035',
        title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
        font=dict(color='#8a8d93'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        bargap=0.2  # <--- Adds the gap between bars
    )
    
    chart_year.update_traces(
        marker_color='rgb(171,220,245)', 
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1.5, 
        opacity=0.8
    )
    
    st.write(chart_year)


with chart_col1:
    # Dynamic bins logic
    current_nbins = min(len(df), 60) if len(df) > 5 else 5

    chart6 = px.histogram(
        data_frame=df, 
        x="power", 
        marginal="box", 
        nbins=current_nbins, 
        width=800, 
        height=500, 
        color_discrete_sequence=["darkblue"], 
        title="Histogram - Power"
    )
    
    chart6.update_layout(
        xaxis_title='Power HP', 
        plot_bgcolor='#2d3035', 
        paper_bgcolor='#2d3035',
        title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
        font=dict(color='#8a8d93'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        bargap=0.2  # <--- Gap
    )
    
    chart6.update_traces(
        marker_color='rgb(171,220,245)', 
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1.5, 
        opacity=0.8
    )
    
    st.write(chart6)
    
    
with chart_col2:
    
    chart7 = px.histogram(data_frame=df, x="fuel", text_auto=True, nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"], title="Histogram - Fuel")
    chart7.update_layout(xaxis_title='Fuel',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart7.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart7)
    


    
    
with chart_col1:
    
    chart8 = px.histogram(data_frame=df, x="car_type",text_auto=True, nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"], title="Histogram - Car Type")
    chart8.update_layout(xaxis_title='Car Type',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart8.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart8)

with chart_col2:
    
    chart9 = px.histogram(data_frame=df, x="color",text_auto=True, nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"], title="Histogram - Color")
    chart9.update_layout(xaxis_title='Color',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart9.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart9)
    
  
with chart_col2:
    
    chart11 = px.histogram(data_frame=df, x="country",text_auto=True, nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"], title="Histogram - Country of Origin")
    chart11.update_layout(xaxis_title='Country of Origin',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart11.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart11)

    
with chart_col1:
    
    chart12 = px.histogram(data_frame=df, x="district", text_auto=True,nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"], title="Histogram - Province")
    chart12.update_layout(xaxis_title='Province',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart12.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart12)

    
with chart_col2:
    
    chart13 = px.histogram(data_frame=df, x="drive", text_auto=True,nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"], title="Histogram - Drive Type")
    chart13.update_layout(xaxis_title='Drive Type',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart13.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart13)
    
with chart_col1:
    
    chart14 = px.histogram(data_frame=df, x="from_who", text_auto=True,nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"], title="Histogram - Seller Type (Who is selling)")
    chart14.update_layout(xaxis_title='Seller Type (Who is selling)',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart14.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart14)
    

with chart_col2:
    # UWAGA: Usunąłem obliczanie 'current_nbins' dla tego konkretnego wykresu.
    # Przy małej liczbie unikalnych wartości (drzwi to zazwyczaj 2,3,4,5) 
    # wymuszanie dużej liczby binów psuje wykres.

    chart15 = px.histogram(
        data_frame=df, 
        x="doors",
        text_auto=True, 
        # nbins=current_nbins, <--- USUNIĘTE: Pozwalamy Plotly zgrupować liczby całkowite
        width=800, 
        height=500, 
        color_discrete_sequence=["darkblue"], 
        title="Histogram - Number of Doors"
    )
    
    chart15.update_layout(
        xaxis_title='Number of Doors',  
        xaxis=dict(dtick=1), # Wymusza liczby całkowite na osi X
        plot_bgcolor='#2d3035', 
        paper_bgcolor='#2d3035',
        title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
        font=dict(color='#8a8d93'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        bargap=0.05  # <--- ZMIANA: Mniejszy odstęp między słupkami (wcześniej 0.2)
    )
    
    chart15.update_traces(
        marker_color='rgb(171,220,245)', 
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1.5, 
        opacity=0.8
    )
    
    st.write(chart15)


with chart_col1:
    
    chart16 = px.histogram(data_frame=df, x="seats", text_auto=True,nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"], title="Histogram - Number of Seats")
    chart16.update_layout(xaxis_title='Number of Seats',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart16.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart16)
    



with chart_col2:
    
    chart17 = px.histogram(data_frame=df, x="no_crash",text_auto=True, nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"], title="Histogram - Accident-Free (No Crash)")
    chart17.update_layout(xaxis_title='Accident-Free (No Crash)',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart17.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart17)
    

    
with chart_col1:
    
    chart18 = px.histogram(data_frame=df, x="registered",text_auto=True, nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"], title="Histogram - Registered")
    chart18.update_layout(xaxis_title='Registered',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart18.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart18)
    
with chart_col1:
    # Logic to adjust bins dynamically based on data size
    current_nbins = min(len(df), 60) if len(df) > 5 else 5

    chart19 = px.histogram(
        data_frame=df, 
        x="seller_since",
        text_auto=True, 
        nbins=current_nbins, # <--- Dynamic bins
        width=800, 
        height=500, 
        color_discrete_sequence=["darkblue"], 
        title="Histogram - Seller's Otomoto Account Creation Year"
    )
    
    chart19.update_layout(
        xaxis_title="Seller's Otomoto Account Creation Year",  
        plot_bgcolor='#2d3035', 
        paper_bgcolor='#2d3035',
        title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
        font=dict(color='#8a8d93'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        bargap=0.2  # <--- Adds the gap between bars
    )
    
    chart19.update_traces(
        marker_color='rgb(171,220,245)', 
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1.5, 
        opacity=0.8
    )
    
    st.write(chart19)

with chart_col1:
    
    chart20 = px.histogram(data_frame=df, x="transmission",text_auto=True, nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"], title="Histogram - Transmission")
    chart20.update_layout(xaxis_title='Transmission',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color="#a5a7ab", family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart20.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart20)



# Reset map data to ensure we start fresh
df_map = get_data()

# Apply the same logic as the top filters
if otomoto_brand != "All":
    df_map = df_map[df_map.brand == otomoto_brand]

if otomoto_model != "All":
    df_map = df_map[df_map.model == otomoto_model]

# --- FIX START ---
# Force 'lat' and 'lon' to be numeric. 
# This converts "Not stated" (and any other bad text) into NaN (empty)
df_map['lat'] = pd.to_numeric(df_map['lat'], errors='coerce')
df_map['lon'] = pd.to_numeric(df_map['lon'], errors='coerce')

# Drop rows where coordinates are missing (NaN)
df_map = df_map.dropna(subset=['lat', 'lon'])
# --- FIX END ---

# Prepare for PyDeck
df_map = df_map[['lon', 'lat']]


st.markdown("Distribution of Listings by Location")
st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v10',
     initial_view_state=pdk.ViewState(
         latitude=52.25,
         longitude=21.0,
         zoom=6,
         api_keys="pk.eyJ1IjoicGF3ZWxsaXBpbnNraSIsImEiOiJjbDU4bHp6ZTIwMWgwM2tqemRod3U4dGowIn0.QvUNJOqSfgwjs2E3P4O6Wg",
         pitch=10,
         
     ),
     layers=[
         pdk.Layer(
            'HexagonLayer',
            data=df_map,
            get_position='[lon, lat]',
            auto_highlight=True,
            elevation_scale=100,
            pickable=True,
            elevation_range=[0, 2000],
            extruded=True,
            coverage=1
            # radius=300,
            # elevation_scale=60,
            # elevation_range=[0, 1000],
            # pickable=True,
            # extruded=True,
         ),
         pdk.Layer(
             'ScatterplotLayer',
             data=df_map,
             get_position='[lon, lat]',
             get_color='[200, 30, 0, 160]',
             get_radius=2000,
             pickable=True,
         ),
     ],
 ))






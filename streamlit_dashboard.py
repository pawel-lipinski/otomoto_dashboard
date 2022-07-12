# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 17:52:11 2022

@author: Pablo
"""


import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development
import pydeck as pdk # interactive data visualization


st.set_page_config(
    page_title="Otomoto.pl dashboard",
    layout="wide")




#fields=['lon','lat']

@st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_csv("otomoto_plain_data.csv")

df=get_data()

df["model_count"]=df.groupby(["brand","model", "country"]).power.transform('count')
df_map=get_data()



st.title("Otomoto.pl dashboard (stan na 5 lipca 2022)")


df.sort_values(["brand","model"], inplace=True)



col1, col2, col3 = st.columns(3)

otomoto_brand = col1.selectbox("Wybierz model do wyświetlenia:", pd.unique(df["brand"]))


otomoto_condition = col3.selectbox("Wybierz stan samochodu:", pd.unique(df["condition"]))



df = df[(df.brand==otomoto_brand) & (df.condition==otomoto_condition)]


otomoto_model = col2.selectbox("Wybierz model:", pd.unique(df["model"]))

df = df[(df.brand==otomoto_brand) & (df.condition==otomoto_condition) & (df.model==otomoto_model)]

chart_col1, chart_col2 = st.columns(2)

  
with chart_col1:
    st.markdown("Histogram - przebieg w km")
    chart1 = px.histogram(data_frame=df, labels={"przebieg", "przebieg"}, marginal="box", x="mileage", nbins=60, width=800, height=500)
    chart1.update_layout(xaxis_title="Przebieg w km",  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart1.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart1)
    
    
with chart_col2:
    st.markdown("Heatmapa: moc vs cena")
    chart2 = px.density_heatmap(
        data_frame=df, y="price", x="power", width=800, height=500, template="seaborn"
    )
    chart2.update_layout(xaxis_title='Cena',
                  yaxis_title='Moc')
    st.write(chart2)
    
    
with chart_col1:
    st.markdown("Histogram - model")
    chart3 = px.histogram(data_frame=df, x="model", color="fuel", width=800, height=500, color_discrete_sequence=['#DB6574', '#03DAC5', '#0384da', '#a5a7ab', '#d870db', '#dbcf70'])
    chart3.update_layout(xaxis_title="Model",  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart3.update_traces(marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart3)

with chart_col2:
    st.markdown("Heatmapa: cena vs przebieg")
    chart4 = px.scatter(
        data_frame=df, y="mileage", x="price", width=800, height=500, color="model", size="power", size_max=10, template="ggplot2"
    )
    chart4.update_layout(xaxis_title='Przebieg w km',
                  yaxis_title='Cena')
    st.write(chart4)
 

    
with chart_col2:
    st.markdown("Histogram - rok produkcji")
    chart5 = px.histogram(data_frame=df, x="year",marginal="box", nbins=30, width=800, height=500, color_discrete_sequence=["darkblue"])
    chart5.update_layout(xaxis_title='Rok produkcji',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart5.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart5)

with chart_col1:
    st.markdown("Histogram - moc")
    chart6 = px.histogram(data_frame=df, x="power", marginal="box", nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"])
    chart6.update_layout(xaxis_title='Moc',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart6.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart6)   
    
    
with chart_col2:
    st.markdown("Histogram - paliwo")
    chart7 = px.histogram(data_frame=df, x="fuel", text_auto=True, nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"])
    chart7.update_layout(xaxis_title='Paliwo',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart7.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart7)
    


    
    
with chart_col1:
    st.markdown("Histogram - typ samochodu")
    chart8 = px.histogram(data_frame=df, x="car_type",text_auto=True, nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"])
    chart8.update_layout(xaxis_title='Typ samochodu',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart8.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart8)

with chart_col2:
    st.markdown("Histogram - kolor")
    chart9 = px.histogram(data_frame=df, x="color",text_auto=True, nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"])
    chart9.update_layout(xaxis_title='Kolor',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart9.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart9)
    
with chart_col1:
    st.markdown("Histogram - typ lakieru")
    chart10 = px.histogram(data_frame=df, x="colour_type",text_auto=True, nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"])
    chart10.update_layout(xaxis_title='Typ lakieru',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart10.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart10)
    
with chart_col2:
    st.markdown("Histogram - kraj pochodzenia")
    chart11 = px.histogram(data_frame=df, x="country",text_auto=True, nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"])
    chart11.update_layout(xaxis_title='Kraj pochodzenia',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart11.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart11)

    
with chart_col1:
    st.markdown("Histogram - województwo")
    chart12 = px.histogram(data_frame=df, x="district", text_auto=True,nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"])
    chart12.update_layout(xaxis_title='Województwo',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart12.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart12)

    
with chart_col2:
    st.markdown("Histogram - napęd")
    chart13 = px.histogram(data_frame=df, x="drive", text_auto=True,nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"])
    chart13.update_layout(xaxis_title='Napęd',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart13.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart13)
    
with chart_col1:
    st.markdown("Histogram - kto sprzedaje")
    chart14 = px.histogram(data_frame=df, x="from_who", text_auto=True,nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"])
    chart14.update_layout(xaxis_title='Kto sprzedaje',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart14.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart14)
    

with chart_col2:
    st.markdown("Histogram - liczba drzwi")
    chart15 = px.histogram(data_frame=df, x="doors",text_auto=True, nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"])
    chart15.update_layout(xaxis_title='Liczba drzwi',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart15.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart15)
    
with chart_col1:
    st.markdown("Histogram - liczba siedzeń")
    chart16 = px.histogram(data_frame=df, x="seats", text_auto=True,nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"])
    chart16.update_layout(xaxis_title='Liczba siedzeń',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart16.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart16)
    



with chart_col2:
    st.markdown("Histogram - bezwypadkowy")
    chart17 = px.histogram(data_frame=df, x="no_crash",text_auto=True, nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"])
    chart17.update_layout(xaxis_title='Bezwypadkowy',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart17.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart17)
    

    
with chart_col1:
    st.markdown("Histogram - zarejestrowany")
    chart18 = px.histogram(data_frame=df, x="registered",text_auto=True, nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"])
    chart18.update_layout(xaxis_title='Zarejestrowany',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart18.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart18)
    
with chart_col2:
    st.markdown("Histogram - rok zalozenia konta sprzedawcy na otomoto.pl")
    chart19 = px.histogram(data_frame=df, x="seller_since",text_auto=True, nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"])
    chart19.update_layout(xaxis_title='Rok założenia konta na otomoto.pl',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart19.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart19)

with chart_col1:
    st.markdown("Histogram - skrzynia biegow")
    chart20 = px.histogram(data_frame=df, x="transmission",text_auto=True, nbins=60, width=800, height=500, color_discrete_sequence=["darkblue"])
    chart20.update_layout(xaxis_title='Skrzynia biegów',  plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        font=dict(color='#8a8d93'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    chart20.update_traces(marker_color='rgb(171,220,245)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)
    st.write(chart20)



df_map.sort_values(by="model", inplace=True)

df_map = df_map[(df_map.brand==otomoto_brand)]


df_map = df_map[(df_map.brand==otomoto_brand) & (df_map.model==otomoto_model)]

df_model_data = df_map
df_model_data.sort_values(["year"], inplace=True)

df_map = df_map[['lon', 'lat']].copy()

st.markdown("Rozkład ogłoszeń wg miejsca")
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
             get_radius=4000,
             pickable=True,
         ),
     ],
 ))






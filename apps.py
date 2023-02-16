import os
import re
import json
import requests
import pandas as pd
import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import folium
import requests
import base64
from streamlit_option_menu import option_menu
from PIL import Image
import streamlit as st
from streamlit_folium import st_folium
from matplotlib.pyplot import plot
from folium.plugins import FastMarkerCluster
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap
from sklearn.preprocessing  import LabelEncoder
import streamlit.components.v1 as html 
from streamlit_lottie import st_lottie
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
def load_data():
    # code to load your data into a DataFrame called "data"
    data = pd.read_csv('complete_travel_destination_data.csv')
    return data

data = load_data()

# #css
with open('styles.css') as source_des:
    st.markdown(f"<style>{source_des.read()}</style>",unsafe_allow_html=True)

with st.sidebar:
    choose = option_menu("Main Menu", ["Kelompok","Disctrict", "Types","Grade", "Visual Map", "Pick Destination","Top Tourist"],
                        icons=['','', '','','',''],
                        menu_icon="list", default_index=0,
                        styles={
        "container": {"padding": "80px", "border-radius": "-20px", "background-color": "black;"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#02ab21"},
        "nav-link-selected": {"background-color": "#02ab21"},
    })

@st.experimental_memo
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("image.jpg")

page_bg_img = f"""
<style>
[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


if choose == "Kelompok":
    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    lottie_url_hello = "https://assets10.lottiefiles.com/packages/lf20_3vbOcw.json"
    lottie_hello = load_lottieurl(lottie_url_hello)

    st_lottie(lottie_hello,width=500, height=500, key="hello")
    st.markdown('10121107 - Irham Ahmad Musyadad')
    st.markdown('10121123 - Taufikqur Rohman')
    st.markdown('10121114 - Qaisha Fadhil Ahmad')
    st.markdown('10121106 - Muhammad Syihab')
    st.markdown('10121091 - M Ridwan')
    st.markdown('Teknik Informatika - 3')

# Membuat Aplikasi Streamlit

# Buat Destinasi

elif choose == "Disctrict":
    file_data = st.file_uploader("Upload your CSV file", type=["csv"])
    if file_data is not None:
            data = pd.read_csv(file_data, delimiter=",")
            st.dataframe(data)

    st.header("	:round_pushpin: District Destination")

    top_d_type = data[["Address", "District"]].groupby("District").agg(['count'])['Address']['count'].sort_values(ascending=False)
    ax = sns.barplot( x = top_d_type.index, y = top_d_type.values)
    ax.set_xticklabels(labels=top_d_type.index , rotation=45)
    fig = plt.gcf()
    fig.set_size_inches(10, 8, forward=True)
    ax.set_ylabel("Number of Destinations")
    ax.set_xlabel("District")
    ax.set_title("District with most Destinations to visit");

    st.pyplot(fig)
    
# Disrtribution of Destination Types
elif choose == "Types":
    file_data = st.file_uploader("Upload your CSV file", type=["csv"])
    if file_data is not None:
            data = pd.read_csv(file_data, delimiter=",")
            st.dataframe(data)
    st.header("	:cityscape: Disrtribution of Destination Types")

    colors = sns.color_palette('pastel')[1:7]
    dtc_dest = data[["Address", "Type"]].groupby("Type").agg(['count'])['Address']['count']

    fig, ax = plt.subplots(figsize=(15, 10))
    ax.bar(dtc_dest.index, dtc_dest.values, color = colors)
    ax.set_title("Distribution of Destination Types")
    ax.set_xlabel("Type of Destination")
    ax.set_ylabel("Count")

    st.pyplot(fig)

# Disrtribution of Graded Destinations
elif choose == "Grade":
    file_data = st.file_uploader("Upload your CSV file", type=["csv"])
    if file_data is not None:
            data = pd.read_csv(file_data, delimiter=",")
            st.dataframe(data)
    st.header(":classical_building: Disrtribution of Graded Destinations")

    colors = sns.color_palette('pastel')[0:5]
    dstb_grade = data[["Address", "Grade"]].groupby("Grade").agg(['count'])['Address']['count']
    fig, ax = plt.subplots()
    ax.pie(dstb_grade, labels = dstb_grade.index, colors = colors, autopct='%.0f%%')
    fig.set_size_inches(20, 7, forward=True)
    ax.set_title("Distribution of Graded Destinations")
    st.pyplot(fig)

# Visual Map Destinaotion
elif choose == "Visual Map":
    st.header("	:world_map: Visual Map Destination")

    folium_map = folium.Map(location=[7.8731, 80.7718],
                            zoom_start=8,
                            tiles='CartoDB dark_matter',
                            width='100%',
                            height='100%')

    data_map = data[data['Lat'].notna() & data['Lon'].notna() ]

    FastMarkerCluster(data=list(zip(data_map['Lon'].values, data_map['Lat'].values))).add_to(folium_map)
    folium.LayerControl().add_to(folium_map)

    st_folium(folium_map)

# #Modul Untuk Machine Learning

#buat sidebar MAP
elif choose == "Pick Destination":
    st.header("	:earth_asia: Pick Your Destination")

    data = pd.read_csv("complete_travel_destination_data.csv")
    data_filter = data[['Type', 'Name','Lon', 'Lat']]
    data_filter = data_filter.dropna()

    # persiapan buat data ploating
    le = LabelEncoder()
    data_filter.loc[:, 'id_Type'] = le.fit_transform(data_filter['Type'])
    types = data_filter['Type'].unique()

    boulder_coords = [7.8731, 80.7718] # Define the center of the map

    # Membuat map dan trek lokasi
    def create_map(selected_type):
        my_map = folium.Map(location=boulder_coords, tiles = 'Stamen Terrain', zoom_start = 11)
        
        data_selected = data_filter[data_filter['Type'] == selected_type]
        for i in range (0, len(data_selected)):
            koordinat = data_selected.iloc[i, [2,3]].to_list()
            nama = data_selected.iloc[i, [1]].astype(str).to_string()
            if(data_selected.iloc[i,4]==0):
                folium.Marker(koordinat, popup = nama,icon=folium.Icon(color='black')).add_to(my_map)
            elif(data_selected.iloc[i,4]==1):
                folium.Marker(koordinat, popup = nama,icon=folium.Icon(color='pink')).add_to(my_map)
            elif(data_selected.iloc[i,4]==2):
                folium.Marker(koordinat, popup = nama,icon=folium.Icon(color='darkblue')).add_to(my_map)
            elif(data_selected.iloc[i,4]==3):
                folium.Marker(koordinat, popup = nama,icon=folium.Icon(color='green')).add_to(my_map)
            elif(data_selected.iloc[i,4]==4):
                folium.Marker(koordinat, popup = nama,icon=folium.Icon(color='cadetblue')).add_to(my_map)
            elif(data_selected.iloc[i,4]==5):
                folium.Marker(koordinat, popup = nama,icon=folium.Icon(color='gray')).add_to(my_map)
        return my_map

    # Membuat Filter data Type
    def filter_data_by_type(selected_type):
        filtered_data = data_filter[data_filter['Type'] == selected_type]
        return filtered_data

    selected_type = st.sidebar.selectbox("Select Type Destination", types, key='unique_key')
    filtered_data = filter_data_by_type(selected_type)
    st.write(filtered_data)


    st_folium(create_map(selected_type))

elif choose == "Top Tourist":
    st.header(":medal: Most visitors arriving in Sri Lanka on 2020")
    import pandas as pd
    import numpy as np

    data = pd.read_csv('output.csv')
    data_filter = data[['Country', '2020']]
    data_filter = data_filter.dropna()
    data_filter

    data_filter = data_filter.dropna()

    fig, ax = plt.subplots(figsize=(16,8))
    ax.bar(data_filter['Country'], data_filter['2020'], color='orange', alpha=0.5)

    ax.set_title('Total for Country', size=18)
    ax.set_xlabel('\nCountry', size=14)
    ax.set_ylabel('Total\n', size=14)
    ax.tick_params(axis='both', labelsize=14)
    ax.grid(linestyle='--', color='gray', alpha=0.7)
    fig.tight_layout()

    st.pyplot(fig)
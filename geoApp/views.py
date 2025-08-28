from django.shortcuts import render, redirect
import os
import pandas as pd
import geopandas as gpd

# Create your views here.
def geopandas(request):

    MUTATO_FOCSOP_MEGNEV = request.POST.get('MUTATO_FOCSOP_MEGNEV')
    if not MUTATO_FOCSOP_MEGNEV:
        MUTATO_FOCSOP_MEGNEV = "Lakásállomány, -építés, -megszűnés, -árak" 

    MUTATO_MEGNEV = request.POST.get('MUTATO_MEGNEV')
    if not MUTATO_MEGNEV:
        MUTATO_MEGNEV = "1 szobás lakások aránya" 
    
    shp_dir = os.path.join(os.getcwd(), 'static', 'media')
    Hungary_city = gpd.read_file(os.path.join(shp_dir, 'telepules_BP_egesz.shp'))
    Hungary_city = Hungary_city[['NAME', 'geometry']]
    Hungary_city_values = pd.read_csv(os.path.join(shp_dir, 'TIMEA_Varosok_2024.csv'), sep = ";")
    Mutatok = pd.read_csv(os.path.join(shp_dir, 'TIMEA_Mutatok_2024.csv'), sep = ";")
    # Mutatok = pd.read_csv("https://raw.githubusercontent.com/aszilagyi1989/Shiny_CSV/refs/heads/main/TIMEA_Mutatok_2024.csv", sep = ";")

    Hungary_city_values = Hungary_city_values[['NEV', 'VALUE', 'M_KOD']]
    Hungary_city = pd.merge(Hungary_city, Hungary_city_values, how = 'left', left_on = 'NAME', right_on = 'NEV')
    Hungary_city = pd.merge(Hungary_city, Mutatok, how = 'left', left_on = 'M_KOD', right_on = 'MUTATO_KOD')
    Hungary_city = Hungary_city[['NAME', 'VALUE', 'geometry', 'M_KOD', 'MUTATO_FOCSOP_MEGNEV', 'MUTATO_MEGNEV']]

    FOCSOP = Hungary_city['MUTATO_FOCSOP_MEGNEV'].unique()
    FOCSOP = sorted(FOCSOP)
    
    ALCSOP = Hungary_city.loc[Hungary_city['MUTATO_FOCSOP_MEGNEV'] == MUTATO_FOCSOP_MEGNEV, ['MUTATO_MEGNEV']]
    ALCSOP = ALCSOP['MUTATO_MEGNEV'].unique()
    ALCSOP = sorted(ALCSOP)

    Hungary_city = Hungary_city[Hungary_city['MUTATO_MEGNEV'] == MUTATO_MEGNEV] # 'TYWG006' MUTATO_MEGNEV

    m = Hungary_city.explore("VALUE", legend = False) 
    m = m._repr_html_()

    context = {'my_map': m, 'FOCSOP': FOCSOP, 'ALCSOP': ALCSOP}

    return render(request, 'geopandas.html', context)
from django.shortcuts import render, redirect
import os
import pandas as pd
import geopandas as gpd

# Create your views here.
def geopandas(request):

    shp_dir = os.path.join(os.getcwd(), 'static', 'media')
    Hungary_city = gpd.read_file(os.path.join(shp_dir, 'telepules_BP_egesz.shp'))
    Hungary_city = Hungary_city[['NAME', 'geometry']]
    Hungary_city_values = pd.read_csv(os.path.join(shp_dir, 'TIMEA_Varosok_2024.csv'), sep = ";")
    Mutatok = pd.read_csv(os.path.join(shp_dir, 'TIMEA_Mutatok_2024.csv'), sep = ";")

    Hungary_city_values = Hungary_city_values[['NEV', 'VALUE', 'M_KOD']]
    Hungary_city = pd.merge(Hungary_city, Hungary_city_values, how = 'left', left_on = 'NAME', right_on = 'NEV')
    Hungary_city = pd.merge(Hungary_city, Mutatok, how = 'left', left_on = 'M_KOD', right_on = 'MUTATO_KOD')
    Hungary_city = Hungary_city[['NAME', 'VALUE', 'geometry', 'M_KOD', 'MUTATO_FOCSOP_MEGNEV', 'MUTATO_MEGNEV']]
    Hungary_city = Hungary_city[Hungary_city['M_KOD'] == 'TYWG006']

    m = Hungary_city.explore("VALUE", legend = False)
    m = m._repr_html_()
    context = {'my_map': m}

    return render(request, 'geopandas.html', context)
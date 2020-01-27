import pandas as pd
import ast
import json

from geo.helpers import *


data = pd.read_csv('RU.txt', delimiter='\t', names=["geonameid", "name", "asciiname", "alternatenames", "latitude", "longtitude", "feature class",
                                                      "feature code", "country code", "cc2", "admin1 code", "admin2 code", "admin3 code", "admin4 code",
                                                      "population", "elevation", "dem", "timezone", "modification date"],
                                            low_memory=False)

data.fillna("", inplace=True)


def getbygeonameid(geonameid):
    """ Returns city info by its geonameid"""
    try:
        info = data.loc[data['geonameid'] == int(geonameid)]
        d = info.to_dict(orient='records')
    except ValueError:
        d = {}

    j = json.dumps(d, indent=4, separators=(',', ': '), ensure_ascii=False)
    return (j)


def get_city_name_suggestions(city_name, cities):
    """ Returns list of suggested city names """

    contains_name = cities.loc[data['alternatenames'].str.contains(city_name, na=False)]
    suggestions = []
    for c in contains_name['alternatenames']:
        if c[-1] not in suggestions:
            suggestions.append(c[-1])
    return ({f'{city_name} not found. Suggestions': suggestions})
     

def getcities(city1, city2):
    """ 
    Returns all info about two cities by names
        feature class == 'P' defines city 
    """

    if not city1 or not city2:
        return {}

    info1 = data.loc[data['alternatenames'].str.contains(city1, na=False) & 
                    (data['feature class'] =='P')].sort_values(by=['population'], ascending=False)

    info2 = data.loc[data['alternatenames'].str.contains(city2, na=False) & 
                    (data['feature class'] =='P')].sort_values(by=['population'], ascending=False)

    city1_check = check_city(city1, info1)
    city2_check = check_city(city2, info2)

    if not city1_check:
        lst = get_city_name_suggestions(city1, info1)
        j = json.dumps(lst, indent=4, separators=(',', ': '), ensure_ascii=False, default=str)
        return j 
    if not city2_check:
        lst = get_city_name_suggestions(city2, info2)
        j = json.dumps(lst, indent=4, separators=(',', ': '), ensure_ascii=False, default=str)
        return j 

    if len(info1) < 0 or len(info2) < 0:
        return {}
    else:
        city1_info = info1.iloc[0]
        city2_info = info2.iloc[0]

        d1 = city1_info.to_dict()
        d2 = city2_info.to_dict()
    
        lst = []
        lst.append(d1)
        lst.append(d2)

        lst.append(lat_diff(city1_info, city2_info))
        lst.append(tz_diff(city1_info, city2_info))

        j = json.dumps(lst, indent=4, separators=(',', ': '), ensure_ascii=False, default=str)
        return j

def cities_list_info(cities_list):
    """ Returns all info for each city in cities_list """

    results = []
    for city in cities_list:
        info = data.loc[data['alternatenames'].str.contains(city, na=False) & 
                    (data['feature class'] =='P')].sort_values(by=['population'], ascending=False)

        city_check = check_city(city, info)
        
        if not city_check:
            results.append(get_city_name_suggestions(city, info))
            continue

        city1_info = info.iloc[0]
        results.append(city1_info.to_dict())
    
    j = json.dumps(results, indent=4, separators=(',', ': '), ensure_ascii=False, default=str)
    return j

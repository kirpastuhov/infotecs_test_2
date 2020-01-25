import pandas as pd
import ast
import json
from datetime import datetime
from pytz import timezone
from dateutil.relativedelta import relativedelta


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

def check_city(city_name, cities):
    cities['alternatenames'] = cities['alternatenames'].apply(lambda x: x.split(","))
    city_num = 0
    found = -1
    while city_num < len(cities):
        found = check_city_name(city_name, city_num, cities)
        if found >= 0:
            return True
        else:
            city_num += 1
    return False
            
def check_city_name(city_name, city_num, cities):
    """ Checks if inputed city name is the same as the alternate name of column """

    try:
        if (cities.iloc[city_num]['alternatenames'][-1] == city_name) \
        or (cities.iloc[city_num]['alternatenames'][-2] == city_name):
            return city_num
    except IndexError:
        pass
    return -1

def get_city_name_suggestions(city_name, cities):
    """ Returns list of suggested city names """

    contains_name = cities.loc[data['alternatenames'].str.contains(city_name, na=False)]
    suggestions = []
    for c in contains_name['alternatenames']:
        if c[-1] not in suggestions:
            suggestions.append(c[-1])
    return ({'suggestions': suggestions})
     

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
        return(j)
    if not city2_check:
        lst = get_city_name_suggestions(city2, info2)
        j = json.dumps(lst, indent=4, separators=(',', ': '), ensure_ascii=False, default=str)
        return(j)

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
        return(j)


def tz_diff(info1, info2):
    """ Returns the difference in hours between two timezones """

    tz1 = info1['timezone']
    tz2 = info2['timezone']

    utcnow = timezone('utc').localize(datetime.utcnow())
    here = utcnow.astimezone(timezone(tz1)).replace(tzinfo=None)
    there = utcnow.astimezone(timezone(tz2)).replace(tzinfo=None)

    offset = relativedelta(here, there) 
    diff = offset.hours
    if abs(diff) > 12.0:
        if diff < 0.0:
            diff += 24.0
        else:
            diff -= 24.0

    if abs(diff) == 0:
        return {'tz_diff':"Timezones are the same"}
    else:
        return {'tz_diff':f"Time zone difference: {diff}"}


def lat_diff(info1, info2):
    """ Returns northernmost of two cities """

    lat1 = info1['latitude']
    lat2 = info2['latitude']
    if lat1 > lat2:
        return {'north':f"{info1['name']} is located north of {info2['name']}"}
    else:
        return {'north':f"{info2['name']} is located north of {info1['name']}"}

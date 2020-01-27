from datetime import datetime
from pytz import timezone
from dateutil.relativedelta import relativedelta


def check_city(city_name, cities):
    """ Checks for a valid city_name """

    cities["alternatenames"] = cities["alternatenames"].apply(lambda x: x.split(","))
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
        if (cities.iloc[city_num]["alternatenames"][-1] == city_name) \
        or (cities.iloc[city_num]["alternatenames"][-2] == city_name):
            return city_num
    except IndexError:
        pass
    return -1


def tz_diff(info1, info2):
    """ Returns the difference in hours between two timezones """

    tz1 = info1["timezone"]
    tz2 = info2["timezone"]

    utcnow = timezone("utc").localize(datetime.utcnow())
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
        return {"tz_diff":"Timezones are the same"}
    else:
        return {"tz_diff":f"Time zone difference: {diff}"}


def lat_diff(info1, info2):
    """ Returns northernmost of two cities """

    lat1 = info1["latitude"]
    lat2 = info2["latitude"]
    if lat1 > lat2:
        return {"north":f"{info1['name']} is located north of {info2['name']}"}
    else:
        return {"north":f"{info2['name']} is located north of {info1['name']}"}


from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const
from flatlib.aspects import getAspect

# Astrology calculation

import json
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const

PLANETS = [const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN, const.URANUS, const.NEPTUNE, const.PLUTO]
NODES = [const.NORTH_NODE, const.SOUTH_NODE]
CHIRON = 'Chiron'  # Flatlib may not support Chiron by default

ELEMENTS = {
    'FIRE': ['Aries', 'Leo', 'Sagittarius'],
    'EARTH': ['Taurus', 'Virgo', 'Capricorn'],
    'AIR': ['Gemini', 'Libra', 'Aquarius'],
    'WATER': ['Cancer', 'Scorpio', 'Pisces']
}
MODALITIES = {
    'CARDINAL': ['Aries', 'Cancer', 'Libra', 'Capricorn'],
    'FIXED': ['Taurus', 'Leo', 'Scorpio', 'Aquarius'],
    'MUTABLE': ['Gemini', 'Virgo', 'Sagittarius', 'Pisces']
}

def decimal_to_dms_str(value, is_lat=True):
    deg = abs(int(float(value)))
    min_ = int((abs(float(value)) - deg) * 60)
    dir_ = ("N" if float(value) >= 0 else "S") if is_lat else ("E" if float(value) >= 0 else "W")
    if is_lat:
        return f"{deg}{dir_}{min_}"
    else:
        return f"{deg:03d}{dir_}{min_}"

def extract_elements_modalities(signs):
    elem_count = {k: 0 for k in ELEMENTS}
    mod_count = {k: 0 for k in MODALITIES}
    for sign in signs:
        for elem, sign_list in ELEMENTS.items():
            if sign in sign_list:
                elem_count[elem] += 1
        for mod, sign_list in MODALITIES.items():
            if sign in sign_list:
                mod_count[mod] += 1
    return elem_count, mod_count

def calculate_full_chart(date_str, time_str, place_lat, place_lon):
    """
    Returns a dict with full natal chart info: planets, houses, aspects, elements, modalities, nodes, Chiron (if available), etc.
    """
    y, m, d = date_str.split('-')
    flatlib_date = f"{d}/{m}/{y}"
    dt = Datetime(flatlib_date, time_str, '+00:00')
    lat_str = decimal_to_dms_str(place_lat, is_lat=True)
    lon_str = decimal_to_dms_str(place_lon, is_lat=False)
    pos = GeoPos(lat_str, lon_str)
    chart = Chart(dt, pos)

    # Planets
    planets = {}
    planet_signs = []
    for p in PLANETS:
        # Handle missing objects gracefully
        try:
            obj = chart.getObject(p)
            sign = getattr(obj, 'sign', None)
            lon = getattr(obj, 'lon', None)
            speed = getattr(obj, 'speed', None)
        except KeyError:
            sign = None
            lon = None
            speed = None
        planets[p] = {'sign': sign, 'lon': lon, 'speed': speed}
        if sign:
            planet_signs.append(sign)

    # Nodes
    nodes = {}
    for n in NODES:
        # Handle missing nodes gracefully
        try:
            obj = chart.getObject(n)
            sign = getattr(obj, 'sign', None)
            lon = getattr(obj, 'lon', None)
        except KeyError:
            sign = None
            lon = None
        nodes[n] = {'sign': sign, 'lon': lon}

    # Ascendant
    asc = chart.getAngle(const.ASC)

    # Houses
    houses = {}
    for i, house in enumerate(chart.houses, 1):
        houses[f'House_{i}'] = {
            'sign': house.sign,
            'lon': house.lon
        }

    # Aspects (major only)
    aspects = []
    for p1 in PLANETS:
        for p2 in PLANETS:
            if p1 >= p2:
                continue
            # Get aspects between the two planets using flatlib.aspects.getAspect
            try:
                obj1 = chart.getObject(p1)
                obj2 = chart.getObject(p2)
            except KeyError:
                continue
            try:
                asp = getAspect(obj1, obj2, const.MAJOR_ASPECTS)
            except Exception:
                asp = None
            if asp:
                aspects.append({
                    'p1': p1,
                    'p2': p2,
                    'type': asp.type,
                    'orb': asp.orb
                })

    # Elements & Modalities
    elem_count, mod_count = extract_elements_modalities(planet_signs)

    # Output
    chart_json = {
        'Sun': planets.get(const.SUN, {}),
        'Moon': planets.get(const.MOON, {}),
        'Ascendant': {'sign': asc.sign, 'lon': asc.lon},
        'Planets': planets,
        'Nodes': nodes,
        'Houses': houses,
        'Aspects': aspects,
        'ElementBalance': elem_count,
        'ModalityBalance': mod_count,
        'Chiron': None,  # Not available in flatlib by default
        'Stelliums': [], # Not implemented yet
    }
    return chart_json

def calculate_big_three(date_str, time_str, place_lat, place_lon):
    chart_json = calculate_full_chart(date_str, time_str, place_lat, place_lon)
    return {
        'Sun': chart_json['Sun'].get('sign', ''),
        'Moon': chart_json['Moon'].get('sign', ''),
        'Ascendant': chart_json['Ascendant'].get('sign', '')
    }

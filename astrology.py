# Force Flatlib to use the Meeus backend if Swiss Ephemeris is unavailable
import os
os.environ['FLATLIB_EPHEMERIS'] = os.environ.get('FLATLIB_EPHEMERIS', 'meeus')

# --- AstroVars CLI Workflow ---
def get_user_birth_details_and_interpret():
    from llm_handler import run_llm
    print("=== AstroVars Terminal ===")
    name = input("Name: ")
    place = input("Place of Birth (City, Country): ")
    date = input("Date of Birth (YYYY-MM-DD): ")
    time = input("Time of Birth (HH:MM, 24hr): ")

    ask_llm = input("Would you like an AI interpretation of your birth details? (y/n): ").strip().lower()
    if ask_llm.startswith('y'):
        print("\nGetting AI interpretation...")
        try:
            llm_output = run_llm(name, date, time, place)
            print("\n--- AI Interpretation ---\n")
            print(llm_output)
        except Exception as e:
            print(f"Error calling LLM: {e}")

if __name__ == "__main__":
    get_user_birth_details_and_interpret()

# Astrology libraries
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const
from flatlib.aspects import getAspect

# Timezone lookup & conversion
from timezonefinder import TimezoneFinder
from zoneinfo import ZoneInfo
import pytz  # For timezone offset calculation
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
PLANETS = [
    const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
    const.JUPITER, const.SATURN, const.URANUS, const.NEPTUNE, const.PLUTO
]
NODES = [const.NORTH_NODE, const.SOUTH_NODE]
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

# Timezone utilities
def get_timezone_name(lat, lon):
    """Return the IANA timezone name for given coordinates."""
    tf = TimezoneFinder()
    return tf.timezone_at(lat=lat, lng=lon) or "UTC"

def local_to_utc(local_dt, tz_name):
    """Convert naive local datetime to a timezone-aware UTC datetime."""
    tz = ZoneInfo(tz_name)
    localized = local_dt.replace(tzinfo=tz)
    return localized.astimezone(ZoneInfo("UTC"))

# Helper: Convert decimal degrees to DMS string for Flatlib
# Example: 40.7128 (lat) -> '40N42', -74.0060 (lon) -> '074W00'
def decimal_to_dms_str(value, is_lat=True):
    deg = abs(int(float(value)))
    min_ = int((abs(float(value)) - deg) * 60)
    dir_ = ("N" if float(value) >= 0 else "S") if is_lat else ("E" if float(value) >= 0 else "W")
    if is_lat:
        return f"{deg}{dir_}{min_:02d}"
    else:
        return f"{deg:03d}{dir_}{min_:02d}"

# Helpers for element and modality counts
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

# Core calculation functions
def calculate_full_chart(date_str, time_str, place_lat, place_lon):
    """
    Returns a dict with full natal chart info:
    planets, nodes, houses, aspects, element & modality balances, ascendant, etc.
    
    Parameters:
    - date_str: Date in YYYY-MM-DD format (ISO)
    - time_str: Time in HH:MM format (24-hour)
    - place_lat: Latitude as decimal degrees (positive for North, negative for South)
    - place_lon: Longitude as decimal degrees (positive for East, negative for West)
    """
    logging.info(f"Calculating chart for {date_str} {time_str} at {place_lat}, {place_lon}")
    
    # 1) Parse the input date and time
    try:
        local_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        logging.info(f"Parsed local datetime: {local_dt}")
    except ValueError as e:
        logging.error(f"Date/time parsing error: {e}")
        raise
    
    # 2) Get timezone and calculate offset
    tz_name = get_timezone_name(place_lat, place_lon)
    logging.info(f"Timezone name for location: {tz_name}")
    
    try:
        tz = pytz.timezone(tz_name)
        localized = tz.localize(local_dt)
        offset_raw = localized.strftime('%z')  # e.g. "-0500"
        tz_offset = f"{offset_raw[:3]}:{offset_raw[3:]}"  # e.g. "-05:00"
        logging.info(f"Timezone offset: {tz_offset}")
    except Exception as e:
        logging.error(f"Timezone error: {e}")
        tz_offset = "+00:00"  # Default to UTC if there's an error
        logging.warning(f"Defaulting to UTC ({tz_offset})")
    
    # 3) Convert coordinates to DMS format for Flatlib
    lat_str = decimal_to_dms_str(place_lat, is_lat=True)
    lon_str = decimal_to_dms_str(place_lon, is_lat=False)
    logging.info(f"DMS coordinates: {lat_str}, {lon_str}")
    
    # 4) Format date for Flatlib (MM/DD/YYYY format)
    # CRITICAL: Flatlib expects MM/DD/YYYY (American format)
    flatlib_date = local_dt.strftime('%m/%d/%Y')
    logging.info(f"Flatlib date format: {flatlib_date}")
    
    # 5) Create Flatlib objects and calculate chart
    try:
        dt = Datetime(flatlib_date, time_str, tz_offset)
        pos = GeoPos(lat_str, lon_str)
        chart = Chart(dt, pos)
        logging.info("Chart calculated successfully")
    except Exception as e:
        logging.error(f"Flatlib chart calculation error: {e}")
        raise

    # 3) Extract planetary data
    planets = {}
    planet_signs = []
    for p in PLANETS:
        try:
            obj = chart.getObject(p)
            sign  = getattr(obj, 'sign', None)
            lon   = getattr(obj, 'lon', None)
            speed = getattr(obj, 'speed', None)  # fixed: use getattr
        except KeyError:
            sign = lon = speed = None
        planets[p] = {'sign': sign, 'lon': lon, 'speed': speed}
        if sign:
            planet_signs.append(sign)

    # 4) Nodes
    nodes = {}
    for n in NODES:
        try:
            obj  = chart.getObject(n)
            sign = getattr(obj, 'sign', None)
            lon  = getattr(obj, 'lon', None)
        except KeyError:
            sign = lon = None
        nodes[n] = {'sign': sign, 'lon': lon}

    # 5) Ascendant
    asc = chart.getAngle(const.ASC)

    # 6) Houses
    houses = {
        f"House_{i+1}": {'sign': h.sign, 'lon': h.lon}
        for i, h in enumerate(chart.houses)
    }

    # 7) Major aspects
    aspects = []
    for i, p1 in enumerate(PLANETS):
        for p2 in PLANETS[i+1:]:
            try:
                o1  = chart.getObject(p1)
                o2  = chart.getObject(p2)
                asp = getAspect(o1, o2, const.MAJOR_ASPECTS)
                if asp:
                    aspects.append({
                        'p1': p1,
                        'p2': p2,
                        'type': asp.type,
                        'orb': asp.orb
                    })
            except Exception:
                pass

    # 8) Element & modality balance
    elem_count, mod_count = extract_elements_modalities(planet_signs)

    # 9) Assemble chart JSON
    return {
        'Sun': planets.get(const.SUN, {}),
        'Moon': planets.get(const.MOON, {}),
        'Ascendant': {'sign': asc.sign, 'lon': asc.lon},
        'Planets': planets,
        'Nodes': nodes,
        'Houses': houses,
        'Aspects': aspects,
        'ElementBalance': elem_count,
        'ModalityBalance': mod_count,
        'Chiron': None,
        'Stelliums': []
    }

def calculate_big_three(date_str, time_str, place_lat, place_lon):
    """
    Returns just the Sun, Moon, and Ascendant signs.
    """
    chart = calculate_full_chart(date_str, time_str, place_lat, place_lon)
    return {
        'Sun': chart['Sun'].get('sign', ''),
        'Moon': chart['Moon'].get('sign', ''),
        'Ascendant': chart['Ascendant'].get('sign', '')
    }

# ─── Example Usage ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sample = calculate_big_three(
        date_str="1995-06-15",
        time_str="12:00",
        place_lat=40.7128,
        place_lon=-74.0060
    )
    print("Big Three for 1995-06-15 12:00 (NYC):", sample)

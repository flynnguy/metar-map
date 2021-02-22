import machine
import neopixel
import time
import utime
import ujson

import urequests as requests

with open('airports.json') as fp:
    airports = ujson.loads(fp.read())

pin = 15                    # Pin the data line is connected to
wind_threshold = 15         # Knots of windspeed
blink_speed = 0.8
metar_update_frequency = 500

flight_category_rgb = {
    'WHITE': (255, 255, 255),   # White for Lightning
    'LIFR': (125, 0, 125),      # Magenta
    'LIFR_FADE': (75, 0, 75),   # Magenta Fade for wind
    'IFR': (255, 0, 0),         # Red
    'IFR_FADE': (255, 0, 0),    # Red Fade for wind
    'MVFR': (0, 0, 255),        # Blue
    'MVFR_FADE': (0, 0, 125),   # Blue Fade for wind
    'VFR': (0, 255, 0),         # Green
    'VFR_FADE': (0, 125, 0),    # Green Fade for wind
    'CLEAR': (0, 0, 0),         # Clear (blank)
}

API_URL = "https://www.aviationweather.gov/adds/dataserver_current/httpparam" \
    "?dataSource=metars&requestType=retrieve&format=csv&hoursBeforeNow=5" \
    "&mostRecentForEachStation=true&stationString="

API_URL += ','.join(list(airports))


def get_metars():
    """
    get_metars() fetches all the airport METARs and returns a dict:

    stations['ICAO CODE'] = {               # ICAO CODE is the airport identifier (ex: KBOS)
        'raw_metar': metar[0],              # This stores the raw metar in case we want to display it later if we want
        'flight_category': metar[30],       # VFR, MVFR, IFR, LIFR
        'wind_speed_kt': metar[8],          # Wind speed in knots
        'wind_gust_kt': metar[9],           # Wind gusts if any, if not it is an ''
        'pixel': airports[station_id],      # Where in the pixel chain the airport is located
        'lightning': True if 'LTG' in metar[0] else False,  # If 'LTG' is in the raw metar
        'last_state': 'on',                 # Used to know what the last state was if blinking
    }
    """
    response = requests.get(API_URL)
    response_split = response.text.split('\n')
    stations = {}

    for i in range(6, 6 + len(airports)):
        metar = response_split[i].split(',')

        station_id = metar[1]
        stations[station_id] = {
            'raw_metar': metar[0],
            'flight_category': metar[30],
            'wind_speed_kt': metar[8],
            'wind_gust_kt': metar[9],
            'pixel': airports[station_id],
            'lightning': True if 'LTG' in metar[0] else False,
            'last_state': 'on',
        }
    return stations


stations = get_metars()
last_fetched = utime.time()  # The number of seconds, as an integer, since power on
while True:
    np = neopixel.NeoPixel(machine.Pin(pin), len(airports))  # Initialize neopixels
    # Check if we want to refresh the metars
    if (utime.time() - last_fetched) > metar_update_frequency:
        stations = get_metars()
        last_fetched = utime.time()
    for station, data in stations.items():
        color = None
        # Uncomment one of the below items to test
        # data['lightning'] = True
        # data['wind_speed_kt'] = '16'
        # data['wind_gust_kt'] = '16'
        flight_category = data['flight_category']
        if data['lightning']:
            # Use white for lightning
            color = flight_category_rgb['WHITE']
        elif int(data['wind_speed_kt']) > wind_threshold:
            color = flight_category_rgb[flight_category + '_FADE']
        elif data['flight_category']:
            # Normal conditions for category
            color = flight_category_rgb[flight_category]
        else:
            # Unknown state, reset to blank
            color = flight_category_rgb['CLEAR']

        # These are the states we want to blink on (wind gusts and lightning)
        if data['wind_gust_kt'] or data['lightning']:
            if 'color' in data and data['color'] != flight_category_rgb['CLEAR']:
                color = flight_category_rgb['CLEAR']
        stations[station]['color'] = color
        np[data['pixel']] = color
    np.write()

    time.sleep(blink_speed)

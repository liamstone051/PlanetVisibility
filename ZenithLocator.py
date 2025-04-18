from ephem import *
import math

def time_to_long(lst_deg, gst_deg):
    calc_long = lst_deg - gst_deg
    if calc_long > 180:
        calc_long -= 360
    if calc_long < -180:
        calc_long += 360
    return calc_long * 15

def zenith_locator(planet):
    testing_planet = planet(now())
    greenwich = Observer()
    greenwich.lat = '51:28:38'
    gst = float(greenwich.sidereal_time()) * 12 / pi
    planet_ra = float(testing_planet.ra) * 12 / pi
    calculated_lon = time_to_long(planet_ra, gst)
    return (math.degrees(testing_planet.dec), calculated_lon)

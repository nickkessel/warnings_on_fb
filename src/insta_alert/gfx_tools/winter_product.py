import re
from colorama import Fore, Back
from .metar import build_kdtree, get_nearest_station, get_station_temp, get_list_of_nearest_stations
from insta_alert.utils.constants import WINTER
from shapely.geometry import Point, Polygon
def is_alert_winter(alert, centerlat, centerlon, alert_geometry):
    """Evaluates if a given alert deals with winter weather.
    Any "Winter" type alerts, and special weather statements

    Args:
        alert (NWS Alert Object): Alert to evaluate
        centerlat (float): Middle of the alert polygon latitude
        centerlon (float): Middle of the alert polygon longitude
        alert_geometry (Shapely Geom Object): Geometry (either polygon or zone), from the get_alert_geometry() function

    Returns:
        boolean: if it deals with winter weather
    """
    alert_type = alert['properties'].get("event")
    #print(centerlat, centerlon)
 
    if alert_type in WINTER or alert_type == 'Special Weather Statement':
        #combining both, bc if a wsw or smth is issued out in advance, it may not be cold enough for the snow cmap yet.
        description_text = alert['properties'].get('description', '').lower()
        station_temp = 99.0 #default to this bit of the check being FALSE unless the station is close enough
        attempts = 5 #check this many nearby stations
        ids, lats, lons, temps = get_list_of_nearest_stations(centerlat, centerlon, attempts) #check {attempts} nearest
        for i in range(attempts):
            station_point = Point(lons[i], lats[i])
            if alert_geometry.contains(station_point):
                #print(f'WINTER: inside, temp {temps[i]}')
                if temps[i] != None:
                    print(f'WINTER: Using {ids[i]}, at {temps[i]}C')
                    station_temp = temps[i]
                    break
                else:
                    print(f'WINTER: observation at {ids[i]} is None, checking next.')
            else:
                print(f'WINTER: observation at {ids[i]} not in alert geom')
                
                
        snow_pattern = (
                r"(?i)\b("
                r"wintry\s+mix|"
                r"(?:light|moderate|heavy)?\s*snow(?:fall|falling|showers|accumulations?)?|"
                r"snow\s+accumulations?|"
                r"freezing\s+(?:drizzle|rain)|"
                r"ice\s+accumulations?|"
                r"icy\s+(?:roads?|conditions?)|"
                r"slick\s+(?:roads?|travel)|"
                r"black\s+ice|"
                r"blowing\s+snow|"
                r"snow\s+covered\s+roads?"
                r")\b"
        )  #regex to check for winter stuff goes here. need more
        snow_match = re.search(snow_pattern, description_text)
       # print(description_text)
        #print(snow_match)
        if (station_temp <= 2.0) or (snow_match):
            print(Fore.LIGHTBLUE_EX + 'WINTER: Using snow cmap' + Fore.RESET)
            return True
            #pefrom metar query with that many nearby stations, return the lists of each variable. 
            #if station 1 (nearest distance) lat/lon is in the polygon, use that and check for temp.
            #if the temp exists, use it for the check
            #if the temp doesnt exist, go to the next closest station, repeat check of if its in polygon and existing temp
        
        
        '''
        if dist < 35: #anything within 35km
            station_temp = get_station_temp(station)
           
            snow_pattern = r'\bsnow'  #regex to check for winter stuff goes here. need more
            snow_match = re.search(snow_pattern, description_text)
            if snow_match and station_temp < 5.0: #colder than 5c and theres snow match? winter it...
                print(Fore.LIGHTBLUE_EX + 'Winter SPS identified by regex and METAR, using snow cmap' + Fore.RESET)
                return True
            else:
                return False
        else:
            station_temp = 0.0 #defaulting again if the station is too far away
           
            snow_pattern = r'\bsnow'  #regex to check for winter stuff goes here. need more
            snow_match = re.search(snow_pattern, description_text)
            if snow_match:
                print(Fore.LIGHTBLUE_EX + 'Winter SPS identified by regex only, using snow cmap' + Fore.RESET)
                return True
            else:
                return False
        '''
    return False

#want this to run when script startup
#tree, df = build_kdtree()

#station, dist = get_nearest_station(tree, df, 45.678, -110.67)

#(get_station_temp(station))
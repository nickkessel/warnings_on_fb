from shapely.geometry import Polygon
from pyproj import Geod
from colorama import Fore, Back, Style
def calc_area(raw_coords):
    coords = raw_coords[0]
    polygon = Polygon(coords)
    geod = Geod(ellps="WGS84")
    
    area_m2, _ = geod.geometry_area_perimeter(polygon)
    area_m2 = abs(area_m2)
    area_km2 = round(area_m2 / 1000000, 2)
    print(Fore.BLUE + f'POLY: area in km sq. {area_km2}' + Fore.RESET)
    return area_km2

from shapely.geometry import shape
from colorama import Fore, Back
import requests
import time
from shapely import unary_union, buffer
import gc

zone_geometry_cache = {}
MAX_ZONES_IN_CACHE = 75 #was 200, but seemed to get some errors possibly as a result. no alert should be much bigger than 75 zones?

def count_vertices(geom):
    """Helper to count total vertices in a geometry."""
    if geom is None:
        return 0
    if geom.geom_type == 'Polygon':
        return len(geom.exterior.coords)
    elif geom.geom_type == 'MultiPolygon':
        return sum(len(g.exterior.coords) for g in geom.geoms)
    else:
        return 0
    
def get_alert_geometry(alert):
    """
    Determines the geometry for an alert. 
    If the alert has a direct (polygon) geometry, it uses that.
    If not, it fetches and combines geometries from the affected zones.
    """
    # Check for a direct polygon geometry first
    geometry_data = alert.get("geometry")
    if geometry_data:
        print("Processing polygon-based alert.")
        #print(shape(geometry_data))
        return shape(geometry_data), 'polygon'

    # If no direct geometry, process as a zone-based alert (e.g., a Watch)
    print("GEO: Processing zone-based alert (geometry is null).")
    affected_zones = alert['properties'].get('affectedZones', [])
    if not affected_zones:
        print(Fore.YELLOW + "Alert has no geometry and no affected zones." + Fore.RESET)
        return None, None
    
    alert_type = alert['properties'].get("event")
    '''
    if issuing_state == 'AK' and alert_type == 'Special Weather Statement':
        print('not plotting due to known errors with Alaska zone-based SPS.')
        return None, None
    '''
    geometries = []
    print(f"GEO: Fetching geometries for {len(affected_zones)} zones...")
    max_retries = 5
    for attempt in range(max_retries):
        for zone_url in affected_zones:
            if zone_url in zone_geometry_cache: # Check cache first to reduce API calls
                geometries.append(zone_geometry_cache[zone_url])
                continue
            
            try:
                # Fetch zone data from the NWS API
                response = requests.get(zone_url, headers={"User-Agent": "warnings_on_fb/kesse1ni@cmich.edu"}, timeout=10)
                response.raise_for_status()
                zone_geom_data = response.json().get('geometry')
                
                if zone_geom_data:
                    zone_shape = shape(zone_geom_data)
                    #print(f'GEO: {count_vertices(zone_shape)} vertices pre-simplify')
                    zone_shape = zone_shape.simplify(0.0075, preserve_topology= True) #0.001 is like 0.001deg (100m), which should reduce vertex count. increase value to use less memory and have lower res 
                            #alert geom borders. 0.02 is prob the highest you wanna go b4 u start losing important detail, esp w/ smaller alerts. could work in a way for larger (more zone) alerts have larger val,
                            #leading to less fine detail and alerts w/ less zones have smaller val, leading to more detail 0.0075 seems p good
                    #print(f'GEO: {count_vertices(zone_shape)} vertices post-simplify')
                    geometries.append(zone_shape)
                    if len(zone_geometry_cache) >= MAX_ZONES_IN_CACHE:
                        # remove a random item (simple approach) or the first item
                        zone_geometry_cache.pop(next(iter(zone_geometry_cache)))
                    zone_geometry_cache[zone_url] = zone_shape
            except requests.RequestException as e:
                print(Fore.RED + f"GEO: Failed to fetch geometry for zone {zone_url}: {e}. Attempt {attempt}, retrying." + Fore.RESET)
                if attempt + 1 >= max_retries:
                    print(Back.RED + f"GEO: All download attempts ({max_retries}) failed" + Back.RESET)
                    attempt += 1
                    continue
                else:
                    time.sleep(2)
    if not geometries:
        print(Fore.RED + "GEO: Could not retrieve any geometries for the affected zones." + Fore.RESET)
        return None
    try:
        # Combine all individual zone polygons into one single shape
        combined_geometry = unary_union(geometries)
        
        del geometries
        gc.collect()
        #print(f'GEO: {count_vertices(combined_geometry)} vertices pre-buffer')
        clean_geometry = buffer(combined_geometry, 0.001, quad_segs= 1) #should remove tiny/weird overlaps. less quad segs = less resolution mehtinks
        #print(f'GEO: {count_vertices(clean_geometry)} vertices post-buffer')
        print("GEO: Successfully combined zone geometries.")
        return clean_geometry, 'zone'
    
    except Exception as e:
        print(Fore.RED + f"Error combining geometries: {e}" + Fore.RESET)
        gc.collect()
        return None, None
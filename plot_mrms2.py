import requests
import gzip
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

#recreate radarscope colortable for colormap
# List of (dBZ, RGBA) tuples 
stops1 = [
    (-15, (0, 0, 0, 0)),
    (5, (29, 37, 60)),
    (17.5, (89, 155, 171)),
    (22.5, (33, 186, 72)),
    (32.5, (5, 101, 1)),
    (37.5, (251, 252, 0)),  # to (199,176,0) maybe a typo? Using first set
    (42.5, (253, 149, 2)),  # to (172,92,2) same, using first
    (50, (253, 38, 0)),     # to (135,43,22) same
    (60, (193, 148, 179)),  # to (200,23,119) — mixed RGB? Use first
    (70, (165, 2, 215)),    # to (64,0,146)
    (75, (135, 255, 253)),  # to (54,120,142)
    (80, (173, 99, 64)),
    (85, (105, 0, 4)),
    (95, (0, 0, 0)),
]

# Normalize dBZ values to 0–1 for matplotlib
min_dbz1 = stops1[0][0]
max_dbz1 = stops1[-1][0]
normalized_stops1 = [
    ((level - min_dbz1) / (max_dbz1 - min_dbz1), tuple(c/255 for c in color))
    for level, color in stops1
]

# Create the colormap
radarscope_cmap = LinearSegmentedColormap.from_list("radarscope", normalized_stops1)

#inches, (R G B)
stops2 = [
    (0.0,  (0, 0, 0, 0)),         
    (0.01, (155, 255, 155, 255)), 
    (0.5,  (0, 200, 0, 255)),     
    (1.0,  (255, 255, 0, 255)),   
    (2.0,  (255, 128, 0, 255)),   
    (3.0,  (255, 0, 0, 255)),     
    (4.5,  (150, 0, 75, 255)),    
    (6.0,  (255, 0, 255, 255)),   
]

# Normalize dBZ values to 0–1 for matplotlib
min_val2 = stops2[0][0]
max_val2 = stops2[-1][0]
normalized_stops2 = [
    ((level - min_val2) / (max_val2 - min_val2), tuple(c/255 for c in color))
    for level, color in stops2
]

# Create the colormap
qpe_cmap = LinearSegmentedColormap.from_list("QPE", normalized_stops2)

valid_time = 0
def save_mrms_subset(bbox, type, output_path):
    """
    Fetches latest MRMS data, subsets it to a bounding box, 
    and saves it as a transparent PNG.

    Args:
        bbox (dict): A dictionary with keys 'lon_min', 'lon_max', 
                     'lat_min', 'lat_max'.
        type (str): The type of warning. This'll generate a different image & colormap
                     for a svr/tor (reflectivity) vs ffw (QPE). Pass in full names
        output_path (str): The path to save the output PNG file.
    """
    # 1. Download and Decompress (same as before)
    ref_url = "https://mrms.ncep.noaa.gov/2D/ReflectivityAtLowestAltitude/MRMS_ReflectivityAtLowestAltitude.latest.grib2.gz"
    qpe_url = "https://mrms.ncep.noaa.gov/2D/MultiSensor_QPE_03H_Pass1/MRMS_MultiSensor_QPE_03H_Pass1.latest.grib2.gz" #pass 1 seems to be updated sooner, could try and implement choosing diff. one depending on when alert is being generated
    qpe1_url = "https://mrms.ncep.noaa.gov/2D/RadarOnly_QPE_01H/MRMS_RadarOnly_QPE_01H.latest.grib2.gz" #seems to be updated much quicker than the other product
    
    if type == "Flash Flood Warning":
        url = qpe1_url
        print("QPE")
        cmap_to_use = qpe_cmap
        vmin, vmax = min_val2, max_val2
        cbar_label = "Radar Estimated Precipitation (1h)"
    else:
        url = ref_url
        print("REF")
        cmap_to_use = radarscope_cmap
        vmin, vmax = min_dbz1, max_dbz1
        cbar_label = "Reflectivity (dBZ)"

    print(f"Fetching data from {url}")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        grib_content = gzip.decompress(response.content)
        with open("latest.grib2", "wb") as f:
            f.write(grib_content)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading data: {e}")
        return

    # 2. Load and Subset the Data
    print("Reading and subsetting data...")
    ds = xr.open_dataset("latest.grib2", engine="cfgrib")
    
    # Use xarray's .sel() to slice the data to the bounding box
    # This is the key optimization step
    # GRIB files often use 0-360 longitude, so we convert our -180 to 180 box.
    lon_slice = slice(
        bbox['lon_min'] + 360 if bbox['lon_min'] < 0 else bbox['lon_min'],
        bbox['lon_max'] + 360 if bbox['lon_max'] < 0 else bbox['lon_max']
    )
    lat_slice = slice(bbox['lat_max'], bbox['lat_min'])

    subset = ds.sel(latitude=lat_slice, longitude=lon_slice)

    # Check if the subset is empty
    if subset.unknown.size == 0:
        print("Error: Data subset is empty. Check your bounding box coordinates.")
        os.remove("latest.grib2")
        return
    # 3. Create the Plot
    print("Generating plot...")
    fig = plt.figure(figsize=(10, 8))
    proj = ccrs.LambertConformal(central_longitude=-97.5, central_latitude=38.5)
    ax = fig.add_subplot(1, 1, 1, projection=proj)

    # Set map extent to the bounding box
    ax.set_extent(
        [bbox['lon_min'], bbox['lon_max'], bbox['lat_min'], bbox['lat_max']], 
        crs=ccrs.PlateCarree()
    )

    # 4. Customize and Plot Subset
    # Add ONLY state borders
    ax.add_feature(cfeature.STATES.with_scale('50m'), linestyle='-', edgecolor='white')
    
    im = ax.pcolormesh(
        subset.longitude, subset.latitude, subset.unknown,
        transform=ccrs.PlateCarree(),
        cmap=cmap_to_use, vmin=vmin, vmax=vmax
    )

    # Attach to the 'im' object, control size with shrink/aspect/pad
    cbar = plt.colorbar(im, orientation='horizontal', pad=0.01, aspect=50, shrink=0.85)
    cbar.set_label(cbar_label, color='white', fontsize=12, weight='bold')
    #cbar.tick_params(colors='white')



    # 5. Save the Figure to a File
    print(f"Saving image to {output_path}...")
    plt.savefig(
        output_path,
        dpi=600,                  # Adjust for resolution
        transparent=True,         # Transparent background
        bbox_inches='tight',      # Remove whitespace padding
        pad_inches=0              # Remove padding
    )
    valid_time = ds.time.dt.strftime('%Y-%m-%d %H:%M:%S UTC').item()
    print(valid_time)
    valid_time_short = ds.time.dt.strftime('%H:%M UTC').item()

    
    plt.close(fig) # Close the figure to free up memory
    os.remove("latest.grib2")
    os.remove("latest.grib2.5b7b6.idx") # Clean up the downloaded files
    print("Done.")
    return valid_time_short


if __name__ == '__main__':
    # Define a bounding box for the Ohio region
    cincy_bbox = { #this is the area that is being scanned for alerts as well
        "lon_min": -85.413208,
        "lon_max": -83.161011,
        "lat_min": 38.522384,
        "lat_max": 40.155786
    }
    test_bbox = {
        "lon_min": -82,
        "lon_max": -78,
        "lat_min": 32,
        "lat_max": 34.5
    }

    save_mrms_subset(test_bbox, "Flash Flood Warning", 'mrms_stuff/test_qpe')
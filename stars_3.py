# -*- coding: utf-8 -*-
"""Stars_3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10dtsOvwE0SbCj0xaQpXXSgQjxdEdS_wB
"""

!pip install astroquery astropy
from astroquery.gaia import Gaia
from astropy.coordinates import SkyCoord
import astropy.units as u
import pandas as pd
import numpy as np
import time

# Define the center of the sphere (in ICRS coordinates)
ra_center = 280.47  # Right Ascension in degrees
dec_center = -8.66  # Declination in degrees
distance_center = 200  # Distance in parsecs  ( 1 parsec = 3 light years and 2.4745844 x 10^12 kilometers )

sphere_radius = 25  # Radius in parsecs

# Calculate parallax range
parallax_center = 1000 / distance_center  # Parallax in milliarcseconds
parallax_min = 1000 / (distance_center + sphere_radius)
parallax_max = 1000 / (distance_center - sphere_radius)

# Calculate angular radius
angular_radius = np.degrees(np.arcsin(sphere_radius / distance_center))

# Construct ADQL query with only the columns you need
query = f"""
SELECT TOP 5000
    source_id,
    ra,
    dec,
    parallax,
    phot_g_mean_mag
FROM gaiadr3.gaia_source
WHERE 1=CONTAINS(
    POINT('ICRS', ra, dec),
    CIRCLE('ICRS', {ra_center}, {dec_center}, {angular_radius})
)
AND parallax BETWEEN {parallax_min} AND {parallax_max}
AND parallax_over_error > 5
"""

start_time = time.time()
# Execute the query
job = Gaia.launch_job_async(query)
results = job.get_results()
# Convert to pandas DataFrame
df = results.to_pandas()

# Calculate distances
center_coord = SkyCoord(ra=ra_center*u.degree, dec=dec_center*u.degree, distance=distance_center*u.pc)

# Convert the DataFrame columns to numpy arrays for SkyCoord
star_coords = SkyCoord(
    ra=df['ra'].values * u.degree,
    dec=df['dec'].values * u.degree,
    distance=(1000 / df['parallax'].values) * u.pc  # Make sure to handle potential division by zero
)

# Check for NaN values in distance due to zero parallax
df['distance_from_center'] = center_coord.separation_3d(star_coords).to(u.pc).value

end_time = time.time()





# Renaming columns to make them more readable
df_renamed = df.rename(columns={
    'source_id': 'Source ID',
    'ra': 'Right Ascension (deg)',
    'dec': 'Declination (deg)',
    'parallax': 'Parallax (mas)',
    'parallax_over_error': 'Parallax Error Ratio',
    'phot_g_mean_mag': 'G-Band Magnitude'
})

df_renamed.dropna(inplace=True)
# Display the updated DataFrame with readable column names
print(df_renamed.info())
print(df_renamed.head())
print(f'Time taken to query : {end_time - start_time}')

# If you want to save it as CSV with new names
df_renamed.to_csv('stars_in_sphere_renamed.csv', index=False)
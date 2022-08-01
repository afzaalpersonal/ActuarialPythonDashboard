# Import dependencies
import numpy as np
from natsort import natsorted, natsort_keygen

# Construct aggregated data used for geospacial charts
def get_data_agg_area(
        data_base = []
    ):

    # Aggregate base data
    data_base_agg = data_base.groupby(['Area']).agg({
        'ClaimNb'  : 'sum',
        'Exposure' : 'sum',
        'Density'  : 'mean',
        'DrivAge'  : 'mean',
        'IDpol'    : 'count'
    }).reset_index()

    # Arrange in ascending order
    data_base_agg = data_base_agg.sort_values(by=['Area'], key=natsort_keygen())

    return data_base_agg


# Construct aggregated data used for region charts
def get_data_agg_region(
        data_base       = [],
        data_region     = [],
        data_region_geo = []
    ):

    # Aggregate base data
    data_base_agg = data_base.groupby(['Region']).agg({
        'ClaimNb'  : 'sum',
        'Exposure' : 'sum',
        'Density'  : 'mean',
        'DrivAge'  : 'mean',
        'IDpol'    : 'count'
    }).reset_index()

    # Extract region ID and assign to "code" column
    data_base_agg['code'] = data_base_agg['Region'].apply(lambda x: x[1:])

    # Merge regional data with claims data
    data_region_combined = data_base_agg.merge(
        data_region,
        how = 'left',
        on  = 'Region'
    )

    # Merge combined data with geo data
    data_region_combined = data_region_combined.merge(
        data_region_geo,
        how = 'left',
        on  = 'code'
    )

    return data_region_combined


# Construct aggregated data used for brand charts
def get_data_agg_brand(
        data_base = []
    ):

    # Aggregate base data
    data_base_agg = data_base.groupby(['VehBrand']).agg({
        'ClaimNb'  : 'sum',
        'Exposure' : 'sum',
        'IDpol'    : 'count'
    }).reset_index()

    # Arrange in ascending order
    data_base_agg = data_base_agg.sort_values(by=['VehBrand'], key=natsort_keygen())

    return data_base_agg


# This function is used when creating range slider components.
def get_val_range(
        type = 'ClaimNb',
        data_base = []
    ):

    # Assign default variable values
    min = int(data_base[type].min())
    max = int(data_base[type].max())

    # Assign age range list
    return [min, max]


# This function is used when creating dropdown components.
def get_val_dropdown(
        type      = 'ClaimNb',
        data_base = []
    ):

    # Assign default variable values
    dropdown = []

    # Sort in ascending order
    values = natsorted(data_base[type].unique(), key=natsort_keygen())

    # Loop through values and construct list
    for i in values:

        # Assign values to use in dropdown
        label = i
        value = i.lower()

        # Assign option data
        row = {'label' : label, 'value' : value}

        # Update select options
        dropdown.append(row.copy())

    return dropdown

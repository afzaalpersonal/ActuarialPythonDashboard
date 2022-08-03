# Import dependencies
import numpy as np
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
from numerize import numerize

# Page summary - Total policies in filtered segment (this single function is used to construct all summary charts)
def chart_summary_policy(
    type     = 'policy',
    data     = [],
    data_bak = []
):

    # Get segment type
    if type == 'policy':

        # Create dictionary for chart naming / styling
        data_type = dict(
            title      = 'Policies',
            label      = 'Policies',
            color_hex  = '#d9ab16',
            color_rgba = 'rgba(217, 171, 22, 0.05)',
        )

        # Get values for dataset size
        val_part = len(data)
        val_full = len(data_bak)

    elif type == 'claim_policy':

        # Create dictionary for chart naming / styling
        data_type = dict(
            title      = 'Policy Claims',
            label      = 'Claims',
            color_hex  = '#113458',
            color_rgba = 'rgba(17, 52, 88, 0.05)',
        )

        # Extract data where claims are present
        data     = data.loc[(data['ClaimNb'] >= 1)]
        data_bak = data_bak.loc[(data_bak['ClaimNb'] >= 1)]

        # Get values for dataset size
        val_part = len(data)
        val_full = len(data_bak)

    elif type == 'claim_unique':

        # Create dictionary for chart naming / styling
        data_type = dict(
            title      = 'Claims',
            label      = 'Claims',
            color_hex  = '#113458',
            color_rgba = 'rgba(81, 157, 204, 0.05)',
        )

        # Extract data where claims are present
        data     = data.loc[(data['ClaimNb'] >= 1)]
        data_bak = data_bak.loc[(data_bak['ClaimNb'] >= 1)]

        # Get values for dataset size
        val_part = data['ClaimNb'].sum()
        val_full = data_bak['ClaimNb'].sum()

    elif type == 'exposure':

        data_type = dict(
            title      = 'Exposure',
            label      = 'Exposure',
            color_hex  = '#519dcc',
            color_rgba = 'rgba(81, 157, 204, 0.05)',
        )

        # Get values for dataset size
        val_part = data['Exposure'].sum()
        val_full = data_bak['Exposure'].sum()

    # Get percentages for dataset size
    per_part = round( 100 * ( val_part / val_full ), 2 )
    per_full = round( 100 * ( val_full - val_part ) / val_full, 2 )

    # Assign data inputs
    labels = [data_type['label'],'']
    values = [per_part, per_full]
    colors = [data_type['color_hex'], data_type['color_rgba']]

    # Initiate chart
    fig = go.Figure()

    # Add data to chart
    fig.add_trace(
        go.Pie(
            textinfo      = 'none',
            labels        = labels,
            values        = values,
            marker_colors = colors,
            hole          = 0.75,
            sort          = False
        )
    )

    # Update chart layout
    fig.update_layout(
        showlegend = False,
        title      = dict(
            text      = '{} in Segment'.format(data_type['title']),
            font_size = 18,
            y         = 1,
            x         = 0.5,
            xanchor   = 'center',
            yanchor   = 'top',
            font      = dict(
                color  = '#222',
                family = 'Open Sans'
            ),
        ),
        margin = dict(
            t = 40,
            b = 35,
            l = 0,
            r = 0
        ),
        annotations = [
            dict(
                text      = str(numerize.numerize(per_part, 1)) + '%',
                x         = 0.5,
                y         = 0.5,
                showarrow = False,
                font      = dict(
                    size   = 20,
                    color  = '#222',
                    family = 'Open Sans'
                ),
            ),
            dict(
                text      = 'Total: {} of {}'.format(numerize.numerize(int(val_part), 1), numerize.numerize(int(val_full), 1)),
                x         = 0.5,
                y         = -0.25,
                showarrow = False,
                font      = dict(
                    size   = 12,
                    color  = '#222',
                    family = 'Open Sans'
                ),
            ),
        ],
        hovermode = False
    )

    return fig


# Construct charts - Mixed data by driver age, vehicle age and vehicle power
def chart_mixed_total(
    type = 'DrivAge',
    data = [],
    rate = False
):

    # Exit early if no data is present
    if len(data) == 0:
        return chart_empty()

    # Features dictionary
    features = {
        'DrivAge'  : 'Driver Age',
        'VehAge'   : 'Vehicle Age',
        'VehPower' : 'Vehicle Power',
        'VehGas'   : 'Fuel Type'
    }

    # Assign default variable values
    rates  = []
    total0 = []
    total1 = []

    # Convert to data frame
    df = pd.DataFrame(data)

    # Extract specific data
    df_claims0 = df
    df_claims1 = df.loc[(df['ClaimNb'] >= 1)]

    # Initiate chart
    fig = go.Figure()

    # Get list of all areas in ascending order
    unique_values = np.sort(df_claims0[type].unique())

    # Construct data variables for each area
    for i in unique_values:

		# Update dict for total claim numbers
        total0.append(df_claims0.loc[df_claims0[type] == i, 'ClaimNb'].count())
        total1.append(df_claims1.loc[df_claims1[type] == i, 'ClaimNb'].sum())

		# Only proceed if claim rate is needed
        if rate == True:

			# Update dict for total claim rates
            rate0 = df_claims0.loc[df_claims0[type] == i, 'ClaimNb'].count()
            rate1 = df_claims1.loc[df_claims1[type] == i, 'ClaimNb'].sum()

            rate = round(rate1 / rate0, 3)

			# This check ensure that line graph doesn't drop to zero where no claims data is present for the step
            if rate > 0:
                rates.append(rate)
            else:
                rates.append(None)

    # Assign color for bars
    colors0 = ['#d9ab16',] * len( unique_values )
    colors1 = ['#113458',] * len( unique_values )
    colors2 = ['#519dcc',] * len( unique_values )

    # Add data to chart
    fig.add_trace(
        go.Bar(
            name              = 'Policies',
            legendgroup       = 'Policies',
            x                 = unique_values,
            y                 = total0,
            yaxis             = 'y1',
            opacity           = 1,
            marker_color      = colors0,
            marker_line_width = 0,
            hovertemplate     = '<br>'.join([
                features[type] + ': %{x}',
                'Policies: %{y}',
                '<extra></extra>'
            ])
        )
    )
    fig.add_trace(
        go.Bar(
            name              = 'Claims',
            legendgroup       = 'Claims',
            x                 = unique_values,
            y                 = total1,
            yaxis             = 'y1',
            opacity           = 1,
            marker_color      = colors1,
            marker_line_width = 0,
            hovertemplate     = '<br>'.join([
                features[type] + ': %{x}',
                'Claims: %{y}',
                '<extra></extra>'
            ])
        )
    )

    if rate == True:

        # Add line chart for claim rates if needed
        fig.add_trace(
            go.Scatter(
                mode              = 'lines+markers',
                name              = 'Claim Rate',
                legendgroup       = 'Claim Rate',
                x                 = unique_values,
                y                 = rates,
                yaxis             = 'y2',
                opacity           = 1,
                line_color        = colors2[0],
                marker_color      = colors2,
                marker_line_width = 0,
                marker_size       = 4,
                hovertemplate     = '<br>'.join([
                    features[type] + ': %{x}',
                    'Claim Rate: %{y}',
                    '<extra></extra>'
                ])
            )
        )

    # Update chart layout
    fig.update_layout(
        barmode = 'group',
        legend  = dict(
            title_text    = '',
            tracegroupgap = 0,
            orientation   = 'h',
            yanchor       = 'bottom',
            xanchor       = 'center',
            y             = -0.3,
            x             = 0.5,
        ),
        xaxis = dict(
            title = features[type],
        ),
        yaxis1 = dict(
            title = 'Total',
        ),
        yaxis2 = dict(
            title      = 'Claim Rate',
            overlaying = 'y1',
            side       = 'right',
            showgrid   = False
        ),
        title = dict(
            text      = 'Total by {}'.format(features[type]),
            font_size = 18,
            y         = 1,
            x         = 0.5,
            xanchor   = 'center',
            yanchor   = 'top',
            font      = dict(
                color  = '#222',
                family = 'Open Sans'
            ),
        ),
        plot_bgcolor  = 'rgba(255, 255, 255, 0)',
        paper_bgcolor = 'rgba(255, 255, 255, 0)',
        margin = dict(
            t = 25,
            b = 0,
            l = 0,
            r = 0
        ),
    )

    # Show Chart
    return fig


# Construct charts - Vehicle brand analysis
def chart_bubble_mixed(
    data = [],
    rate = False
):

    # Exit early if no data is present
    if len(data) == 0:
        return chart_empty()

    # Reset variable values
    data_tooltips = []

    # Assign default variable values
    y_title = 'Claims'

    # Assign default variable values
    sizeref_min = 4
    sizeref_max = 50

    # Convert to data frame
    df = pd.DataFrame(data)

    # Initiate chart
    fig = go.Figure()

    # Get bubble sizes
    veh_brand = df['VehBrand']
    claim_nb  = df['ClaimNb']
    exposure  = df['Exposure']
    id_pol    = df['IDpol']

    # Rebase claim numbers to claim rate if needed
    if rate == True:
        claim_nb = round( claim_nb / id_pol, 3)
        y_title  = 'Claim Rate'

    # Set bubble sizes
    sizes = sizeref_min + (sizeref_max - sizeref_min) * np.array(exposure) / max(exposure)

    # Construct tooltips
    for k, v in veh_brand.items():

        # Change tooltop content depending on chart type (claims or claim rate)
        if rate == True:
            data_tooltips.append('Brand: {}<br />Claims: {}<br />Exposure: {}<extra></extra>'.format(veh_brand[k], round(claim_nb[k], 3), numerize.numerize(int(exposure[k]), 1)))
        else:
            data_tooltips.append('Brand: {}<br />Claims: {}<br />Exposure: {}<extra></extra>'.format(veh_brand[k], numerize.numerize(int(claim_nb[k]), 1), numerize.numerize(int(exposure[k]), 1)))

    # Assign color for bars
    colors  = ['#519dcc',] * len( veh_brand )
    opacity = [1,] * len( veh_brand )

    # Add data to chart
    fig.add_trace(
        go.Scatter(
            x            = veh_brand,
            y            = claim_nb,
            mode         = 'markers',
            marker_color = colors,
            marker       = dict(
                size    = sizes,
                opacity = opacity,
            ),
            hovertemplate = data_tooltips
        )
    )

    # Update chart layout
    fig.update_layout(
        barmode = 'stack',
        legend  = {
            'title_text'    : 'Area',
            'tracegroupgap' : 0,
        },
        xaxis = dict(
            title     = 'Brand',
            gridcolor = '#fff'
        ),
        yaxis = dict(
            title     = y_title,
            gridcolor = '#fff'
        ),
        title = dict(
            text      = 'Claims by Brand & Exposure',
            font_size = 18,
            y         = 1,
            x         = 0.5,
            xanchor   = 'center',
            yanchor   = 'top',
            font      = dict(
                color  = '#222',
                family = 'Open Sans'
            ),
        ),
        plot_bgcolor  = 'rgba(255, 255, 255, 0)',
        paper_bgcolor = 'rgba(255, 255, 255, 0)',
        margin = dict(
            t = 25,
            b = 0,
            l = 0,
            r = 0
        ),
    )

    # Show Chart
    return fig


# Construct chart - Fuel type
def chart_pie_fuel(
    data = []
):

    # Exit early if no data is present
    if len(data) == 0:
        return chart_empty()

    # Reset variable values
    data_tooltips = []

    # Assign default variable values
    labels = []
    values = []

    # Convert to data frame
    df = pd.DataFrame(data)

    # Get list of all areas in ascending order
    unique_values = np.sort(df['VehGas'].unique())

    # Construct data variables for each area
    for i in unique_values:

        # Get total number of policies
        value = np.sum(df['VehGas'] == i)

        # Assign pie chart data
        labels.append(i)
        values.append(value)

        # Construct tooltip data
        data_tooltips.append('Fuel: {}<br />Policies: {}<extra></extra>'.format(i, numerize.numerize(int(value), 1)))

    # Assign colors for each section
    colors = ['#d9ab16', '#113458']

    # Initiate chart
    fig = go.Figure()

    # Add data to chart
    fig.add_trace(
        go.Pie(
            labels        = labels,
            values        = values,
            marker_colors = colors,
            hole          = 0,
            sort          = False,
            hovertemplate = data_tooltips
        )
    )

    # Update chart layout
    fig.update_layout(
        legend = dict(
            title_text    = '',
            tracegroupgap = 0,
            orientation   = 'h',
            yanchor       = 'bottom',
            xanchor       = 'center',
            y             = -0.5,
            x             = 0.5,
        ),
        title = dict(
            text      = 'Fuel Type',
            font_size = 18,
            y         = 1,
            x         = 0.5,
            xanchor   = 'center',
            yanchor   = 'top',
            font      = dict(
                color  = '#222',
                family = 'Open Sans'
            ),
        ),
        margin = dict(
            t = 75,
            b = 0,
            l = 0,
            r = 0
#            t = 75,
#            b = 85,
#            l = 0,
#            r = 0
        ),
    )

    return fig

# Construct chart - Area analysis
def chart_mixed_area(
    type = 'IDpol',
    data = []
):

    # Exit early if no data is present
    if len(data) == 0:
        return chart_empty()

    # Assign default variable values
    sizeref_min = 4
    sizeref_max = 50

    # Convert to data frame
    df = pd.DataFrame(data)

    # Initiate chart
    fig = go.Figure()

    # Get list of all areas in ascending order
    unique_values = np.sort(df[type].unique())

    # Get bubble sizes
    exposure = df['Exposure']

    # Set bubble sizes
    sizes = sizeref_min + (sizeref_max - sizeref_min) * np.array(exposure) / max(exposure)

    # Assign color for various chart sections
    colors0 = ['#d9ab16',] * len( unique_values )
    colors1 = ['#113458',] * len( unique_values )
    colors2 = ['#519dcc',] * len( unique_values )

    # Ensure bubbles are not opaque
    opacity = [1,] * len( unique_values )

    # Add data to chart
    fig.add_trace( # Bar chart for total policies
        go.Bar(
            name              = 'Policies',
            legendgroup       = 'Policies',
            x                 = df['Area'],
            y                 = df['IDpol'],
            yaxis             = 'y1',
            opacity           = 1,
            marker_color      = colors0,
            marker_line_width = 0,
            hovertemplate     = '<br>'.join([
                'Area: %{x}',
                'Policies: %{y}',
                '<extra></extra>'
            ])
        )
    )
    fig.add_trace( # Bar chart for total claims
        go.Bar(
            name              = 'Claims',
            legendgroup       = 'Claims',
            x                 = df['Area'],
            y                 = df['ClaimNb'],
            yaxis             = 'y1',
            opacity           = 1,
            marker_color      = colors1,
            marker_line_width = 0,
            hovertemplate     = '<br>'.join([
                'Area: %{x}',
                'Claims: %{y}',
                '<extra></extra>'
            ])
        )
    )
    fig.add_trace( # Line chart for average age
        go.Scatter(
            mode         = 'lines+markers',
            name         = 'Avg DrivAge',
            legendgroup  = 'Avg DrivAge',
            x            = df['Area'],
            y            = df['DrivAge'],
            yaxis        = 'y2',
            opacity      = 1,
            line_color   = colors2[0],
            marker_color = colors2,
            marker       = dict(
                opacity = opacity,
            ),
            marker_line_width = 0,
            hovertemplate     = '<br>'.join([
                'Area: %{x}',
                'Avg Driver Age: %{y}',
                '<extra></extra>'
            ])
        )
    )
    fig.add_trace( # Bubble size for exposure
        go.Scatter(
            mode         = 'markers',
            name         = 'Exposure',
            legendgroup  = 'Exposure',
            x            = df['Area'],
            y            = df['DrivAge'],
            yaxis        = 'y2',
            opacity      = 1,
            line_color   = colors2[0],
            marker_color = colors2,
            marker       = dict(
                size = sizes,
            ),
            marker_line_width = 0,
            hovertemplate     = '<br>'.join([
                'Area: %{x}',
                'Exposure: %{marker}',
                '<extra></extra>'
            ])
        )
    )

    # Update chart layout
    fig.update_layout(
        barmode    = 'stack',
        legend     = dict(
            title_text    = '',
            tracegroupgap = 0,
            orientation   = 'h',
            yanchor       = 'bottom',
            xanchor       = 'center',
            y             = -0.3,
            x             = 0.5,
        ),
        xaxis = dict(
            title = 'Area',
        ),
        yaxis1 = dict(
            title = 'Total',
        ),
        yaxis2 = dict(
            title      = 'Avg DrivAge',
            overlaying = 'y1',
            side       = 'right',
            showgrid   = False
        ),
        title = dict(
            text      = 'Area Analysis',
            font_size = 18,
            y         = 1,
            x         = 0.5,
            xanchor   = 'center',
            yanchor   = 'top',
            font      = dict(
                color  = '#222',
                family = 'Open Sans'
            ),
        ),
        plot_bgcolor  = 'rgba(255, 255, 255, 0)',
        paper_bgcolor = 'rgba(255, 255, 255, 0)',
        margin = dict(
            t = 25,
            b = 0,
            l = 0,
            r = 0
        ),
    )

    # Show Chart
    return fig

# Chart to show claims data by region - Modified from original by Mark Cooper
def chart_geo(
    column = 'DrivAge',
    data   = []
):

    # Exit early if no data is present
    if len(data) == 0:
        return chart_empty()

    # Features dictionary
    features = {
        'IDpol'    : 'Total Policies by Region',
        'ClaimNb'  : 'Total Claims by Region',
        'Exposure' : 'Total Exposure by Region',
        'Density'  : 'Population Density by Region',
        'DrivAge'  : 'Average Driver Age by Region'
    }

    # Convert to GeoPandas dataframe
    df_geo = gpd.GeoDataFrame(data)

    # Set index on Region
    df_geo = df_geo.set_index('Region')

    # Construct chart
    fig = px.choropleth(
        df_geo,
        geojson                = df_geo.geometry,
        locations              = df_geo.index,
        color                  = column,
        projection             = 'mercator',
        color_continuous_scale = 'Blues',
        hover_name             = 'Name'
    )

    # Update chart geos
    fig.update_geos(
        fitbounds = 'locations',
        visible   = False
    )

    # Update chart layout
    fig.update_layout(
        title = dict(
            text      = features[column],
            font_size = 18,
            y         = 1,
            x         = 0.5,
            xanchor   = 'center',
            yanchor   = 'top',
            font      = dict(
                color  = '#222',
                family = 'Open Sans'
            ),
        ),
        plot_bgcolor  = 'rgba(255, 255, 255, 0)',
        paper_bgcolor = 'rgba(255, 255, 255, 0)',
        margin = dict(
            t = 25,
            b = 0,
            l = 0,
            r = 0
        ),
    )

    # Show Chart
    return fig


# Placeholder content if not data is present
def chart_empty():

    fig = go.Figure()

    fig.update_layout(
        xaxis = dict(
            visible = False
        ),
        yaxis = dict(
            visible = False
        ),
        annotations = [
            dict(
#                text = 'No Data Available',
                text      = 'No matching records',
                xref      = 'paper',
                yref      = 'paper',
                y         = 0.55,
                x         = 0.5,
                showarrow = False,
                font      = dict(
                    size = 20
                )
            )
        ],
        plot_bgcolor  = 'rgba(255, 255, 255, 0)',
        paper_bgcolor = 'rgba(255, 255, 255, 0)',
        margin = dict(
            t = 25,
            b = 0,
            l = 0,
            r = 0
        ),
    )

    return fig

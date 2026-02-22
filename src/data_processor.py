"""
Process and calculate 5-year ranges for petroleum stock data.

This module handles the statistical processing of petroleum stock data to calculate
the 5-year historical min/max ranges that are displayed as shaded areas on the graphs,
matching the style of the EIA Weekly Petroleum Status Report.
"""

import pandas as pd
from datetime import datetime, timedelta


def calculate_five_year_range(df, reference_date=None):
    """
    Calculate 5-year minimum and maximum values for each week of the year.
    
    This function computes the historical range (min/max) for each week across
    the previous 5 years. This creates the shaded "5-year range" band shown on
    EIA petroleum stock graphs.
    
    Methodology:
    1. Filter data to last 5 years from reference date
    2. Group data by ISO week number (1-52/53)
    3. Calculate min and max stock levels for each week across all 5 years
    
    Args:
        df (pandas.DataFrame): DataFrame with 'date' and 'value' columns containing
                              historical stock data
        reference_date (datetime, optional): Date to calculate range relative to.
                                            Defaults to the most recent date in the data.
    
    Returns:
        pandas.DataFrame: DataFrame with columns:
                         - week_of_year: ISO week number (1-52/53)
                         - min_5yr: Minimum stock level for that week over 5 years
                         - max_5yr: Maximum stock level for that week over 5 years
    
    Example:
        >>> df = pd.DataFrame({
        ...     'date': pd.date_range('2020-01-01', periods=260, freq='W'),
        ...     'value': range(260)
        ... })
        >>> range_df = calculate_five_year_range(df)
        >>> print(range_df.head())
           week_of_year  min_5yr  max_5yr
        0             1      0.0    260.0
        1             2      1.0    261.0
    """
    # Use the most recent date in the dataset if no reference date provided
    if reference_date is None:
        reference_date = df['date'].max()
    
    # Calculate the date 5 years ago (approximately 5 * 365 days)
    five_years_ago = reference_date - timedelta(days=5*365)
    
    # Filter to only include data from the last 5 years
    historical_df = df[df['date'] >= five_years_ago].copy()
    
    # Extract ISO week number (1-52 or 1-53) from each date
    # ISO week: Week 1 is the first week with a Thursday in the new year
    historical_df['week_of_year'] = historical_df['date'].dt.isocalendar().week
    
    # Group by week number and calculate min/max across all years
    # This gives us the historical range for each week of the year
    range_df = historical_df.groupby('week_of_year')['value'].agg(['min', 'max']).reset_index()
    
    # Rename columns to be more descriptive
    range_df.columns = ['week_of_year', 'min_5yr', 'max_5yr']
    
    return range_df


def prepare_plot_data(df, weeks_to_show=104):
    """
    Prepare data for plotting: combine recent weekly values with 5-year range.
    
    This function takes the full historical dataset and prepares it for graphing
    by combining:
    1. The most recent N weeks of actual stock data (the line on the graph)
    2. The 5-year min/max range for those weeks (the shaded area on the graph)
    
    The result is a single DataFrame ready to pass to the graphing function.
    
    Args:
        df (pandas.DataFrame): DataFrame with 'date' and 'value' columns containing
                              all historical stock data
        weeks_to_show (int): Number of most recent weeks to display on the graph.
                            Default is 104 (two years).
    
    Returns:
        pandas.DataFrame: DataFrame ready for plotting with columns:
                         - date: Date of the observation
                         - value: Actual stock level for that week
                         - week_of_year: ISO week number
                         - min_5yr: 5-year minimum for that week
                         - max_5yr: 5-year maximum for that week
    
    Example:
        >>> df = fetch_series_data('WGTSTUS1')  # Get all historical data
        >>> plot_df = prepare_plot_data(df, weeks_to_show=52)  # Prepare last year
        >>> # plot_df now has both current values and 5-year ranges aligned by week
    """
    # Extract the most recent N weeks of data
    # tail() gets the last N rows after data is sorted by date
    recent_df = df.tail(weeks_to_show).copy()
    
    # Add ISO week number to recent data for joining with range data
    recent_df['week_of_year'] = recent_df['date'].dt.isocalendar().week
    
    # Calculate the 5-year min/max range for each week
    # This uses ALL historical data, not just the recent weeks
    range_df = calculate_five_year_range(df)
    
    # Merge the recent actual values with their corresponding 5-year ranges
    # Join on week_of_year so each week gets its historical min/max
    # left join ensures we keep all recent weeks even if range data is missing
    plot_df = recent_df.merge(range_df, on='week_of_year', how='left')
    
    return plot_df

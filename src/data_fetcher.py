"""
Fetch petroleum stock data from EIA API v2.

This module handles all communication with the U.S. Energy Information Administration
API version 2 to retrieve weekly petroleum stock data.

API Version: EIA API v2 (current as of 2026)
API Documentation: https://www.eia.gov/opendata/documentation.php
"""

import requests
import pandas as pd
from src.config import EIA_API_KEY, EIA_API_BASE


def fetch_series_data(series_id, start_date=None):
    """
    Fetch time series data from EIA API v2 for a specific petroleum stock series.
    
    EIA API v2 uses GET requests with URL parameters.
    The API returns data in a nested JSON structure that must be parsed carefully.
    
    API v2 Key Differences from v1:
    - Series IDs no longer include "PET." prefix or ".W" suffix
    - Returns data in response.data instead of series[0].data
    - Uses facets for filtering instead of direct series ID lookup
    - Supports advanced filtering, sorting, and pagination
    
    Args:
        series_id (str): EIA API v2 series identifier without prefix/suffix
                        Example: 'WGTSTUS1' for US Total Motor Gasoline Stocks
                        (NOT the old v1 format 'PET.WGTSTUS1.W')
        start_date (str, optional): Start date in YYYY-MM-DD format to limit data range.
                                   If None, returns all available historical data.
    
    Returns:
        pandas.DataFrame: DataFrame with two columns:
                         - date: datetime objects for each weekly observation
                         - value: float values in thousand barrels
    
    Raises:
        ValueError: If API key is not set or no data is returned
        requests.HTTPError: If API request fails (bad key, rate limit, etc.)
    
    Example:
        >>> df = fetch_series_data('WGTSTUS1', start_date='2020-01-01')
        >>> print(df.head())
                date    value
        0 2020-01-03  256789.0
        1 2020-01-10  258123.0
    """
    # Validate that API key is configured
    if not EIA_API_KEY:
        raise ValueError("EIA_API_KEY not set. Create a .env file with your API key.")
    
    # Construct the API v2 endpoint URL
    # Route structure: /petroleum/stoc/wstk/data/
    # - petroleum: energy source category
    # - stoc: stocks subcategory
    # - wstk: weekly stocks data
    # - data: endpoint to retrieve actual data values
    url = f"{EIA_API_BASE}/petroleum/stoc/wstk/data/"
    
    # Build the query parameters for the GET request
    # API v2 uses GET requests with parameters in the URL
    params = {
        'api_key': EIA_API_KEY,                    # Your registered API key
        'frequency': 'weekly',                      # Data frequency
        'data[0]': 'value',                        # Request the 'value' column
        'facets[series][]': series_id,             # Filter to specific series ID
        'sort[0][column]': 'period',               # Sort by date
        'sort[0][direction]': 'asc',               # Ascending order
        'offset': 0,                               # Pagination: start at first record
        'length': 5000                             # Maximum records to return
    }
    
    # Add optional start date filter if provided
    if start_date:
        params['start'] = start_date
    
    # Make GET request to API v2
    response = requests.get(url, params=params)
    
    # Raise exception if request failed (4xx or 5xx status codes)
    response.raise_for_status()
    
    # Parse JSON response
    data = response.json()
    
    # Validate response structure (API v2 nests data in response.data)
    if 'response' not in data or 'data' not in data['response']:
        raise ValueError(f"No data returned for series {series_id}")
    
    # Extract the actual data array from nested structure
    series_data = data['response']['data']
    
    # Check if data array is empty
    if not series_data:
        raise ValueError(f"Empty data returned for series {series_id}")
    
    # Convert to pandas DataFrame for easier manipulation
    df = pd.DataFrame(series_data)
    
    # Parse the 'period' field as datetime objects
    # API v2 returns dates in 'period' field (v1 used 'date')
    df['date'] = pd.to_datetime(df['period'])
    
    # Convert value strings to numeric, handling any non-numeric values as NaN
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    
    # Select only the columns we need and sort by date
    df = df[['date', 'value']].sort_values('date').reset_index(drop=True)
    
    return df

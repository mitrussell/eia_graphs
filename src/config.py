"""
Configuration for EIA data series and products.

This module contains all configuration for accessing the U.S. Energy Information
Administration (EIA) API v2 to retrieve petroleum stock data.

API Version: EIA API v2 (https://api.eia.gov/v2)
Note: EIA deprecated API v1 in November 2022. This code uses the current v2 API.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# EIA API v2 credentials and base URL
# Get your free API key at: https://www.eia.gov/opendata/register.php
EIA_API_KEY = os.getenv('EIA_API_KEY', '')
EIA_API_BASE = 'https://api.eia.gov/v2'

# Product configurations with their EIA API v2 series identifiers
# 
# API v2 Series ID Format:
# - Series IDs no longer use the old v1 format (e.g., "PET.WGTSTUS1.W")
# - New format uses just the core identifier (e.g., "WGTSTUS1")
# - These are passed as facet filters in API v2 requests
#
# Series ID Naming Convention:
# - W = Weekly frequency
# - GTST = Gasoline Total Stocks
# - CEST = Crude oil Excluding SPR Total Stocks  
# - DIST = Distillate Total Stocks
# - US1 = United States Total
# - PA11-PA51 = PADD regions 1 through 5
#
# Data Source: Weekly Petroleum Status Report (WPSR)
# Units: Thousand Barrels (converted to Million Barrels for display)
PRODUCTS = {
    'gasoline': {
        'name': 'Motor Gasoline',
        'unit': 'Million Barrels',
        'series': {
            'US': 'WGTSTUS1',      # Weekly Gasoline Total Stocks, US Total
            'PADD1': 'WGTSTPA11',  # PADD 1 (East Coast)
            'PADD2': 'WGTSTPA21',  # PADD 2 (Midwest)
            'PADD3': 'WGTSTPA31',  # PADD 3 (Gulf Coast)
            'PADD4': 'WGTSTPA41',  # PADD 4 (Rocky Mountain)
            'PADD5': 'WGTSTPA51',  # PADD 5 (West Coast)
        }
    },
    'crude': {
        'name': 'Crude Oil',
        'unit': 'Million Barrels',
        'series': {
            'US': 'WCESTUS1',      # Weekly Crude Excluding SPR Total Stocks, US Total
            'PADD1': 'WCESTP11',   # PADD 1 (East Coast)
            'PADD2': 'WCESTP21',   # PADD 2 (Midwest)
            'PADD3': 'WCESTP31',   # PADD 3 (Gulf Coast)
            'PADD4': 'WCESTP41',   # PADD 4 (Rocky Mountain)
            'PADD5': 'WCESTP51',   # PADD 5 (West Coast)
        }
    },
    'distillate': {
        'name': 'Distillate Fuel Oil',
        'unit': 'Million Barrels',
        'series': {
            'US': 'WDISTUS1',      # Weekly Distillate Total Stocks, US Total
            'PADD1': 'WDISTP11',   # PADD 1 (East Coast)
            'PADD2': 'WDISTP21',   # PADD 2 (Midwest)
            'PADD3': 'WDISTP31',   # PADD 3 (Gulf Coast)
            'PADD4': 'WDISTP41',   # PADD 4 (Rocky Mountain)
            'PADD5': 'WDISTP51',   # PADD 5 (West Coast)
        }
    }
}

# Human-readable region names for graph titles
# PADD = Petroleum Administration for Defense Districts
REGION_NAMES = {
    'US': 'U.S. Total',
    'PADD1': 'PADD 1',  # East Coast
    'PADD2': 'PADD 2',  # Midwest
    'PADD3': 'PADD 3',  # Gulf Coast
    'PADD4': 'PADD 4',  # Rocky Mountain
    'PADD5': 'PADD 5',  # West Coast
}

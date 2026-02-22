"""
Main entry point for EIA petroleum stock graph generation.

This script provides a command-line interface to generate petroleum stock graphs
that match the style of the U.S. Energy Information Administration's Weekly
Petroleum Status Report (WPSR).

Usage:
    python main.py <product> <region> [--output-dir OUTPUT_DIR]

Examples:
    python main.py gasoline US
    python main.py crude PADD3
    python main.py distillate PADD1 --output-dir graphs/

The script will:
1. Fetch data from EIA API v2
2. Calculate 5-year historical ranges
3. Generate a publication-quality graph
4. Save the graph as a PNG file
"""

import argparse
from pathlib import Path
from src.config import PRODUCTS, REGION_NAMES
from src.data_fetcher import fetch_series_data
from src.data_processor import prepare_plot_data
from src.graph_generator import create_stock_graph


def generate_graph(product, region, output_dir='output'):
    """
    Generate a petroleum stock graph for a specific product and region.
    
    This is the main orchestration function that coordinates all the steps:
    1. Validates product and region inputs
    2. Fetches data from EIA API v2
    3. Processes data to calculate 5-year ranges
    4. Generates and saves the graph
    
    Args:
        product (str): Product key from PRODUCTS config
                      Options: 'gasoline', 'crude', 'distillate'
        region (str): Region key from REGION_NAMES config
                     Options: 'US', 'PADD1', 'PADD2', 'PADD3', 'PADD4', 'PADD5'
        output_dir (str): Directory path where graph PNG will be saved
                         Default: 'output/'
    
    Raises:
        ValueError: If product or region is not recognized
    
    Example:
        >>> generate_graph('gasoline', 'US', output_dir='graphs/')
        Fetching data for U.S. Total Motor Gasoline...
        Processing data...
        Generating graph...
        Graph saved to graphs/gasoline_us_stocks.png
    """
    # Validate product input
    if product not in PRODUCTS:
        raise ValueError(f"Unknown product: {product}. Choose from {list(PRODUCTS.keys())}")
    
    # Get product configuration (name, unit, series IDs)
    product_config = PRODUCTS[product]
    
    # Validate region input for this product
    if region not in product_config['series']:
        raise ValueError(f"Unknown region: {region}. Choose from {list(product_config['series'].keys())}")
    
    # Extract configuration values
    series_id = product_config['series'][region]      # EIA API v2 series ID
    product_name = product_config['name']             # Human-readable product name
    unit = product_config['unit']                     # Unit of measurement
    region_name = REGION_NAMES[region]                # Human-readable region name
    
    # Step 1: Fetch data from EIA API v2
    print(f"Fetching data for {region_name} {product_name}...")
    df = fetch_series_data(series_id)
    
    # Step 2: Process data to calculate 5-year ranges and prepare for plotting
    print(f"Processing data...")
    plot_df = prepare_plot_data(df)
    
    # Step 3: Generate the graph
    print(f"Generating graph...")
    
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Construct output filename: {product}_{region}_stocks.png
    # Example: gasoline_us_stocks.png
    filename = f"{product}_{region.lower()}_stocks.png"
    filepath = output_path / filename
    
    # Create and save the graph
    create_stock_graph(plot_df, product_name, region_name, unit, filepath)
    
    print(f"Graph saved to {filepath}")


def main():
    """
    Command-line interface entry point.
    
    Parses command-line arguments and calls generate_graph() with the
    appropriate parameters.
    
    Command-line Arguments:
        product: Required positional argument for product type
        region: Required positional argument for geographic region
        --output-dir: Optional flag to specify output directory
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Generate EIA petroleum stock graphs',
        epilog='Example: python main.py gasoline US --output-dir graphs/'
    )
    
    # Required positional argument: product type
    parser.add_argument(
        'product',
        choices=list(PRODUCTS.keys()),
        help='Product type (gasoline, crude, or distillate)'
    )
    
    # Required positional argument: region
    parser.add_argument(
        'region',
        help='Region (US, PADD1, PADD2, PADD3, PADD4, or PADD5)'
    )
    
    # Optional argument: output directory
    parser.add_argument(
        '--output-dir',
        default='output',
        help='Output directory for graphs (default: output/)'
    )
    
    # Parse command-line arguments
    args = parser.parse_args()
    
    # Convert region to uppercase for consistency (allows user to type 'us' or 'US')
    region_upper = args.region.upper()
    
    # Generate the graph
    generate_graph(args.product, region_upper, args.output_dir)


# Standard Python idiom: only run main() if this file is executed directly
# (not if it's imported as a module)
if __name__ == '__main__':
    main()

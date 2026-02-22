"""
Generate petroleum stock graphs matching EIA Weekly Petroleum Status Report style.

This module creates publication-quality graphs that replicate the visual style of
the U.S. Energy Information Administration's Weekly Petroleum Status Report (WPSR).

Graph Style:
- Weekly stock levels shown as a blue line
- 5-year historical min/max range shown as a gray shaded area
- Clean, professional styling using seaborn themes
- Date-formatted x-axis with readable labels
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd


def setup_style():
    """
    Configure matplotlib and seaborn styling for professional-looking graphs.
    
    This applies a clean, publication-ready style that matches the EIA's
    visual standards. The style is applied globally and affects all subsequent
    matplotlib plots in the session.
    
    Style choices:
    - whitegrid: Clean white background with subtle gridlines
    - deep palette: Professional color scheme with good contrast
    """
    sns.set_style("whitegrid")
    sns.set_palette("deep")


def create_stock_graph(plot_df, product_name, region_name, unit, output_path=None):
    """
    Create a petroleum stock graph with weekly line and 5-year historical range.
    
    This function generates a graph matching the EIA Weekly Petroleum Status Report
    style, showing:
    1. A shaded gray area representing the 5-year min/max range
    2. A blue line showing current weekly stock levels
    3. Properly formatted axes with dates and units
    
    Graph Components:
    - X-axis: Dates formatted as "Mon DD\nYYYY" (e.g., "Jan 15\n2026")
    - Y-axis: Stock levels in specified units (typically Million Barrels)
    - Title: "{Region} {Product} Stocks" (e.g., "U.S. Total Motor Gasoline Stocks")
    - Legend: Shows "5-Year Range" and "Weekly" data series
    
    Args:
        plot_df (pandas.DataFrame): DataFrame with columns:
                                    - date: datetime objects
                                    - value: current weekly stock levels
                                    - min_5yr: 5-year minimum for each week
                                    - max_5yr: 5-year maximum for each week
        product_name (str): Name of petroleum product (e.g., "Motor Gasoline")
        region_name (str): Geographic region (e.g., "U.S. Total", "PADD 1")
        unit (str): Unit of measurement (e.g., "Million Barrels")
        output_path (str, optional): File path to save the graph as PNG.
                                    If None, graph is not saved to disk.
    
    Returns:
        matplotlib.figure.Figure: The generated figure object, which can be
                                 displayed with plt.show() or further customized.
    
    Example:
        >>> plot_df = prepare_plot_data(df)
        >>> fig = create_stock_graph(
        ...     plot_df,
        ...     product_name="Motor Gasoline",
        ...     region_name="U.S. Total",
        ...     unit="Million Barrels",
        ...     output_path="output/gasoline_us_stocks.png"
        ... )
    """
    # Apply the seaborn styling
    setup_style()
    
    # Create figure and axis objects
    # figsize=(12, 6) creates a wide graph suitable for time series data
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot the 5-year range as a shaded area (filled region between min and max)
    # This is drawn first so it appears behind the weekly line
    ax.fill_between(
        plot_df['date'],           # X-axis: dates
        plot_df['min_5yr'],        # Lower bound: 5-year minimum
        plot_df['max_5yr'],        # Upper bound: 5-year maximum
        alpha=0.3,                 # Transparency (0=invisible, 1=opaque)
        color='gray',              # Gray color for historical range
        label='5-Year Range'       # Legend label
    )
    
    # Plot the current weekly stock levels as a line
    # This is drawn on top of the shaded area
    ax.plot(
        plot_df['date'],           # X-axis: dates
        plot_df['value'],          # Y-axis: current stock levels
        linewidth=2,               # Line thickness
        color='#1f77b4',          # Blue color (matplotlib default blue)
        label='Weekly'             # Legend label
    )
    
    # Format the x-axis to show dates in a readable format
    # DateFormatter: Formats dates as "Mon DD\nYYYY" (e.g., "Feb 15\n2026")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d\n%Y'))
    
    # Set major tick marks every 2 months for readability
    # MonthLocator(interval=2): Places ticks on Jan, Mar, May, Jul, Sep, Nov
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    
    # Rotate date labels to horizontal and center them
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=0, ha='center')
    
    # Set axis labels with appropriate font sizes
    ax.set_xlabel('Date', fontsize=11)
    ax.set_ylabel(unit, fontsize=11)
    
    # Set graph title
    # Format: "{Region} {Product} Stocks" (e.g., "U.S. Total Motor Gasoline Stocks")
    ax.set_title(
        f'{region_name} {product_name} Stocks',
        fontsize=13,
        fontweight='bold'
    )
    
    # Add legend to identify the data series
    # loc='best': matplotlib automatically chooses the best position
    # frameon=True: draws a box around the legend
    ax.legend(loc='best', frameon=True)
    
    # Enable grid lines for easier reading of values
    # alpha=0.3: makes gridlines subtle and not distracting
    ax.grid(True, alpha=0.3)
    
    # Adjust layout to prevent label cutoff
    # This ensures all text fits within the figure boundaries
    plt.tight_layout()
    
    # Save to file if output path is provided
    if output_path:
        plt.savefig(
            output_path,
            dpi=300,              # High resolution for publication quality
            bbox_inches='tight'   # Trim any extra whitespace
        )
    
    return fig

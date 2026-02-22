#!/usr/bin/env python3
"""
Test script to verify the EIA graph generator is working correctly.

This script will attempt to generate a sample graph for US Total Motor Gasoline
stocks and report any errors encountered.

Before running:
1. Install dependencies: pip install -r requirements.txt
2. Get API key: https://www.eia.gov/opendata/register.php
3. Create .env file with: EIA_API_KEY=your_key_here
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from main import generate_graph


def test_basic_graph():
    """Test generating a basic US gasoline stocks graph."""
    print("=" * 60)
    print("Testing EIA Graph Generator")
    print("=" * 60)
    print()
    
    try:
        # Test with US Total Motor Gasoline
        print("Test 1: Generating US Total Motor Gasoline graph...")
        generate_graph('gasoline', 'US', output_dir='output')
        print("✓ Test 1 passed!")
        print()
        
        # Test with PADD3 Crude Oil
        print("Test 2: Generating PADD 3 Crude Oil graph...")
        generate_graph('crude', 'PADD3', output_dir='output')
        print("✓ Test 2 passed!")
        print()
        
        # Test with PADD1 Distillate
        print("Test 3: Generating PADD 1 Distillate graph...")
        generate_graph('distillate', 'PADD1', output_dir='output')
        print("✓ Test 3 passed!")
        print()
        
        print("=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        print()
        print("Generated graphs are in the 'output/' directory as PNG files:")
        print("  - gasoline_us_stocks.png")
        print("  - crude_padd3_stocks.png")
        print("  - distillate_padd1_stocks.png")
        
    except ValueError as e:
        print(f"✗ Configuration error: {e}")
        print()
        print("Make sure you have:")
        print("1. Created a .env file with your EIA_API_KEY")
        print("2. Registered for a free API key at https://www.eia.gov/opendata/register.php")
        sys.exit(1)
        
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        print()
        print("Error details:")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    test_basic_graph()

# EIA Petroleum Stock Graph Generator

Generate petroleum stock graphs matching the EIA Weekly Petroleum Status Report style.

Uses **EIA API v2** to fetch weekly petroleum stock data and creates publication-quality graphs with:
- Current weekly stock levels (blue line)
- 5-year historical min/max range (gray shaded area)
- Professional formatting matching EIA standards

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Get an EIA API key:
   - Register at https://www.eia.gov/opendata/register.php
   - Copy `.env.example` to `.env`
   - Add your API key to `.env`:
     ```
     EIA_API_KEY=your_api_key_here
     ```

## Usage

Generate a graph for a specific product and region:

```bash
python main.py gasoline US
python main.py crude PADD3
python main.py distillate PADD1
```

### Available Products
- `gasoline` - Motor Gasoline
- `crude` - Crude Oil (excluding SPR)
- `distillate` - Distillate Fuel Oil

### Available Regions
- `US` - U.S. Total
- `PADD1` through `PADD5` - Regional PADDs
  - PADD 1: East Coast
  - PADD 2: Midwest
  - PADD 3: Gulf Coast
  - PADD 4: Rocky Mountain
  - PADD 5: West Coast

### Options
- `--output-dir` - Specify output directory (default: `output/`)

Example with custom output directory:
```bash
python main.py gasoline US --output-dir graphs/
```

## Testing

Run the test script to verify everything is working:

```bash
python test_graphs.py
```

This will generate three sample graphs to confirm your setup is correct.

## Output

Graphs are saved as **PNG files** in the output directory with naming format:
`{product}_{region}_stocks.png`

Examples:
- `gasoline_us_stocks.png`
- `crude_padd3_stocks.png`
- `distillate_padd1_stocks.png`

Output format: PNG (300 DPI, publication quality)

## API Information

This project uses **EIA API v2** (current as of 2026). The older API v1 was deprecated in November 2022.

Key API v2 features:
- POST requests with JSON payloads
- Facet-based filtering
- Series IDs without "PET." prefix (e.g., `WGTSTUS1` instead of `PET.WGTSTUS1.W`)


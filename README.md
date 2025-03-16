# Treasury Yield Data Fetcher

## Overview
This script fetches historical U.S. Treasury yield data from the **FRED API** and calculates yield spreads. The processed data is saved as a timestamped CSV file for further analysis.

## Features
- Fetches Treasury yield data for **2-Year, 10-Year, and 30-Year** maturities.
- Calculates **10Y-2Y** and **30Y-10Y** yield spreads.
- Saves the data in a **timestamped CSV file**.
- Allows users to specify API key, date range, and output file name via **command-line arguments**.

## Usage
### Running the Script
You must provide a valid **FRED API Key** to fetch data. To run the script, use:

## Output
The script generates a **CSV file** containing:
- **Date** (formatted as YYYY-MM-DD)
- **2-Year Yield**
- **10-Year Yield**
- **30-Year Yield**
- **10Y-2Y Spread** (Difference between 10-Year and 2-Year yields)
- **30Y-10Y Spread** (Difference between 30-Year and 10-Year yields)

Example output (first few rows):
```csv
date,2-Year,10-Year,30-Year,10Y-2Y,30Y-10Y
2024-01-01,4.5,4.8,5.1,0.3,0.3
2024-01-02,4.4,4.7,5.0,0.3,0.3
```


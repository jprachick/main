import requests
import pandas as pd
import datetime
from typing import Optional, Dict

def fetch_fred_data(series_id: str, api_key: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
    """
    Fetches historical Treasury yield data from the FRED API.
    
    Args:
        series_id (str): The FRED series ID for Treasury yields.
        api_key (str): API key for accessing FRED data.
        start_date (str): Start date for fetching data (YYYY-MM-DD format).
        end_date (str): End date for fetching data (YYYY-MM-DD format).
    
    Returns:
        Optional[pd.DataFrame]: A DataFrame containing date and yield values, or None if an error occurs.
    """
    BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "observation_start": start_date,
        "observation_end": end_date,
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json().get("observations", [])
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df = df.dropna(subset=["value"])  # Remove missing values
        return df[["date", "value"]]
    else:
        print(f"Error fetching data for {series_id}: {response.text}")
        return None

def fetch_treasury_yields(api_key: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetches Treasury yields for multiple maturities and calculates yield spreads.
    
    Args:
        api_key (str): API key for accessing FRED data.
        start_date (str): Start date for fetching data (YYYY-MM-DD format).
        end_date (str): End date for fetching data (YYYY-MM-DD format).
    
    Returns:
        pd.DataFrame: A DataFrame containing Treasury yields and yield spreads.
    """
    series_ids: Dict[str, str] = {
        "2-Year": "DGS2",
        "10-Year": "DGS10",
        "30-Year": "DGS30",
    }
    
    dfs = []
    for name, series_id in series_ids.items():
        df = fetch_fred_data(series_id, api_key, start_date, end_date)
        if df is not None:
            df.rename(columns={"value": name}, inplace=True)
            dfs.append(df)
    
    if not dfs:
        raise ValueError("No data was retrieved from FRED API.")
    
    # Merge data on date
    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = pd.merge(merged_df, df, on="date", how="outer")
    
    # Sort data by date
    merged_df = merged_df.sort_values("date")
    
    # Calculate Yield Spreads
    merged_df["10Y-2Y"] = merged_df["10-Year"] - merged_df["2-Year"]
    merged_df["30Y-10Y"] = merged_df["30-Year"] - merged_df["10-Year"]
    
    return merged_df

def save_to_csv(df: pd.DataFrame, output_file: str) -> None:
    """
    Saves the DataFrame to a CSV file with a timestamped filename.
    
    Args:
        df (pd.DataFrame): The DataFrame to save.
        output_file (str): The base filename (without timestamp).
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{output_file}_{timestamp}.csv"
    df.to_csv(file_name, index=False)
    print(f"Data saved to {file_name}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Fetch and save Treasury yield data from FRED API.")
    parser.add_argument("--api_key", required=True, help="FRED API Key")
    parser.add_argument("--start_date", default="2000-01-01", help="Start date for data fetch (YYYY-MM-DD)")
    parser.add_argument("--end_date", default=datetime.datetime.today().strftime("%Y-%m-%d"), help="End date for data fetch (YYYY-MM-DD)")
    parser.add_argument("--output_file", default="treasury_yields", help="Base name for output CSV file")
    
    args = parser.parse_args()
    
    treasury_data = fetch_treasury_yields(args.api_key, args.start_date, args.end_date)
    save_to_csv(treasury_data, args.output_file)

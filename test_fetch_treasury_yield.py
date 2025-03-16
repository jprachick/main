import unittest
import pandas as pd
from fetch_treasury_yield import fetch_fred_data, fetch_treasury_yields

# Replace with your actual API key for testing
API_KEY = "your_actual_fred_api_key"
START_DATE = "2020-01-01"
END_DATE = "2023-01-01"

class TestFetchTreasuryYield(unittest.TestCase):
    
    def test_fetch_fred_data(self):
        """Test fetching a single Treasury yield series."""
        series_id = "DGS10"  # 10-Year Treasury Yield
        df = fetch_fred_data(series_id, API_KEY, START_DATE, END_DATE)
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertIn("date", df.columns)
        self.assertIn("value", df.columns)
        
    def test_fetch_treasury_yields(self):
        """Test fetching multiple Treasury yields and calculating spreads."""
        df = fetch_treasury_yields(API_KEY, START_DATE, END_DATE)
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertIn("date", df.columns)
        self.assertIn("2-Year", df.columns)
        self.assertIn("10-Year", df.columns)
        self.assertIn("30-Year", df.columns)
        self.assertIn("10Y-2Y", df.columns)
        self.assertIn("30Y-10Y", df.columns)
        
    def test_spread_calculations(self):
        """Ensure that the yield spread calculations are correct."""
        df = fetch_treasury_yields(API_KEY, START_DATE, END_DATE)
        df["calculated_10Y-2Y"] = df["10-Year"] - df["2-Year"]
        df["calculated_30Y-10Y"] = df["30-Year"] - df["10-Year"]
        
        self.assertTrue((df["10Y-2Y"] == df["calculated_10Y-2Y"]).all())
        self.assertTrue((df["30Y-10Y"] == df["calculated_30Y-10Y"]).all())

if __name__ == "__main__":
    unittest.main()

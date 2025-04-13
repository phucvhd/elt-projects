import yfinance as yf
from sqlalchemy import create_engine

def get_stock_data(ticker, period="1mo", interval="1d"):
    """
    Fetch historical stock data for a given ticker symbol.
    
    Parameters:
    ticker (str): The stock ticker symbol.
    period (str): The period for which to fetch data (e.g., '1d', '1mo', '1y').
    
    Returns:
    DataFrame: A DataFrame containing the historical stock data.
    """
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    df.reset_index(inplace=True)
    df['Ticker'] = ticker  # Add ticker column for identification
    return df

def fetch_stock_data(ticker, start="2023-01-01", end="2023-12-31"):
    stock = yf.Ticker(ticker)
    df = stock.history(start=start, end=end)
    df.reset_index(inplace=True)
    df['Ticker'] = ticker  # Add ticker column for identification
    return df

def convert_to_csv(data, filename):
    """
    Convert the stock data to a CSV file.
    
    Parameters:
    data (DataFrame): The stock data to convert.
    filename (str): The name of the output CSV file.
    """
    data.to_csv(filename)
    print(f"Data saved to {filename}")

def create_connection_engine(username, password, host, port, dbname):
    return create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{dbname}')

def convert_to_sql(data, engine, table_name):
    # Push DataFrame to SQL
    try:
        data.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"✅ Data loaded successfully into '{table_name}'")
    except Exception as e:
        print("❌ Failed to load data:", e)
    
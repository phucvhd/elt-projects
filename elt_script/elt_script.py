import subprocess
import yahoo_finance

# Configuration for the destination PostgreSQL database
yahoo_finance_config = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'password',
    # Use the service name from docker-compose as the hostname
    'host': 'host.docker.internal',
    'port': 5434
}

print("Starting ELT script...")

engine = yahoo_finance.create_connection_engine(
    yahoo_finance_config['user'],
    yahoo_finance_config['password'],
    yahoo_finance_config['host'],
    yahoo_finance_config['port'],
    yahoo_finance_config['dbname']
)

try:
    df = yahoo_finance.get_stock_data('AAPL', period='1mo', interval='1d')
    yahoo_finance.convert_to_sql(df, engine, 'yahoo_finance')
except Exception as e:
    print(f"Error occurred: {e}")

print("Ending ELT script...")
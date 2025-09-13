SELECT
  "Ticker",
  DATE("Date") AS "Trade date",
  "Open", "High", "Low", "Close", "Volume", "Dividends", "Stock Splits"
FROM {{source('postgres', 'yahoo_finance')}}
from yfinance import Ticker

from elt.configs.base_model import TickerInfo, StockPrice, Dividend, StockSplit, CorporateAction


class Mapper:
    @staticmethod
    def map_info(ticker: Ticker) -> TickerInfo:
        info = ticker.get_info()
        return TickerInfo(
            symbol=ticker.ticker,
            short_name=info.get("shortName"),
            long_name=info.get("longName"),
            sector=info.get("sector"),
            industry=info.get("industry"),
            country=info.get("country"),
            market_cap=info.get("marketCap"),
            currency=info.get("currency"),
            exchange=info.get("exchange"),
            long_business_summary=info.get("longBusinessSummary"),
            full_time_employees=info.get("fullTimeEmployees"),
            raw_json=info
        )

    @staticmethod
    def map_history(ticker: Ticker) -> list:
        hist = ticker.history(period="1mo", interval="1d").reset_index()
        return [
            StockPrice(
                symbol=ticker.ticker,
                date=row['Date'].to_pydatetime(),
                open=row['Open'],
                high=row['High'],
                low=row['Low'],
                close=row['Close'],
                volume=row['Volume'],
                dividends=row['Dividends'],
                stock_splits=row['Stock Splits']
            ) for _, row in hist.iterrows()
        ]

    @staticmethod
    def map_stock_price(df) -> list[StockPrice]:
        return [
            StockPrice(
                symbol=row["Ticker"],
                date=row['Date'].to_pydatetime(),
                open=row['Open'],
                high=row['High'],
                low=row['Low'],
                close=row['Close'],
                volume=row['Volume'],
                dividends=row['Dividends'],
                stock_splits=row['Stock Splits']
            ) for _, row in df.iterrows()
        ]

    @staticmethod
    def map_dividends(ticker: Ticker) -> list:
        dividends = ticker.dividends
        return [
            Dividend(symbol=ticker.ticker, date=date.to_pydatetime(), dividend=value)
            for date, value in dividends.items()
        ]

    @staticmethod
    def map_splits(ticker: Ticker) -> list:
        splits = ticker.splits
        return [
            StockSplit(symbol=ticker.ticker, date=date.to_pydatetime(), split_ratio=value)
            for date, value in splits.items()
        ]

    @staticmethod
    def map_corporate_actions(ticker: Ticker) -> list:
        actions_df = ticker.actions
        actions_list = []
        if actions_df is not None:
            for date, row in actions_df.iterrows():
                if row.get('Dividends', 0) != 0:
                    actions_list.append(CorporateAction(
                        symbol=ticker.ticker,
                        date=date.to_pydatetime(),
                        action_type='dividend',
                        value=float(row['Dividends'])
                    ))
                if row.get('Stock Splits', 0) != 0:
                    actions_list.append(CorporateAction(
                        symbol=ticker.ticker,
                        date=date.to_pydatetime(),
                        action_type='split',
                        value=float(row['Stock Splits'])
                    ))
        return actions_list
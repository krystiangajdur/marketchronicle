import datetime
import math

import yfinance as yf

from app.providers.base import PriceBar


class YFinanceProvider:
    def get_history(
        self, symbol: str, start: datetime.date, end: datetime.date | None = None
    ) -> list[PriceBar]:
        end_exclusive = None if end is None else end + datetime.timedelta(days=1)
        df = yf.Ticker(symbol).history(
            start=start.isoformat(),
            end=end_exclusive.isoformat() if end_exclusive else None,
            auto_adjust=True,
        )

        bars: list[PriceBar] = []
        for ts, row in df.iterrows():
            prices = (row["Open"], row["High"], row["Low"], row["Close"])
            if any(math.isnan(p) for p in prices):
                continue
            volume = row["Volume"]
            bars.append(
                PriceBar(
                    date=ts.date(),
                    open=float(row["Open"]),
                    high=float(row["High"]),
                    low=float(row["Low"]),
                    close=float(row["Close"]),
                    volume=None if math.isnan(volume) else int(volume),
                )
            )
        return bars

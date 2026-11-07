import datetime

import pandas as pd

from app.providers import yfinance_provider
from app.providers.yfinance_provider import YFinanceProvider


class FakeTicker:
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol

    def history(self, start, end, auto_adjust):
        index = pd.DatetimeIndex(
            ["2024-01-02", "2024-01-03", "2024-01-04"], tz="America/New_York"
        )
        return pd.DataFrame(
            {
                "Open": [10.0, 11.0, float("nan")],
                "High": [12.0, 13.0, float("nan")],
                "Low": [9.0, 10.0, float("nan")],
                "Close": [11.0, 12.0, float("nan")],
                "Volume": [1000, float("nan"), 500],
                "Dividends": [0.0, 0.0, 0.0],
                "Stock Splits": [0.0, 0.0, 0.0],
            },
            index=index,
        )


def test_converts_rows_to_price_bars(monkeypatch):
    monkeypatch.setattr(yfinance_provider.yf, "Ticker", FakeTicker)

    bars = YFinanceProvider().get_history(
        "AAPL", datetime.date(2024, 1, 2), datetime.date(2024, 1, 4)
    )

    assert len(bars) == 2  # the row with NaN prices is skipped
    assert bars[0].date == datetime.date(2024, 1, 2)
    assert bars[0].close == 11.0
    assert bars[0].volume == 1000
    assert bars[1].volume is None  # missing volume is allowed
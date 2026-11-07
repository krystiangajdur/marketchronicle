import datetime
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class PriceBar:
    date: datetime.date
    open: float
    high: float
    low: float
    close: float
    volume: int | None


class MarketDataProvider(Protocol):
    def get_history(
        self,
        symbol: str,
        start: datetime.date,
        end: datetime.date | None = None,
    ) -> list[PriceBar]: ...

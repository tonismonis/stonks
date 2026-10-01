from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Stock:
    symbol: str
    price_cents: int

    def current_price(self) -> int:
        return self.price_cents


@dataclass
class Portfolio:
    stocks: dict[Stock, Decimal]  # Owned quantities.
    allocations: dict[Stock, int]  # Basis points: 4000 means 40%.

    def rebalance(self) -> dict[str, Decimal]:
        if sum(self.allocations.values()) != 10_000:
            raise ValueError("Allocations must sum to 10000 basis points")

        # Include target stocks even when the portfolio owns none of them.
        stocks = self.stocks.keys() | self.allocations.keys()
        prices = {stock: stock.current_price() for stock in stocks}
        value = sum(
            (quantity * prices[stock] for stock, quantity in self.stocks.items()),
            Decimal("0"),
        )

        # Fractional shares can produce fractional cents. Keep intermediates
        # as Decimal; cash settlement and rounding are outside this method.
        return {
            stock.symbol: (
                value * self.allocations.get(stock, 0)
                / 10_000 / prices[stock]
                - self.stocks.get(stock, Decimal("0"))
            )
            for stock in sorted(stocks, key=lambda stock: stock.symbol)
        }


if __name__ == "__main__":
    meta = Stock("META", 10_000)
    aapl = Stock("AAPL", 5_000)
    portfolio = Portfolio(
        stocks={meta: Decimal("7"), aapl: Decimal("6")},
        allocations={meta: 4000, aapl: 6000},
    )
    assert portfolio.rebalance() == {"META": Decimal("-3"), "AAPL": Decimal("6")}
    assert portfolio.stocks == {meta: Decimal("7"), aapl: Decimal("6")}

    assert Portfolio({}, {meta: 10_000}).rebalance() == {"META": Decimal("0")}

    # Buy AAPL even though it isn't held yet.
    assert Portfolio({meta: Decimal("10")}, {meta: 4000, aapl: 6000}).rebalance() == {
        "META": Decimal("-6"), "AAPL": Decimal("12"),
    }

    # Sell META completely when it has no target allocation.
    assert Portfolio({meta: Decimal("10")}, {aapl: 10_000}).rebalance() == {
        "META": Decimal("-10"), "AAPL": Decimal("20"),
    }
    print(portfolio.rebalance())

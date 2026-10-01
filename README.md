# Portfolio rebalance

Python 3.10+. No dependencies.

Run the example and inline assertions:

```sh
python3 portfolio.py
```

Expected output:

```text
{'AAPL': Decimal('6'), 'META': Decimal('-3')}
```

`rebalance()` returns shares to buy or sell. Positive means buy, negative means
sell, zero means no trade. It leaves holdings unchanged.

Holdings map `Stock` objects to owned quantities. Allocations map `Stock`
objects to target weights, so target stocks supply prices even when not held.
The method considers stocks in either collection.

```text
portfolio value = sum(quantity × price)
target value = portfolio value × allocation
shares to trade = target value ÷ price − current quantity
```

The example starts with $700 of META and $300 of AAPL. To reach 40% META and
60% AAPL, sell 3 META shares at $100 and buy 6 AAPL shares at $50.

## Assumptions

- Prices use integer cents. `10000` is $100.
- Allocations use basis points. `4000` is 40%; the method checks they total `10000`.
- Share quantities use `Decimal`. Fractional shares are allowed because whole
  shares cannot always achieve the target weights.
- Use one `Stock` per symbol across holdings and allocations. Stocks without
  a target allocation are sold completely; unheld target stocks are bought.
- Prices are positive; quantities and allocations are nonnegative.
- One currency. No cash, fees, taxes, or price changes during rebalancing.

Fractional shares can produce fractional cents, so intermediate values use
`Decimal` too. The method does not round cash amounts because it does not
execute trades.

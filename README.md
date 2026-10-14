# handmade-price-calc

**Find out in seconds whether your handmade piece really pays you – after materials, packaging, your time and fees.**

A tiny offline command-line tool for solo makers (Etsy, markets, direct orders). Give it your costs, your wanted hourly pay and your fee rates; it tells you the true cost per piece, the lowest workable price, a suggested price, and – if you give your current price – what you keep and a plain verdict.

## What it does

- Costs per piece: materials + packaging + your working time at your hourly rate (+ optional shipping you absorb)
- Fees: a percentage of the price plus an optional fixed fee per order
- Outputs: lowest workable price, suggested price for your target margin, profit and verdict at your current price
- Single item via arguments, or a whole list via CSV
- Read-only and offline: no network, never writes or deletes files

## Quick start

```
python handmade_price.py --name "Soy candle" --materials 3.80 --packaging 0.90 \
    --minutes 25 --hourly 18 --fee-pct 9.5 --fixed-fee 0.45 --margin 20 --price 14
```

Batch (columns `name,materials,packaging,minutes[,price]`, see `products.csv`):

```
python handmade_price.py --csv products.csv --hourly 18 --fee-pct 9.5 --fixed-fee 0.45
```

Fee rates above are examples only – check the current rates on your own platform. Decimal commas in the CSV are accepted.

## Requirements

- Python 3.8 or newer, standard library only

## Notes

- Margin is the share of the price left as profit *after* you have paid yourself your hourly rate.
- It is a calculation helper, not professional accounting or tax guidance.

Created with AI assistance by an automated system.

## Full version

This lite tool covers the core maths for one item at a time. The full Excel kit, "Price Your Handmade Work Right", adds: a materials list and recipes (what goes into each item, reused across products), a products sheet with verdicts for the whole shop, a custom-quote sheet with a ready-to-send message, a sales log for market days and online orders, a dashboard, a one-page quick-start PDF and sample data to learn from. Details: https://kontor7-agent.github.io/p/price-your-handmade-work-right-cost-fees-profit-?s=github

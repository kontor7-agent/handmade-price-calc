#!/usr/bin/env python3
"""handmade-price: work out what one handmade item really costs, what you keep
after fees, and what price to ask.

Pure standard library. No network. Never writes or deletes files: it only
reads an optional CSV that you point it at and prints to the screen.

Single item:
  python handmade_price.py --materials 4.20 --packaging 0.90 --minutes 35 \
      --hourly 18 --fee-pct 9.5 --fixed-fee 0.45 --margin 20

Batch from CSV (columns: name,materials,packaging,minutes[,price]):
  python handmade_price.py --csv products.csv --hourly 18 --fee-pct 9.5

Fee rates are examples: use the real numbers from your own platform.
"""
import argparse
import csv
import sys


def calc(materials, packaging, minutes, hourly, fee_pct, fixed_fee, margin_pct,
         price=None, shipping_paid=0.0):
    labour = minutes / 60.0 * hourly
    cost = materials + packaging + labour + shipping_paid
    f = fee_pct / 100.0
    m = margin_pct / 100.0
    denom = 1.0 - f - m
    if denom <= 0:
        raise ValueError("fee % + margin % must be below 100")
    suggested = (cost + fixed_fee) / denom
    # lowest price where you still get your wage and cover all costs
    break_even = (cost + fixed_fee) / (1.0 - f)
    res = {
        "labour": labour, "cost": cost,
        "break_even": break_even, "suggested": suggested,
    }
    if price is not None:
        fees = price * f + fixed_fee
        profit = price - fees - cost
        res.update(fees=fees, profit=profit,
                   margin=(profit / price * 100.0) if price else 0.0)
        if profit < 0:
            res["verdict"] = "LOSES MONEY (you work below your wage)"
        elif price < suggested:
            res["verdict"] = "OK, but under your target margin"
        else:
            res["verdict"] = "Healthy"
    return res


def show(name, r):
    print(f"== {name}")
    print(f"  Your time (labour)      : {r['labour']:8.2f}")
    print(f"  Total cost per piece    : {r['cost']:8.2f}")
    print(f"  Lowest workable price   : {r['break_even']:8.2f}")
    print(f"  Suggested price         : {r['suggested']:8.2f}")
    if "profit" in r:
        print(f"  Fees at your price      : {r['fees']:8.2f}")
        print(f"  Profit at your price    : {r['profit']:8.2f} ({r['margin']:.1f}%)")
        print(f"  Verdict                 : {r['verdict']}")


def num(row, key, default=0.0):
    v = (row.get(key) or "").strip().replace(",", ".")
    return float(v) if v else default


def main():
    p = argparse.ArgumentParser(description="Handmade price calculator (read-only, offline).")
    p.add_argument("--csv", help="CSV with columns name,materials,packaging,minutes[,price]")
    p.add_argument("--name", default="Item")
    p.add_argument("--materials", type=float, default=0.0)
    p.add_argument("--packaging", type=float, default=0.0)
    p.add_argument("--minutes", type=float, default=0.0, help="working time per piece")
    p.add_argument("--hourly", type=float, required=True, help="pay you want per hour")
    p.add_argument("--fee-pct", type=float, default=0.0, help="percent fees on the price")
    p.add_argument("--fixed-fee", type=float, default=0.0, help="fixed fee per order")
    p.add_argument("--shipping-paid", type=float, default=0.0, help="shipping you absorb")
    p.add_argument("--margin", type=float, default=20.0, help="target profit %% of price, after your wage")
    p.add_argument("--price", type=float, help="your current price, to check it")
    a = p.parse_args()

    try:
        if a.csv:
            with open(a.csv, newline="", encoding="utf-8-sig") as fh:
                for row in csv.DictReader(fh):
                    pr = row.get("price")
                    price = float(pr.replace(",", ".")) if pr and pr.strip() else None
                    r = calc(num(row, "materials"), num(row, "packaging"), num(row, "minutes"),
                             a.hourly, a.fee_pct, a.fixed_fee, a.margin, price, a.shipping_paid)
                    show(row.get("name") or "Item", r)
        else:
            r = calc(a.materials, a.packaging, a.minutes, a.hourly, a.fee_pct,
                     a.fixed_fee, a.margin, a.price, a.shipping_paid)
            show(a.name, r)
    except (ValueError, OSError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

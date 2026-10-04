---
name: dsa-order-book
title: 'Order Book (Matching Engine)'
tags: [dsa]
difficulty: Advanced
---

## Statement

Design an order book for a trading exchange. Implement an `OrderBook` class that:

- Maintains buy and sell orders sorted by price (best prices first)
- Matches incoming orders against existing liquidity
- Tracks open orders and executed trades

Write methods:

- `add_order(order_type, price, quantity)`: add a buy/sell order
- `cancel_order(order_id)`: remove an open order
- `get_best_bid()` / `get_best_ask()`: return current market prices

### Constraints

- O(log n) insert/cancel (use heaps or BST)
- Match orders at the best available price
- Handle partial fills (order quantity > available liquidity)

### Hints

<details>
<summary>Hint 1</summary>

Use a max-heap for buy orders (sorted by price descending) and a min-heap for sell orders (sorted by price ascending).

</details>

<details>
<summary>Hint 2</summary>

When a new order arrives, iterate through the opposite side's orders and match at their prices.

</details>

## Theory

### Order Book Structure

An order book records all pending buy and sell orders in a market. The matching engine pairs buyers and sellers:

- Buy orders: sorted descending by price (highest first)
- Sell orders: sorted ascending by price (lowest first)
- Spread: gap between best bid and best ask

### Market Mechanics

- **Bid**: price at which buyers will buy
- **Ask**: price at which sellers will sell
- **Spread**: ask - bid (tighter spreads mean better liquidity)
- **Matching**: incoming order matches against opposite side at available prices

### Real-world use

Order books power stock exchanges, crypto trading, and real-time auctions:

- NASDAQ, NYSE: match millions of orders per second
- Crypto exchanges (Binance, Kraken): maintain orderbooks for each trading pair
- High-frequency trading: algorithms exploit micro-second delays in matching

## Explanation

The solution uses two heaps: a max-heap for bids (buy orders) and a min-heap for asks (sell orders). When a new buy order arrives, scan the ask heap and match at ask prices until the buy order is filled or no more sellers. Partial fills mean an order can execute in multiple matches. Cancellation removes from the heap (lazy deletion or rebuild as needed).

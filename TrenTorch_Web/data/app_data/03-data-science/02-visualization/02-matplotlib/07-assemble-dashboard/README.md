---
name: data-science-matplotlib-assemble-dashboard
title: Assemble: A Small Sales Dashboard
tags: [data-science, visualization, matplotlib, assemble]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A dashboard is several charts answering several questions about the same data, on one figure, with one consistent look. The pieces are all things you have built: a time series, a ranked bar chart, a histogram. The work is in the joining: aggregating the data _for_ each panel (the line wants monthly totals, the bars want per-region totals, the histogram wants the raw order values), labelling every axis so each panel stands alone, and putting a title over the whole figure.

This question builds a three-panel sales dashboard from one table of orders, and because every panel is built from matplotlib objects you can check each one against the aggregation it should show.

### From theory to code

Implement `sales_dashboard(df)`. The signature and docstring are already in the editor.

### Constraints

- `df` has the columns `date` (datetime), `region` (text) and `amount` (number), with at least one row.
- Return `fig`, a figure with **exactly three** Axes in one row (`plt.subplots(1, 3)`), in this order: **revenue by month**, **revenue by region**, **order amounts**.
- Panel 1 is a line of the total `amount` per calendar month, in chronological order, with the title `"Revenue by month"`, x label `"Month"` and y label `"Revenue"`.
- Panel 2 is a bar chart of the total `amount` per region, **largest total first** (ties by region name ascending), bars centred at `0..n-1` with the region names as tick labels, title `"Revenue by region"`, x label `"Region"`, y label `"Revenue"`.
- Panel 3 is a histogram of the raw `amount` values with **5 bins**, title `"Order amounts"`, x label `"Amount"`, y label `"Orders"`.
- The figure has the overall title (`suptitle`) `"Sales dashboard"`. Do not call `plt.show()`.

### Hints

<details>
<summary>Hint 1</summary>

Aggregate with pandas first (`groupby`), then draw. `df["date"].dt.to_period("M")` gives a calendar month to group by.

</details>

<details>
<summary>Hint 2</summary>

Draw each panel on its own Axes from the array that `plt.subplots(1, 3)` returns.

</details>

<details>
<summary>Hint 3</summary>

Sort the region totals with `sort_values(ascending=False, kind="mergesort")` after sorting by name, so ties come out in name order.

</details>

## Theory

### The simple version

A dashboard is a notice board with three posters. Each poster needs its own heading and labels so it makes sense alone, and the board needs a heading too. Before anything is drawn, someone has to prepare the numbers for each poster: monthly totals for one, regional totals for another, the raw list for the third.

### Aggregate, then draw

Draw functions are simple when the data is already in the shape of the picture:

| Panel             | Data prepared with pandas                   | Matplotlib call   |
| ----------------- | ------------------------------------------- | ----------------- |
| revenue by month  | `groupby(month)["amount"].sum()`            | `ax.plot`         |
| revenue by region | `groupby("region")["amount"].sum()`, sorted | `ax.bar`          |
| order amounts     | the raw column                              | `ax.hist(bins=5)` |

Keeping "compute" and "draw" separate also makes each half testable: the numbers can be checked without looking at pixels, and the picture can be checked against the numbers.

### Ranked bars

Sorting categories by value (largest first) lets the eye read the ranking directly. The order of ties must be fixed by a secondary key, here the name, or the chart can reshuffle between runs.

### Consistency

All panels use the same label style: a title, a named x axis and a named y axis with units where there are units. A `suptitle` names the whole figure. These are the cheap things that make a chart readable out of context, in a slide or a report.

### Figures with several Axes

`fig, axes = plt.subplots(1, 3)` gives a 1D array of three Axes. `fig.axes` lists all Axes in the figure in creation order, and `ax.get_title()`, `ax.get_xlabel()` and `fig._suptitle.get_text()` read the text back. `fig.tight_layout()` or `layout="constrained"` keeps labels from overlapping.

### How matplotlib actually implements this

A Figure holds a list of Axes and one `suptitle` text. Each Axes is independent: its own data limits, ticks and artists. `plt.subplots(1, 3)` positions them with a `GridSpec`. Nothing is shared unless you ask (`sharey=True`), which is why the three panels here can have different scales, as they should: months, regions and amounts are different quantities.

## Explanation

`sales_dashboard` creates a 1×3 grid and fills each panel from data prepared for it. For the first it groups `amount` by calendar month and plots the totals in chronological order. For the second it totals by region, sorts by name and then (stably) by total descending, and draws bars at integer positions with the region names as ticks. For the third it draws a 5-bin histogram of the raw amounts. Each panel gets its title and axis labels, and the figure gets the overall title.

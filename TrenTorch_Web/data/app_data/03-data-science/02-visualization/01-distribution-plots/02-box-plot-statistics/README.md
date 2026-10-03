---
name: data-science-box-plot-statistics
title: Box Plot Statistics
tags: [data-science, visualization, distributions]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A box plot compresses a whole column into five numbers and a few dots, which is why it is the standard way to compare many distributions side by side. Every part of the picture is a statistic: the line in the box is the median, the box edges are the quartiles, the whiskers reach out to the most extreme values that are not suspiciously far away, and the dots beyond the whiskers are the points the rule flags as outliers. Computing those numbers is the job of the plotting library, and this question builds them so the picture can be read for what it says and checked against the data. It relates directly to `03-outlier-detection`, whose IQR rule is the same rule that places the whiskers.

### From theory to code

Implement `five_number_summary(x)`, the minimum, first quartile, median, third quartile and maximum, then `box_plot_stats(x, whisker)`, which returns everything a box plot draws: the quartiles, the whisker ends and the outliers beyond them. The signatures and docstrings are already in the editor.

### Constraints

- `x` is a 1D float array with at least one value.
- `five_number_summary` returns a tuple `(minimum, q1, median, q3, maximum)` of floats. Quartiles use linear interpolation between order statistics, the default of `np.percentile`.
- `box_plot_stats(x, whisker)` returns a dict with keys `"q1"`, `"median"`, `"q3"`, `"lower_whisker"`, `"upper_whisker"` and `"outliers"`. The fences are `q1 - whisker * IQR` and `q3 + whisker * IQR` where `IQR = q3 - q1`. The upper whisker is the largest value of `x` that is at most the upper fence, and the lower whisker is the smallest value that is at least the lower fence. `"outliers"` is a sorted 1D float array of the values outside the fences.
- `whisker` is a non-negative float, `1.5` by default. Inputs must not be modified. Do not call `np.percentile` more than needed, and do not use a plotting library.

### Hints

<details>
<summary>Hint 1</summary>

The whiskers end at actual data values, not at the fences themselves. The fence only decides which values count as too far out.

</details>

<details>
<summary>Hint 2</summary>

A value exactly on a fence is inside it, so only values strictly beyond the fences are outliers.

</details>

<details>
<summary>Hint 3</summary>

If there are no outliers on a side, that whisker reaches the minimum or maximum of the data.

</details>

## Theory

### The simple version

Line up everyone in a room by height. The person in the middle gives the median. The people a quarter and three quarters of the way along give the box edges, so half of the room is inside the box. Anyone far taller or shorter than the box's own width would suggest gets a dot of their own, and the whiskers stretch only as far as the tallest and shortest person who is not given a dot.

### The formula

For a sample with first quartile $Q_1$, median and third quartile $Q_3$, the **interquartile range** is $\mathrm{IQR} = Q_3 - Q_1$. The **fences** are

$$
L = Q_1 - k\,\mathrm{IQR}, \qquad U = Q_3 + k\,\mathrm{IQR}
$$

with $k = 1.5$ in Tukey's convention. Then:

- the **upper whisker** is the largest observation with $x \le U$, and the **lower whisker** is the smallest observation with $x \ge L$,
- an **outlier** is any observation with $x < L$ or $x > U$,
- the **five-number summary** is $(\min, Q_1, \text{median}, Q_3, \max)$.

Quartiles with linear interpolation place $Q_p$ at position $p\,(n - 1)$ in the sorted data and blend the two neighbouring values when that position is not a whole number.

For normally distributed data, $k = 1.5$ flags about 0.7% of values, so on a large clean sample a few outlier dots are expected and are not a sign of bad data.

### What a box plot hides

Five numbers cannot show whether a distribution has two humps. Two very different shapes can have identical box plots. Overlaying the points, or using a violin plot or the density from `04-kernel-density`, shows what the summary hides. The box plot's strength is comparing many groups at once, where each group's median, spread and outliers read at a glance.

### Choosing the whisker length

The factor 1.5 is a convention, not a law. Some plots draw whiskers to the 5th and 95th percentiles, or to the minimum and maximum. Always check which rule a chart uses before comparing it with another.

### How NumPy/PyTorch actually implements this

`np.percentile(x, [25, 50, 75])` gives the quartiles. `matplotlib.pyplot.boxplot` and `matplotlib.cbook.boxplot_stats` compute and draw them, with `whis=1.5` as the whisker factor, and `seaborn.boxplot` and `pandas.DataFrame.boxplot` wrap that. `pandas.Series.describe()` reports the five-number summary with the mean and standard deviation added.

## Explanation

`five_number_summary` takes the minimum, the 25th, 50th and 75th percentiles and the maximum, all as plain floats. `box_plot_stats` computes the quartiles and the IQR, forms the two fences from the whisker factor, then selects the values inside the fences. The whisker ends are the minimum and maximum of that inside group, so they are always real data points, and the outliers are everything outside the fences, returned sorted. Using inclusive comparisons for the inside group means a value that lands exactly on a fence is not an outlier.

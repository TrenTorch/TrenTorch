---
name: data-science-pandas-sorting-ranking
title: Sorting, Ranking & Top-N
tags: [data-science, pandas, sorting, ranking]
difficulty: Beginner
---

## Statement

### The problem, from first principles

"Who are the top five?" is the commonest question asked of a table, and it hides three decisions. What happens when two rows tie for fifth place? Which rows go last when a value is missing? And do you want the rows _reordered_, or do you want each row's _position_ in the order as a new number (its rank)? Sorting and ranking look alike and answer different questions, and the answers differ most exactly where real data is awkward: ties and gaps.

This question builds the four tools you use for it: a stable multi-key sort, ranking with a chosen tie rule, a top-N that handles ties and missing values predictably, and a percentile rank that puts every value on a 0 to 1 scale.

### From theory to code

Implement `sort_by_columns(df, columns, ascending)`, `rank_scores(s, method)`, `top_n(df, column, n)` and `percent_rank(s)`. The signatures and docstrings are already in the editor.

### Constraints

- `sort_by_columns(df, columns, ascending)` sorts by the listed columns in order, each with its own direction (`ascending` is a list of bools the same length as `columns`). Rows that tie on every key keep their **original relative order** (a stable sort). Missing values go last in every key. The index labels travel with their rows.
- `rank_scores(s, method)` ranks so that the **highest** value gets rank `1`. `method` is `"min"`, `"dense"` or `"average"`: tied values get the lowest rank of the group, the next consecutive rank, or the mean of the group's ranks. Missing values stay `NaN`. The result is a float Series with `s`'s index.
- `top_n(df, column, n)` returns the `n` rows with the largest `column` values, largest first. Ties keep the original relative order. Rows where `column` is missing are never selected, so fewer than `n` rows can come back.
- `percent_rank(s)` returns `(rank_min - 1) / (count - 1)`, where `rank_min` ranks ascending (smallest value gets 1, ties share the lowest rank) and `count` is the number of non-missing values, which is at least 2. The smallest value maps to `0.0` and the largest to `1.0`. Missing stays `NaN`.

### Hints

<details>
<summary>Hint 1</summary>

`sort_values` accepts a list of columns and a list of directions. Its default algorithm is not stable for several keys; look at its `kind` argument.

</details>

<details>
<summary>Hint 2</summary>

`Series.rank` has `method` and `ascending` parameters. Flipping the direction is how the highest value becomes rank 1.

</details>

<details>
<summary>Hint 3</summary>

Drop the rows with a missing value in `column` first, then sort descending, then take the first `n`.

</details>

## Theory

### The simple version

Sorting rearranges the rows of a leaderboard. Ranking leaves the rows where they are and writes a place number next to each one. If two runners finish together, "1st, 1st, 3rd" (skip a place), "1st, 1st, 2nd" (no gap) and "1.5th, 1.5th, 3rd" (share the average) are three honest ways to number them, and which one you pick should be a decision, not an accident.

### Sorting with several keys

`df.sort_values(["dept", "salary"], ascending=[True, False])` orders by department, and within a department by salary from high to low. Because ties on both keys need _some_ order, the question becomes whether equal rows keep the order they had. A **stable** sort guarantees they do; `kind="mergesort"` (or `"stable"`) asks for that. Stability is what makes "sort by salary, then sort by department" work as a two-pass recipe, and what makes results reproducible.

### Missing values

`na_position="last"` is the default, so `NaN` rows sink to the bottom in an ascending sort **and** in a descending one. That is why top-N needs a decision: `NaN` is not large, it is unknown, so unknowns are removed before choosing the largest.

### The three tie rules

For values `[90, 80, 80, 70]` ranked from the top:

| method    | ranks              |
| --------- | ------------------ |
| `min`     | 1, 2, 2, 4         |
| `dense`   | 1, 2, 2, 3         |
| `average` | 1.0, 2.5, 2.5, 4.0 |

`min` is sports ranking, `dense` numbers distinct levels, and `average` keeps the sum of ranks constant, which is what rank-based statistics (Spearman correlation, the Wilcoxon test) need.

### Percent rank

Rescaling ranks to $[0,1]$ gives a unit-free position:

$$
\text{percent\_rank}(x_i) = \frac{\text{rank}_{\min}(x_i) - 1}{N - 1}
$$

where $N$ is the number of known values. It is the fraction of the _other_ values that are strictly smaller, which is what a spreadsheet's `PERCENTRANK` reports.

### How pandas actually implements this

`sort_values` calls NumPy's `lexsort` for several keys, or `argsort` (quicksort, or timsort when `kind="stable"`) for one, then takes the rows by position. `Series.rank` sorts once (`argsort`) and walks the sorted array assigning ranks to runs of equal values, which is $O(n \log n)$. `nlargest` uses a partial selection when it can, which is faster than a full sort for small `n`.

## Explanation

`sort_by_columns` calls `sort_values` with the stable `mergesort` algorithm so that rows tied on every key keep their input order, and `NaN` goes last by default. `rank_scores` ranks descending (`ascending=False`) so the highest value is rank 1, with the requested tie method. `top_n` drops rows whose column is missing, sorts descending with a stable algorithm so ties keep their order, and takes the first `n`. `percent_rank` ranks ascending with the `min` rule, subtracts one, and divides by the number of known values minus one, which puts the smallest at 0 and the largest at 1.

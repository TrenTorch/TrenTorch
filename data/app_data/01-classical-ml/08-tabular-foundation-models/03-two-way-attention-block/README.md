---
name: tabular-foundation-models-two-way-attention-block
title: 'Combine into a TabPFN-style two-way attention block'
tags: [tabular-foundation-models, attention]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`01-row-wise-attention` and `02-column-wise-attention` are two separate halves of the same idea — one axis alone can't capture everything a table has to say about itself. TabPFN's actual architecture alternates these two directions, letting information mix across an entire row, then across an entire column, then row again, and so on, building up genuinely table-wide context: after enough layers, information from any cell can eventually influence any other cell.

### From theory to code

Implement `two_way_attention_block(table, row_weights, col_weights)`: `row_wise_attention`, then `column_wise_attention` on its output, each with a residual connection. Reuse `01-row-wise-attention`'s `row_wise_attention` and `02-column-wise-attention`'s `column_wise_attention`. Each attention step adds its own input back to its output (a residual connection), not just the raw attention result.

### Constraints

- `table`: shape `(n_rows, n_cols, d_model)`. Returns the same shape.
- `row_weights`/`col_weights`: each a `(w_query, w_key, w_value)` tuple.
- Column-wise attention operates on the row-wise step's _output_, not the original `table`.
- With all-zero weight matrices, the output must equal the input exactly (both attention steps contribute nothing, leaving only the residual passthrough).

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`row_output = table + row_wise_attention(table, *row_weights)` — the residual add is not optional, and it's what makes the all-zero-weights sanity check hold.

</details>

<details>
<summary>Hint 2</summary>

The column-wise step's input is `row_output`, not `table` — building on what the row-wise step already produced, not starting over from scratch.

</details>

## Theory

### The simple version

This question combines the two directions into one block, the unit that would actually get stacked to build a deeper model:

```text
table
   -> row-wise attention (within each row) + residual
row_output
   -> column-wise attention (within each column) + residual
col_output  ->  the block's output
```

### The formula

The **residual connection** (`output = input + attention(input)`, rather than just `attention(input)`) is a real, deliberate Transformer-architecture detail, not an embellishment: it means the attention layer only has to learn what to _add_ to the existing representation, not reconstruct the whole thing from scratch, which makes deep stacks of these blocks dramatically easier to train. A concrete consequence, useful for checking the implementation: a block whose attention weights are all zero must leave the input completely unchanged — `attention` contributes nothing, so the residual alone passes the input straight through.

### How PyTorch actually implements this

Context only, untested by your submission: this is the same residual-connection pattern this curriculum's `04-modern-cnn-concepts/02-residual-connection` and `05-transformers-llm/01-transformer-block/03-residual-connection` questions implement — `output = x + sublayer(x)`, here applied around each of the two attention directions in sequence, exactly the block TabPFN stacks repeatedly to build its full architecture.

## Explanation

`two_way_attention_block` unpacks `row_weights`/`col_weights` (each a `(w_query, w_key, w_value)` tuple) and calls `row_wise_attention(table, *row_weights)`, adding its result to `table` itself (`row_output = table + row_wise_attention(...)`), the residual connection. It then calls `column_wise_attention` on `row_output` (not the original `table` — this step builds on whatever the row-wise step already produced), again adding the result back to its own input (`col_output = row_output + column_wise_attention(...)`).

With all-zero weight matrices, both `row_wise_attention` and `column_wise_attention` project every query/key/value to exactly `0`, giving a uniform (all-equal) attention distribution over an all-zero `value` — an attention output of exactly `0`. The two residual connections then leave `table` completely unchanged, `table + 0 + 0 = table`, a real, checkable sanity property of the implementation, not a coincidence.

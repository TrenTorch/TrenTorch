MSE doesn't punish a confidently wrong probability nearly hard enough.

```text
L = -mean( y*log(p) + (1-y)*log(1-p) )
```

- when `y = 1`, loss is `-log(p)` — grows huge as `p` approaches 0.
- when `y = 0`, loss is `-log(1-p)` — grows huge as `p` approaches 1.

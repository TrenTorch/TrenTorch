Q1-Q6 all learn `w, b` by gradient descent, directly fitting the boundary (discriminative: model `P(y|x)`). LDA models each class as its own Gaussian (generative: model `P(x|y)`, use Bayes' rule for `P(y|x)`).

```text
class 0 points cluster around mean₀
class 1 points cluster around mean₁
both classes share the same spread (covariance)
```

Sharing one covariance matrix is exactly what makes LDA's boundary linear too, arrived at by a completely different route.

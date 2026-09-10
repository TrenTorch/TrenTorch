99% one-class data lets a model score deceptively low loss by always predicting the majority class.

```text
L = -mean( w_y * (y*log(p) + (1-y)*log(1-p)) )
```

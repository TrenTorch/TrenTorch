We now have every individual piece required to train the model.

Training simply means repeating the same process many times:

```text
initialize w, b
       ↓
   predict
       ↓
   calculate loss
       ↓
   calculate gradient
       ↓
   update w, b
       ↓
     repeat
```

Each repetition is called an epoch.

As training progresses, the parameters should move toward values that produce smaller prediction errors.

This is the basic training-loop pattern that will appear again and again in deep learning. Later, the model, loss, and optimizer may become much more complicated, but the structure is fundamentally the same.

---
name: dl-training-data-augmentation
title: 'Data augmentation: label-preserving input transformations'
tags: [neural-networks, regularization, data-processing]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`[01-early-stopping]` fights overfitting by stopping training early; data augmentation fights the SAME underlying problem from a completely different angle: instead of stopping the model from memorizing a fixed training set, give it a training set that's effectively bigger and more varied in the first place, so there's less to memorize and more genuine variation to actually learn from. If you have 10,000 labeled photos of dogs and cats, and on every single epoch you feed the model a randomly flipped, randomly cropped, or slightly noised version of each photo instead of the exact same pixels every time, the model never sees the EXACT same input twice across the whole training run, which makes naive memorization far less useful, while the underlying semantic content (this is still a photo of a dog) hasn't changed at all.

The defining property every augmentation needs is right there in the name of this question: LABEL-PRESERVING. A horizontal flip of a photo of a dog is still, unambiguously, a photo of a dog; the augmented image can be safely paired with the exact same label the original had. (Not every transformation has this property: flipping a photo of a handwritten "6" upside down would turn it into something that looks like a "9", a genuinely label-CHANGING transformation you'd never want to use for this purpose.)

### From theory to code

Implement three small, independent augmentations. `horizontal_flip(image)` mirrors an image left-to-right. `random_crop(image, crop_h, crop_w, rng)` extracts a `(crop_h, crop_w)`-sized region from a random valid position, using the passed-in `rng` (a `np.random.RandomState`) to choose that position, so results are reproducible given the same `rng` state. `add_gaussian_noise(image, std, rng)` adds independent random noise to every pixel, again using `rng` for the actual random draws.

### Constraints

- `horizontal_flip` must flip along the WIDTH axis (axis `1`, for an image shaped `(H, W, ...)`), not the height axis.
- `random_crop`'s chosen top-left corner must always keep the FULL `(crop_h, crop_w)` region within the image's bounds (never cropping partially off the edge).
- All random choices (crop position, noise values) must be drawn from the PASSED-IN `rng` argument, not from NumPy's global random state, so results are exactly reproducible given the same `rng`.
- None of these functions should modify `image` in place; each should return a new array.

### Hints

<details>
<summary>Hint 1: horizontal_flip</summary>

`image[:, ::-1, ...]` reverses the WIDTH axis (axis 1) while leaving height (axis 0) and any remaining axes (like color channels) untouched; `...` (Ellipsis) matches however many trailing axes the image actually has.

</details>

<details>
<summary>Hint 2: random_crop's valid range</summary>

The top-left corner's row can range from `0` up to (and including) `height - crop_h`, so use `rng.randint(0, height - crop_h + 1)` (NumPy's `randint` upper bound is EXCLUSIVE, hence the `+1`). Same logic for the column, using `width - crop_w`.

</details>

<details>
<summary>Hint 3: add_gaussian_noise</summary>

`rng.normal(loc=0.0, scale=std, size=image.shape)` draws one independent noise value per pixel, matching `image`'s exact shape; add it directly to `image` and return the sum (this naturally creates a NEW array, rather than modifying `image` in place).

</details>

## Theory

### The simple version

A driving instructor deliberately practicing with a student under a WIDE variety of conditions, different times of day, light rain, an unfamiliar neighborhood, rather than only ever practicing the exact same route in perfect weather. The road rules haven't changed (the "label," safe driving, is preserved throughout), but the variety forces the student to learn something more GENERAL than "exactly how to drive THIS specific route," which is precisely what you want them to have learned by the time they take an actual test on unfamiliar roads. Data augmentation gives a model that same breadth of varied practice, without needing to collect a single additional labeled example.

### The formula

There's no single unifying numeric formula here (each augmentation is its own small, independent transformation), but the property they all must satisfy is worth stating precisely:

```
label(augment(x)) == label(x)   for every valid augmentation and every input x
```

This is the formal statement of "label-preserving," and it's the one property any new augmentation you might invent needs to be checked against before using it.

### How PyTorch actually implements this

`torchvision.transforms` (and its faster, GPU-friendly successor, `torchvision.transforms.v2`) implements exactly these three augmentations, and many more, as `RandomHorizontalFlip`, `RandomCrop`, and `GaussianNoise` (or manually via `torch.randn_like(x) * std`), typically composed together via `transforms.Compose([...])` into a single pipeline applied inside a `Dataset.__getitem__` (from `[03-training-loop/01-dataset-dataloader]`), so a FRESH random augmentation gets applied every single time an image is loaded, including on repeated epochs over the same underlying file. A subtlety real augmentation pipelines have to get right that this question's `rng`-parameter design makes explicit: the actual randomness needs a properly seeded, per-worker random generator when `DataLoader` uses multiple parallel worker PROCESSES (`num_workers > 1`, mentioned in `[01-dataset-dataloader]`'s Theory section), since naively sharing one global unseeded random state across separate OS processes can silently produce IDENTICAL "random" augmentations across different workers, a real, well-documented PyTorch gotcha.

## Explanation

`horizontal_flip` returns `image[:, ::-1, ...]`: the `::-1` slice on axis 1 (the width axis) reverses that axis's order while every other axis (height, and any channel axis) is left completely untouched by the `:` and `...` slices.

`random_crop` reads `height, width = image.shape[0], image.shape[1]`, computes valid top-left ranges (`height - crop_h` and `width - crop_w`, the largest starting positions that still keep the full crop inside the image), draws `top` and `left` from `rng.randint(0, ... + 1)` (the `+1` compensating for `randint`'s exclusive upper bound), and slices out `image[top : top+crop_h, left : left+crop_w]`.

`add_gaussian_noise` draws one noise value per pixel via `rng.normal(loc=0.0, scale=std, size=image.shape)`, matching `image`'s exact shape, and returns `image + noise`, a fresh array rather than an in-place modification.

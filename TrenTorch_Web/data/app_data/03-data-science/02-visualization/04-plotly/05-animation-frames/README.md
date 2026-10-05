---
name: data-science-plotly-animation-frames
title: Animation Frames & Sliders
tags: [data-science, visualization, plotly, animation]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Plotly can animate a chart in the browser with no extra code on the page. A figure may carry **frames**: a list of named snapshots, each of which overrides some traces' data. The browser steps through the frames when you press a play button or drag a slider, and _that machinery is also just data_, `updatemenus` for the buttons and `sliders` for the control, so an animated figure is still a plain figure you can build and check.

Two things make animations honest. The axis ranges must be **fixed** across frames: otherwise the axes rescale at every step and a point can look as if it did not move when the scale moved instead. And the frame names must match the slider's steps exactly, or the slider jumps to nothing. This question builds an animated scatter with Express, builds the same thing by hand from frames, and reads a frame back.

### From theory to code

Implement `animated_scatter(df, x, y, frame)`, `figure_from_frames(frames)` and `last_frame_summary(fig)`. The signatures and docstrings are already in the editor.

### Constraints

- `animated_scatter(df, x, y, frame)` returns a Plotly Express scatter with `animation_frame=frame`, and **fixed axis ranges**: the x axis range is `[min(x), max(x)]` and the y axis range `[min(y), max(y)]` over the **whole** frame (all animation frames), exactly those numbers.
- `figure_from_frames(frames)` takes a dict mapping a frame name to an `(x, y)` pair of equal-length sequences (iterated in insertion order, at least one entry) and returns a `go.Figure` whose **initial data** is one `Scatter` trace (markers only) of the **first** entry, with one `go.Frame` per entry (same name, each holding one `Scatter` of that entry's points), and a **slider** with one step per frame, in order. The slider step for a frame has `method="animate"`, `label` equal to the frame name and `args[0] == [frame_name]`.
- `last_frame_summary(fig)` describes the **last** frame of `fig` as a dict `{"name": frame name, "n_points": number of x values of its first trace, "x_max": largest x value of its first trace}` (`x_max` as a Python `float`).
- Do not call `fig.show()`.

### Hints

<details>
<summary>Hint 1</summary>

`px.scatter(..., animation_frame="col", range_x=[lo, hi], range_y=[lo, hi])` fixes the axes for the whole animation.

</details>

<details>
<summary>Hint 2</summary>

`go.Frame(data=[go.Scatter(...)], name="2020")` is one snapshot. `go.Figure(data=[...], frames=[...])` attaches them.

</details>

<details>
<summary>Hint 3</summary>

A slider step is `dict(method="animate", label=name, args=[[name], {...}])`; `fig.update_layout(sliders=[dict(steps=[...])])` adds the slider.

</details>

## Theory

### The simple version

An animated chart is a flip-book. Each page is a **frame**. The figure carries the pages, and the browser flips them when you press play or drag the slider. For the flip-book to be readable, every page must be drawn on the same-sized sheet: if each frame rescaled the axes, a dot that moved right would look still, because the ruler moved with it.

<div class="tt-widget" data-widget="data-science-plotly-animation-frames"></div>

### Frames in the structure

```
Figure
 ├─ data    : traces shown at the start
 ├─ layout  : axes, sliders, updatemenus (the play button)
 └─ frames  : [ Frame(name="2019", data=[Scatter(...)]),
                Frame(name="2020", data=[Scatter(...)]), ... ]
```

A `Frame` has a `name` and a `data` list. When it is played, its traces **replace** the traces at the same position in the figure. Frames do not store the layout, so ranges you want kept must be set on the layout itself.

### The controls are data too

A **slider** lists _steps_; each step tells the browser which frame to jump to:

```python
steps = [dict(method="animate", label=name,
              args=[[name], dict(mode="immediate",
                                 frame=dict(duration=300, redraw=True))])
         for name in names]
fig.update_layout(sliders=[dict(steps=steps)])
```

`args[0]` is the list of frame names to show, so it **must match** a frame's `name` exactly. A **play button** lives in `updatemenus` as a button with `method="animate"` and `args=[None]` (meaning "all frames").

### Fixed ranges

Plotly Express animations compute `range_x` and `range_y` for you only if you ask, and without them the axes autoscale per frame. Passing the full-data ranges (`[x.min(), x.max()]`, `[y.min(), y.max()]`) keeps one scale throughout, which is also what lets the viewer compare the first frame with the last.

### Express and animation

`px.scatter(df, x, y, animation_frame="year")` splits the frame by `year` into one `Frame` per value (sorted), creates the slider with one step per frame and a Play/Pause menu. Everything above is generated; `fig.frames`, `fig.layout.sliders` and `fig.layout.updatemenus` expose it.

### How plotly actually implements this

Frames are included in the figure's JSON. plotly.js runs `Plotly.animate`, which interpolates between the current traces and the next frame's traces over the requested duration (for properties it can interpolate, such as marker positions) and redraws. All the Python side does is hold the data.

## Explanation

`animated_scatter` calls Express with `animation_frame` and passes `range_x` and `range_y` computed from the whole data frame, so every frame uses the same axes. `figure_from_frames` creates a figure whose first trace comes from the first entry, builds one `Frame` per entry carrying that entry's points, and one slider step per frame whose `args[0]` is the frame's name. `last_frame_summary` reads the final frame from `fig.frames` and reports its name, the number of points in its first trace and the largest x.

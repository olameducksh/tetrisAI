# tetrisAI

A Tetris game built from scratch in Python with pygame, and a heuristic AI that
plays it.

The AI evaluates every possible placement of the current piece — all 4 rotations
across all columns — and picks the one that leaves the best-looking board. "Best"
is a weighted sum of four board features.

## Demo

Run `python tetris.py` and the AI takes over immediately.

## Requirements

- Python 3
- pygame

```bash
pip install pygame
```

## Usage

**Watch the AI play** (default):

```bash
python tetris.py
```

**Play it yourself** — change the two constants at the top of `tetris.py`:

```python
RUNAI = False       # stops the AI taking over
FALLSPEED = 500     # one row every 500 ms instead of instantly
```

| Key | Action |
|-----|--------|
| ← → | Move left / right |
| ↓ | Soft drop |
| ↑ | Rotate |
| Z | Hard drop |
| C | Hold piece |

## How the AI works

For each piece the AI simulates dropping it in every rotation and column, then
scores the resulting board:

```
score = W_LINES     * lines completed
      + W_HEIGHT    * aggregate column height
      + W_HOLES     * number of buried empty cells
      + W_BUMPINESS * total height difference between adjacent columns
```

The four features:

| Feature | Meaning | Wanted |
|---------|---------|--------|
| **Lines** | Rows completed by this placement | High |
| **Aggregate height** | Sum of every column's height | Low |
| **Holes** | Empty cells with a block above them | Low |
| **Bumpiness** | How jagged the surface is | Low |

It also runs the same evaluation on the piece in the hold slot and swaps if that
scores better.

Current weights (from
[Yiyuan Lee's Tetris AI writeup](https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/),
with the line-clear term scaled up):

```python
WEIGHT_LINES     =  3.4
WEIGHT_HEIGHT    = -0.51
WEIGHT_HOLES     = -0.36
WEIGHT_BUMPINESS = -0.18
```

## Files

| File | Description |
|------|-------------|
| `tetris.py` | Game engine — board, pieces, collisions, line clears, rendering, main loop |
| `ai_heuristics.py` | Board evaluation and the search over possible placements |

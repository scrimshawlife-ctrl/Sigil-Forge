# Methods: Kamea (planetary magic squares)

Version: **v1** (locked for Sigil-Forge)

This document describes the letter→number cipher and the seven planetary
kamea tables used by `scripts/kamea.py`. Tables are **hardcoded** in code;
this file is the human-readable reference and source note.

## Planetary assignment (Chaldean order)

| Key       | Planet  | Order | Magic constant M(n) | Total sum |
|-----------|---------|-------|---------------------|-----------|
| `saturn`  | Saturn  | 3×3   | 15                  | 45        |
| `jupiter` | Jupiter | 4×4   | 34                  | 136       |
| `mars`    | Mars    | 5×5   | 65                  | 325       |
| `sol`     | Sol/Sun | 6×6   | 111                 | 666       |
| `venus`   | Venus   | 7×7   | 175                 | 1225      |
| `mercury` | Mercury | 8×8   | 260                 | 2080      |
| `luna`    | Luna    | 9×9   | 369                 | 3321      |

`M(n) = n(n² + 1) / 2`. Total sum = `n · M(n)`.

## Cipher: Agrippa reduced digital mapping (v1)

Latin letters map to 1–9 by position modulo 9 (A=1 … I=9, then repeats):

```
1: A J S
2: B K T
3: C L U
4: D M V
5: E N W
6: F O X
7: G P Y
8: H Q Z
9: I R
```

Implementation: `(ord(ch.lower()) - ord('a')) % 9 + 1` for a–z.

Only values **1–9** are produced; on larger kameas the path visits the unique
cells holding those numbers (higher cells are unused by this cipher).

## Square selection

- **Operator override:** `select_square(digest, override="mars")` → that key
  (must be one of the seven keys above).
- **Default:** treat `digest_hex` as unsigned hex integer;  
  `PLANET_ORDER[int(digest, 16) % 7]`  
  with `PLANET_ORDER = saturn, jupiter, mars, sol, venus, mercury, luna`.

## Path construction

1. For each letter, map to number via the cipher.
2. Find the cell `(row, col)` containing that number (0-based).
3. Append cell center `(col + 0.5, row + 0.5)` — unit cell size, origin at
   top-left of the grid.
4. Skip non-letters and missing numbers.

## Hardcoded tables (Agrippa orientation)

Source tradition: Heinrich Cornelius Agrippa, *De Occulta Philosophia* (1531),
Book II planetary tables as commonly republished (e.g. Wikipedia “Magic
square” planetary tables; Golden Dawn / Western ceremonial practice). Saturn
uses the classic Lo Shu orientation with 5 in the center and 2 at top-right.

### Saturn 3×3 (M=15)

| 4 | 9 | 2 |
|---|---|---|
| 3 | 5 | 7 |
| 8 | 1 | 6 |

### Jupiter 4×4 (M=34)

|  4 | 14 | 15 |  1 |
|----|----|----|----|
|  9 |  7 |  6 | 12 |
|  5 | 11 | 10 |  8 |
| 16 |  2 |  3 | 13 |

### Mars 5×5 (M=65)

| 11 | 24 |  7 | 20 |  3 |
|----|----|----|----|----|
|  4 | 12 | 25 |  8 | 16 |
| 17 |  5 | 13 | 21 |  9 |
| 10 | 18 |  1 | 14 | 22 |
| 23 |  6 | 19 |  2 | 15 |

### Sol 6×6 (M=111)

|  6 | 32 |  3 | 34 | 35 |  1 |
|----|----|----|----|----|----|
|  7 | 11 | 27 | 28 |  8 | 30 |
| 19 | 14 | 16 | 15 | 23 | 24 |
| 18 | 20 | 22 | 21 | 17 | 13 |
| 25 | 29 | 10 |  9 | 26 | 12 |
| 36 |  5 | 33 |  4 |  2 | 31 |

### Venus 7×7 (M=175)

| 22 | 47 | 16 | 41 | 10 | 35 |  4 |
|----|----|----|----|----|----|----|
|  5 | 23 | 48 | 17 | 42 | 11 | 29 |
| 30 |  6 | 24 | 49 | 18 | 36 | 12 |
| 13 | 31 |  7 | 25 | 43 | 19 | 37 |
| 38 | 14 | 32 |  1 | 26 | 44 | 20 |
| 21 | 39 |  8 | 33 |  2 | 27 | 45 |
| 46 | 15 | 40 |  9 | 34 |  3 | 28 |

### Mercury 8×8 (M=260)

|  8 | 58 | 59 |  5 |  4 | 62 | 63 |  1 |
|----|----|----|----|----|----|----|----|
| 49 | 15 | 14 | 52 | 53 | 11 | 10 | 56 |
| 41 | 23 | 22 | 44 | 45 | 19 | 18 | 48 |
| 32 | 34 | 35 | 29 | 28 | 38 | 39 | 25 |
| 40 | 26 | 27 | 37 | 36 | 30 | 31 | 33 |
| 17 | 47 | 46 | 20 | 21 | 43 | 42 | 24 |
|  9 | 55 | 54 | 12 | 13 | 51 | 50 | 16 |
| 64 |  2 |  3 | 61 | 60 |  6 |  7 | 57 |

### Luna 9×9 (M=369)

| 37 | 78 | 29 | 70 | 21 | 62 | 13 | 54 |  5 |
|----|----|----|----|----|----|----|----|----|
|  6 | 38 | 79 | 30 | 71 | 22 | 63 | 14 | 46 |
| 47 |  7 | 39 | 80 | 31 | 72 | 23 | 55 | 15 |
| 16 | 48 |  8 | 40 | 81 | 32 | 64 | 24 | 56 |
| 57 | 17 | 49 |  9 | 41 | 73 | 33 | 65 | 25 |
| 26 | 58 | 18 | 50 |  1 | 42 | 74 | 34 | 66 |
| 67 | 27 | 59 | 10 | 51 |  2 | 43 | 75 | 35 |
| 36 | 68 | 19 | 60 | 11 | 52 |  3 | 44 | 76 |
| 77 | 28 | 69 | 20 | 61 | 12 | 53 |  4 | 45 |

## API (`scripts/kamea.py`)

- `KAMEA_SQUARES: dict[str, list[list[int]]]`
- `letter_to_number(ch: str) -> int`
- `select_square(digest_hex: str, override: str | None = None) -> str`
- `plot_path(letters: list[str], square_name: str) -> list[tuple[float, float]]`

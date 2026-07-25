# reCAPTCHA Challenge Dataset

[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)](LICENSE)
[![Validate Dataset](https://github.com/ssivakorn/reCAPTCHA-challenge-dataset/actions/workflows/validate.yml/badge.svg)](https://github.com/ssivakorn/reCAPTCHA-challenge-dataset/actions/workflows/validate.yml)
![Challenges](https://img.shields.io/badge/challenges-1000-blue)
![Last Update](https://img.shields.io/badge/last%20update-2026--06--14-blue)

Labeled dataset of Google reCAPTCHA visual challenges collected from real-world websites. Each challenge includes the instruction text, extracted keyword, individual tile images, and ground-truth tile labels annotated by a human annotator.

- Last Update: 2026-06-14

## Intended Use

This dataset is published for research purposes — including CAPTCHA
robustness/security research, accessibility research, and academic study
of visual challenge design. It is not intended for use in building or
operating automated systems that solve reCAPTCHA challenges to defeat
bot-detection in production (e.g. account creation abuse, scraping,
spam). Such use is likely to violate Google's reCAPTCHA and general
Terms of Service regardless of this dataset's license, and is outside
the intended use of this release.

## Challenge Types

### Type A — Independent Image Tiles
The user receives a 3×3 grid of nine independent tiles and must select
all tiles containing the target keyword. Type A has two sub-variants:
- **Static:** All matches must be identified in a single pass
- **Dynamic:** Correctly clicked tiles refresh with new images; the
  challenge loops until no matches remain

### Type B — Single Image Grid
The user receives a single photograph split into a 4×4 grid of 16 tiles
and must select all tiles containing the target keyword. All matches must
be identified in a single pass with no tile refresh.


## Annotation

Each challenge was manually labeled by a human annotator using a custom
web interface. The annotator recorded which tiles constitute correct
answers based on the challenge instruction. Labels reflect strict
exact-match criteria consistent with reCAPTCHA's own acceptance standard.


## File Formats

### `info.json`
Each challenge folder contains an `info.json` file with the following fields:

```json
{
  "instruction": "Select all squares with\ntraffic lights\nIf there are none, click skip",
  "keyword": "traffic lights",
  "correct_answers": [1, 3, 5, 7]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `instruction` | string | Full instruction text shown to the user |
| `keyword` | string | Extracted target object keyword |
| `correct_answers` | list[int] | Zero-indexed tile indices that are correct answers |

### Tile Images
- **Type A:** 9 tiles (`tile_0.png` to `tile_8.png`), each an independent image
- **Type B:** 16 tiles (`tile_0.png` to `tile_15.png`), each a crop of `full_images.png`
- Tile indices follow left-to-right, top-to-bottom order

**Type A (3×3):**

```
| 0 | 1 | 2 |

| 3 | 4 | 5 |

| 6 | 7 | 8 |
```
**Type B (4×4):**

```
|  0 |  1 |  2 |  3 |

|  4 |  5 |  6 |  7 |

|  8 |  9 | 10 | 11 |

| 12 | 13 | 14 | 15 |
```

## Validation

`scripts/validate.py` checks every folder in `dataset/` against the schema documented above and runs automatically on every push via [GitHub Actions](.github/workflows/validate.yml). For each challenge it verifies:

- `info.json` is present and parses as valid JSON
- `instruction` and `keyword` are strings, and `correct_answers` is a list
- the tile file count is either 9 (Type A) or 16 (Type B)
- the tile files present exactly match `tile_0.png` ... `tile_N.png` for that count — no gaps, no extras
- every index in `correct_answers` is an integer within range for the folder's tile count

It does not validate image content (e.g. that a tile actually matches its label) — only structural/schema correctness.

```
python3 scripts/validate.py
```

## License

Copyright (c) 2026. This dataset is released under [CC BY-NC 4.0](LICENSE) (Attribution-NonCommercial). You may share and adapt it with attribution, for non-commercial purposes only.

# How this profile is maintained

This repo is my GitHub profile README. A few pieces keep it current.

## Layout

| Path | Purpose |
| --- | --- |
| `README.md` | The profile page itself |
| `assets/` | Hero banner, button graphics and the stats card used by the README |
| `scripts/generate_stats_card.py` | Builds `assets/card-stats.svg` from public GitHub data |
| `tests/` | pytest checks for the script (valid SVG, escaping, offline mode) |
| `.github/workflows/update-profile-card.yml` | Runs the tests, then refreshes the card daily |

## Updating by hand

1. Edit `README.md`. Replace every `YOUR-...` placeholder link and every `[bracketed]` text.
2. Swap `assets/profile-hero.svg` for your own banner if you like (keep the file name or update the README).
3. Regenerate the card locally:

   ```bash
   python scripts/generate_stats_card.py --user aayushpanda77
   ```

   Use `--offline` to draw zeroed sample numbers without touching the network.

## Running the tests

```bash
pip install pytest
pytest -q
```

## Automation

The workflow runs daily and on manual dispatch. It tests the script first, regenerates
`assets/card-stats.svg`, and commits only if the file changed. No extra secrets are needed:
it uses the built-in `GITHUB_TOKEN`.

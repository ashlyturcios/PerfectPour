# Data

This project uses the Coffee Quality Institute's Arabica and Robusta ratings, compiled by James LeDoux in the [Coffee Quality Database](https://github.com/jldbc/coffee-quality-database).

To reproduce the analysis notebook, download these two files from that repo's `data/` folder and place them here:

- `arabica_ratings_raw.csv`
- `robusta_ratings_raw.csv`

The notebook expects them at `data/arabica_ratings_raw.csv` and `data/robusta_ratings_raw.csv` relative to the repo root.

The raw CSVs aren't committed to this repo directly since they're a third-party dataset — pulling from the source keeps this repo lightweight and ensures you always get the current version.

# Netflix Titles Dashboard

A single-script exploratory data analysis (EDA) tool that turns the [Netflix Movies and Series dataset](https://www.kaggle.com/datasets/debayank2024/netflix-movies-and-series) into a 6-panel visual dashboard using `pandas`, `numpy`, and `matplotlib`.

It answers common questions about the Netflix catalog: How many movies vs. TV shows are there? Which genres and countries dominate? How long are movies, and how many seasons do shows typically run?

The dataset is downloaded automatically via `kagglehub`, so no manual file download is required.

---

## Project Structure

```
.
├── netflix_project.py     # Main script: downloads data, cleans it, builds the dashboard
├── requirements.txt       # Python dependencies
├── .gitignore              # Files and folders excluded from version control
├── netflix_dashboard.png   # Generated output image (created after running the script)
└── README.md
```

---

## What the Dashboard Shows

The script generates a single figure with 6 subplots:

| Panel | Chart Type | What It Shows |
|---|---|---|
| Movies vs TV Shows | Pie chart | Overall split of content types in the catalog |
| Titles by Release Year | Line chart | Trend of movie and TV show releases over time |
| Top 10 Genres | Horizontal bar chart | Most common genres, split by movies vs. TV shows |
| Movie Duration Distribution | Bar chart | Movies grouped into Short (<=60 min), Medium (61-120 min), Long (>120 min) |
| TV Show Seasons Breakdown | Bar chart | Number of TV shows by season count |
| Top 10 Countries | Horizontal bar chart | Countries with the most titles produced |

---

## Requirements

- Python 3.8+
- A [Kaggle account](https://www.kaggle.com/) and API credentials, since the dataset is fetched through `kagglehub` (see [Kaggle API setup](#kaggle-api-setup) below)

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

---

## Kaggle API Setup

`kagglehub` needs a Kaggle API token to download the dataset:

1. Go to your [Kaggle account settings](https://www.kaggle.com/settings) and click **Create New Token** under the API section. This downloads a `kaggle.json` file.
2. Place that file at `~/.kaggle/kaggle.json` (Linux/Mac) or `C:\Users\<username>\.kaggle\kaggle.json` (Windows).
3. Alternatively, set the `KAGGLE_USERNAME` and `KAGGLE_KEY` environment variables.

`kagglehub` handles the download and caching automatically once credentials are in place — no need to manually place a CSV file in the project folder.

---

## How to Run

```bash
python netflix_project.py
```

The script will:

1. Download the dataset (or use the cached copy on subsequent runs).
2. Clean and process the data.
3. Display the dashboard in a matplotlib window.
4. Save the dashboard as `netflix_dashboard.png` in the same folder as the script.

---

## How It Works (Code Walkthrough)

1. **Download the dataset** — Uses `kagglehub.dataset_download()` to fetch the latest version of the dataset, then locates the CSV file inside the downloaded folder.
2. **Clean nulls** — Drops rows missing `rating` or `duration`, since those fields are required for the duration/rating-related charts. Missing `cast` and `country` values are filled with `"Unknown"` and excluded from their respective counts.
3. **Parse dates** — Converts `date_added` into a proper datetime column and extracts `year_added` / `month_added` for potential time-based analysis.
4. **Extract numeric duration** — Uses a regex to pull the numeric portion out of strings like `"90 min"` or `"3 Seasons"`, then splits that into separate movie-duration and TV-season columns based on `type`.
5. **Explode multi-value fields** — Both `cast` and `listed_in` (genres) can contain comma-separated lists; these are split and exploded into one row per value so they can be counted individually.
6. **Bucket movie durations** — Movies are grouped into Short / Medium / Long buckets using NumPy array filtering.
7. **Build the dashboard** — All six charts are assembled into a single 3x2 grid using `plt.subplots` with `constrained_layout=True` for clean spacing.
8. **Save and display** — The figure is saved to `netflix_dashboard.png` next to the script (so it works regardless of the current working directory) and then shown in a window.

---

## Notes and Known Limitations

- **Rows with missing `rating` or `duration` are dropped** before any analysis runs. This is a reasonable choice for consistency, but it does mean a small number of titles are excluded from every chart, not just the ones that need those fields.
- **Season counts aren't binned**: shows with unusually high season counts will each get their own bar on the "TV Show Seasons Breakdown" chart, which can make that axis sparse or cluttered. Consider grouping outliers (e.g., "10+ seasons") if your dataset has long-running series.
- **Dataset version**: `kagglehub.dataset_download()` always pulls the latest version of the dataset. If the dataset's schema changes upstream, the column names referenced in the script may need to be updated.

---

## License

This project is provided as-is for educational and portfolio purposes. The Netflix dataset itself is subject to its original license terms on Kaggle.

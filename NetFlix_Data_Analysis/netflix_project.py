from pathlib import Path

import kagglehub
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Download latest version
path = kagglehub.dataset_download("debayank2024/netflix-movies-and-series")
BASE_DIR = Path(__file__).resolve().parent

# Load the dataset before performing the cleaning and analysis steps below.
csv_files = list(Path(path).rglob("*.csv"))
if not csv_files:
    raise FileNotFoundError(f"No CSV file found in downloaded dataset: {path}")
df = pd.read_csv(csv_files[0])

print("Path to dataset files:", Path(path).resolve())
# Define relative path based on the script location


# Keep this variable available for optional release-year analysis.
relesed_year = pd.DataFrame({})

# Exclude records that cannot be used reliably in the rating and duration analyses.
df = df.dropna(subset=["rating"])
df = df.dropna(subset=["duration"])

# Calculate the total number of movies and TV shows.
movie = (df["type"] == "Movie").sum()
tv_show = (df["type"] == "TV Show").sum()
num_of_movies_series = [movie, tv_show]


# Normalize missing cast values before splitting and counting individual cast members.
df["cast"] = df["cast"].fillna("Unknown")
cast_counts = pd.DataFrame(
    {
        "cast_count": df["cast"]
        .str.split(", ")
        .explode()
        .value_counts()
        .drop("Unknown", errors="ignore")
    }
)
# Normalize country values and count titles associated with each country.
df["country"] = df["country"].fillna("Unknown")
country_counts = pd.DataFrame(
    {
        "country_count": df["country"]
        .str.split(", ")
        .explode()
        .value_counts()
        .drop("Unknown", errors="ignore")
    }
)

# Parse the date added field and derive calendar components for time-based analysis.
df["date_added_clean"] = pd.to_datetime(df["date_added"].str.strip(), errors="coerce")
df["year_added"] = df["date_added_clean"].dt.year
df["month_added"] = df["date_added_clean"].dt.month_name()

# Count titles by release year.
released_year = df["release_year"].value_counts()

# Extract the numeric portion of each duration value for comparison and grouping.


df["duration_num"] = df["duration"].str.extract(r"(\d+)").astype(float)


duration = pd.DataFrame(index=df.index)
duration["movie_duration"] = df["duration_num"].where(df["type"].eq("Movie"))
duration["series_duration"] = df["duration_num"].where(df["type"].eq("TV Show"))

movie_duration = duration["movie_duration"]

movie_duration = np.array(movie_duration.dropna())

short_movies = movie_duration[movie_duration <= 60]
medium_movies = movie_duration[(movie_duration > 60) & (movie_duration <= 120)]
long_movies = movie_duration[movie_duration > 120]

# Count TV shows by their number of seasons.
tv_seasons = df.loc[df["type"].eq("TV Show"), "duration_num"].dropna()
season_counts = tv_seasons.value_counts().sort_index()


# Expand genre combinations into one row per category and content type.
listed_in = df[["type", "listed_in"]].copy()
listed_in["listed_in"] = listed_in["listed_in"].fillna("Unknown")
listed_in = listed_in.assign(category=listed_in["listed_in"].str.split(", ")).explode(
    "category"
)
listed_in = listed_in[listed_in["category"].ne("Unknown")]

category_counts = listed_in.pivot_table(
    index="category",
    columns="type",
    aggfunc="size",
    fill_value=0,
)

# Create a dashboard containing six complementary views of the catalog.
fig, axes = plt.subplots(
    3,
    2,
    figsize=(18, 20),
    constrained_layout=True,
)

axes[0, 0].pie(
    num_of_movies_series,
    labels=["Movies", "Tv_Shows"],
    autopct="%1.1f%%",
    wedgeprops={"linewidth": 1.5, "edgecolor": "black"},
    startangle=90,
    explode=[0, 0.1],
)
# Compare the overall proportions of movies and TV shows.
axes[0, 0].set_title("Movies to TV Shows")

# Plot release-year trends separately for movies and TV shows.
titles_by_year = (
    df.groupby(["release_year", "type"]).size().unstack(fill_value=0).sort_index()
)
axes[0, 1].plot(
    titles_by_year.index,
    titles_by_year.get("Movie", 0),
    label="Movies",
)
axes[0, 1].plot(
    titles_by_year.index,
    titles_by_year.get("TV Show", 0),
    label="TV Shows",
)
axes[0, 1].set_title("Movies and TV Shows by Release Year")
axes[0, 1].set_xlabel("Year")
axes[0, 1].set_ylabel("Quantity")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# Display the ten most common genres with a movie/TV show comparison.
top_genres = category_counts.sum(axis=1).nlargest(10).sort_values()
x = np.arange(len(top_genres))
width = 0.4
axes[1, 0].barh(
    x - width / 2,
    category_counts.reindex(top_genres.index).get(
        "Movie", pd.Series(0, index=top_genres.index)
    ),
    width,
    label="Movies",
)
axes[1, 0].barh(
    x + width / 2,
    category_counts.reindex(top_genres.index).get(
        "TV Show", pd.Series(0, index=top_genres.index)
    ),
    width,
    label="TV Shows",
)
axes[1, 0].set_yticks(x, top_genres.index)
axes[1, 0].set_title("Top 10 Genres")
axes[1, 0].set_xlabel("Number of Titles")
axes[1, 0].legend()

# Group movies into short, medium, and long duration ranges.
axes[1, 1].bar(
    ["Short (≤60)", "Medium (61–120)", "Long (>120)"],
    [len(short_movies), len(medium_movies), len(long_movies)],
    color="teal",
)
axes[1, 1].set_title("Movie Duration Distribution")
axes[1, 1].set_ylabel("Number of Movies")

# Visualize the distribution of TV shows by season count.
axes[2, 0].bar(
    season_counts.index.astype(int).astype(str),
    season_counts.values,
    color="darkorange",
)
axes[2, 0].set_title("TV Show Seasons Breakdown")
axes[2, 0].set_xlabel("Number of Seasons")
axes[2, 0].set_ylabel("Number of TV Shows")
axes[2, 0].tick_params(axis="x", rotation=45)

# Show the ten countries associated with the largest number of titles.
top_countries = country_counts["country_count"].nlargest(10).sort_values()
axes[2, 1].barh(top_countries.index, top_countries.values, color="steelblue")
axes[2, 1].set_title("Top 10 Countries by Content Production")
axes[2, 1].set_xlabel("Number of Titles")
axes[2, 1].set_ylabel("Country")

# Save the generated dashboard beside the script so it works from any
# working directory (including a fresh GitHub clone).
OUTPUT_PATH = BASE_DIR / "netflix_dashboard.png"
plt.savefig(OUTPUT_PATH, dpi=150, bbox_inches="tight")
plt.show()

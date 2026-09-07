from pathlib import Path

import kagglehub
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Download the dataset with kagglehub and resolve the returned path automatically.
download_path = Path(
    kagglehub.dataset_download("yusufdelikkaya/udemy-online-education-courses")
)

# Locate the CSV file in the downloaded directory for direct loading.
csv_file = next(iter(download_path.glob("*.csv")))
df = pd.read_csv(csv_file)

# Remove duplicate records and report the resulting dataset dimensions.
df = df.drop_duplicates().copy()
print("Dataset Shape:", df.shape)

# Extract publication dates and derive the publication year for time-based analysis.
df["date_time"] = pd.to_datetime(df["published_timestamp"])
df["date_time_year"] = df["date_time"].dt.year

# Estimate gross revenue using the course price and number of subscribers.
df["estimated_revenue"] = df["price"] * df["num_subscribers"]

# Summarize course performance by subject and rank subjects by estimated revenue.
subject_analysis = (
    df.groupby("subject")
    .agg(
        total_courses=("course_id", "count"),
        total_subs=("num_subscribers", "sum"),
        total_estimated_revenue=("estimated_revenue", "sum"),
    )
    .reset_index()
)
subject_analysis = subject_analysis.sort_values(
    by="total_estimated_revenue", ascending=False
)

# Compare course volume and subscriber performance for free and paid courses.
payment_summary = (
    df.groupby("is_paid")
    .agg(
        total_courses=("course_title", "count"),
        total_subs=("num_subscribers", "sum"),
        mean_subscribers=("num_subscribers", "mean"),
    )
    .reset_index()
)

# Identify the most popular courses in each payment category.
paid_df = df[df["is_paid"]]
free_df = df[~df["is_paid"]]
top_5_free = free_df.sort_values(by="num_subscribers", ascending=False).head(5)
top_5_paid = paid_df.sort_values(by="num_subscribers", ascending=False).head(5)

# Measure the relationship between price and subscriber count among paid courses.
paid_corr = paid_df["price"].corr(paid_df["num_subscribers"])

# Aggregate course publishing activity and estimated revenue by year.
count_course_at_year = df.groupby("date_time_year").agg(
    course_at_year=("course_title", "count"),
    total_estimated_revenue_per_year=("estimated_revenue", "sum"),
)

# Calculate average price and duration for paid courses by subject.
subject_summary = paid_df.groupby("subject").agg(
    avg_price=("price", "mean"), avg_duration_hours=("content_duration", "mean")
)

# Build a four-panel dashboard for the key findings.
plt.figure(figsize=(10, 8))
plt.subplot(2, 2, 1)
sns.barplot(
    data=subject_analysis, x="subject", y="total_estimated_revenue", palette="Blues_r"
)
plt.title("Total Estimated Revenue by Subject ($)", fontweight="bold")
plt.xticks(rotation=25, ha="right")
plt.xlabel("Subject")
plt.ylabel("Revenue ($)")

plt.subplot(2, 2, 2)
sns.lineplot(
    data=count_course_at_year,
    x=count_course_at_year.index,
    y="course_at_year",
    marker="o",
    color="crimson",
    lw=2.5,
)
plt.title("Courses Published Over Time", fontweight="bold")
plt.xlabel("Year")
plt.ylabel("Number of Courses")

plt.subplot(2, 2, 3)
sns.barplot(data=payment_summary, x="is_paid", y="total_subs", palette="Set2")
plt.title("Total Subscribers: Free vs Paid", fontweight="bold")
plt.xticks(ticks=[0, 1], labels=["Free", "Paid"])
plt.xlabel("Course Type")
plt.ylabel("Subscribers")

plt.subplot(2, 2, 4)
sns.barplot(
    data=subject_summary.reset_index(), x="subject", y="avg_price", palette="mako"
)
plt.title("Average Price by Subject (Paid Only)", fontweight="bold")
plt.xticks(rotation=25, ha="right")
plt.xlabel("Subject")
plt.ylabel("Avg Price ($)")

plt.tight_layout()
images_dir = Path(__file__).resolve().parent / "images"
images_dir.mkdir(exist_ok=True)
plt.savefig(images_dir / "dashboard.png", dpi=300, bbox_inches="tight")
plt.show()

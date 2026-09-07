# Udemy Online Education Courses — EDA

Exploratory Data Analysis on Udemy's online course catalog: revenue by subject,
free vs. paid performance, publishing trends over time, and pricing patterns.

![Dashboard](images/dashboard.png)

## Dataset

- **Source:** [Udemy Online Education Courses](https://www.kaggle.com/datasets/yusufdelikkaya/udemy-online-education-courses) (Kaggle)
- **Author:** yusufdelikkaya
- Loaded automatically at runtime via [`kagglehub`](https://github.com/Kaggle/kagglehub) — no manual download needed.

## Project Structure

```
udemy-eda-project/
├── udemy_eda.py        # Main EDA script
├── README.md
├── requirements.txt
├── .gitignore
├── data/                # Downloaded dataset lands here (gitignored)
└── images/               # Generated charts (dashboard.png)
```

## What This Analysis Covers

1. **Data cleaning** — duplicate removal, shape check
2. **Feature engineering** — publication year, estimated revenue (`price × num_subscribers`)
3. **Subject-level analysis** — total courses, subscribers, and estimated revenue per subject
4. **Free vs. paid comparison** — course volume and subscriber totals by pricing type
5. **Top courses** — top 5 free and top 5 paid courses by subscriber count
6. **Price–popularity relationship** — correlation between price and subscribers (paid courses)
7. **Publishing trends** — courses published and revenue generated per year
8. **Pricing by subject** — average price and content duration per subject (paid only)

All of the above is summarized in a single 4-panel dashboard (`images/dashboard.png`).

## Setup

```bash
git clone <repo-url>
cd udemy-eda-project
pip install -r requirements.txt
```

## Usage

```bash
python udemy_eda.py
```

This will:
1. Download the dataset via `kagglehub` (cached locally after the first run)
2. Clean and process the data
3. Print key stats to the console (dataset shape, revenue by subject, price–subscriber correlation)
4. Generate and save the dashboard to `images/dashboard.png`

## Key Insights

- **Highest-earning subject by estimated revenue:** _fill in after running the script_
- **Free vs. paid subscriber gap:** _fill in after running the script_
- **Correlation between price and subscribers (paid courses):** _fill in after running the script_
- **Year with the most course launches:** _fill in after running the script_

> Run `python udemy_eda.py` and check the console output + `images/dashboard.png`
> to fill in the values above with your own numbers.

## Tech Stack

- Python, pandas — data wrangling
- matplotlib, seaborn — visualization
- kagglehub — dataset access

## License

This project is for educational/portfolio purposes. Dataset license follows the
terms set by the original Kaggle dataset.

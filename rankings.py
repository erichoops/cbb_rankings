import pandas as pd
import requests as req


def generate_rankings():
    # from datetime import datetime, timedelta

    # Get today's date minus 14 days
    # date_14_days_ago = datetime.now() - timedelta(days=14)

    # Format as YYYYMMDD
    # formatted_date = date_14_days_ago.strftime("%Y%m%d")

    #     print(formatted_date)

    #     kp_url = "https://kenpom.com/index.php"

    #     soup = BeautifulSoup(html, "html.parser")

    # url = f"https://barttorvik.com/?year=2026&sort=&hteam=&t2value=&conlimit=All&state=All&begin={formatted_date}&end=20260501&top=0&revquad=0&quad=5&venue=All&type=All&mingames=0#"

    #     driver = webdriver.Chrome()
    #     driver.get(url)
    #     time.sleep(2)
    #     html = driver.page_source
    # #     resp = req.get(url)
    #     soup = BeautifulSoup(html, 'html.parser')
    #     table = soup.find('table')

    #     rows = []
    #     for tr in table.find_all('tr')[2:]:  # Skip header row
    #         cells = [td.text.strip() for td in tr.find_all('td')]
    #         rows.append(cells)

    #     df = pd.DataFrame(rows)

    #     df_filtered = df.iloc[:, :2]

    # #     df_filtered[1] = df_filtered[1].apply(lambda x: re.sub(r"\d+", "", x).strip())

    #     df_filtered.columns = ['recency_rank','team']

    #     df_filtered['recency_rank'] = (
    #         df_filtered['recency_rank']
    #             .fillna(365)
    #             .astype(int)
    #     )

    #     df_filtered

    torvik_download = "https://barttorvik.com/2026_teamsheets.json"

    resp = req.get(torvik_download)

    data = resp.json()
    df = pd.DataFrame(data[0])

    df = df.drop(columns=[1, 2, 3, 5, 6, 7, 9])

    df.columns = ["team", "resume_metric_avg", "predictive_metric_avg"]

    df["resume_metric_avg"] = round(df["resume_metric_avg"].astype(float), 1)
    df["predictive_metric_avg"] = round(df["predictive_metric_avg"].astype(float), 1)

    # Create a DataFrame
    # df = pd.DataFrame(rows, columns=headers)
    # Two columns named 'Avg'
    # Detect and rename duplicate columns
    # cols = pd.Series(df.columns)
    # df.columns = cols.where(~cols.duplicated(), cols + '_' + cols.groupby(cols).cumcount().astype(str))

    resume_weight = 0.65
    predictive_weight = 0.35
    # recency_weight = .1

    # df = pd.DataFrame(df, columns = ['Team', 'Avg', 'Avg_1'])
    # df = df.rename(columns={'Team':'team', 'Avg': 'resume_metric_avg', 'Avg_1':'predictive_metric_avg'})
    # df["team"] = df["team"].apply(lambda x: re.sub(r"\d+", "", x).strip())
    # df["team"] = df["team"].str.replace(r"\b(FO|NO)\b", "", regex=True).str.strip()
    # recency_df = df_filtered
    # df["team"] = df["team"].str.strip()
    # recency_df = recency_df.dropna(subset=["team"])
    # recency_df["team"] = recency_df["team"].apply(lambda x: x.split("\xa0")[0])
    # df = pd.merge(df, recency_df, on="team", how ="outer")
    # df['resume_score'] = round(((365 - df['resume_metric_avg'].astype(float))/3.64),1)
    # df['resume_rank'] = df['resume_score'].rank(ascending=False).astype(int)
    df["cumulative_score"] = round(
        (
            (
                df["resume_metric_avg"].astype(float)
                + df["predictive_metric_avg"].astype(float)
            )
            / 2
        ),
        1,
    )
    # df = df.sort_values(by = 'resume_rank').reset_index()
    df["rank"] = df["cumulative_score"].rank(ascending=True, method="first")
    # df['recency_rank'] =df['recency_rank'].fillna(365).astype(int)
    # df['combined_avg'] = round(((df['resume_metric_avg'].astype(float) + df['predictive_metric_avg'].astype(float))/2),1)
    df["combined_avg"] = round(
        (
            df["resume_metric_avg"].astype(float) / (1 / resume_weight)
            + df["predictive_metric_avg"].astype(float) / (1 / predictive_weight)
        ),
        1,
    )
    # df['cumulative_score'] = round(((365 - df['score'])/3.64),1)
    df = df.dropna(subset=["rank"])
    df["rank"] = df["combined_avg"].rank(ascending=True, method="first").astype(int)
    df["team"] = df["team"].str.replace("\d+", "", regex=True)
    cols = [
        "rank",
        "team",
        "resume_metric_avg",
        "predictive_metric_avg",
        "combined_avg",
    ]  #'recency_rank'
    df = df[cols]

    df = df.rename(
        columns={
            "resume_metric_avg": "resume rank",
            "predictive_metric_avg": "predictive rank",
            # 'recency_rank': 'recency rank',
            "combined_avg": "composite rank",
        }
    )

    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    df = df.sort_values(by=["rank"], ascending=True).set_index(df.index.astype(int) + 1)

    return df

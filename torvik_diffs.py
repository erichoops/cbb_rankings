import ssl
import io

ssl._create_default_https_context = ssl._create_unverified_context

# get t rank modified lines


def get_torvik_diffs(input_date):
    import time
    import pandas as pd
    import numpy as np
    from selenium import webdriver

    #     url="https://barttorvik.com/schedule_mod.php?date=20241116&conlimit=All.&begin=20241101&end=20241115&conlimit=All&lastx=0&year=2025&top=0&hteam=&venue=All&type=All&mingames=0&quad=5&rpi=#"
    url = f"https://barttorvik.com/schedule_mod.php?year=2026&date={input_date}&sort=&begin=20261101&end={input_date}&top=0&revquad=0&quad=5&venue=All&type=All&mingames=0&lastx=0&conlimit=All#"
    #     print(url)
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    html = driver.page_source
    html = io.StringIO(html)
    tables = pd.read_html(html)
    driver.quit()
    #     table_1 = pd.read_html(url)
    df1 = tables[0]

    df1 = df1[["Matchup", "Current T-Rank Line", "Modified Line"]]

    df1 = df1[~df1["Modified Line"].str.contains("Mayaguez", na=False)]

    #     print(df1)

    df1["current_favorite"] = df1["Current T-Rank Line"].str.split("-").str[0]
    df1["current_favorite"] = df1["current_favorite"].str.strip()
    df1["current_spread"] = (
        df1["Current T-Rank Line"].str.split("-").str[1].str.split(",").str[0]
    )
    df1["modified_favorite"] = df1["Modified Line"].str.split("-").str[0]
    df1["modified_favorite"] = df1["modified_favorite"].str.strip()
    df1["modified_spread"] = (
        df1["Modified Line"]
        .str.split("-")
        .str[1]
        .str.split(",")
        .str[0]
        .str.split()
        .str[0]
    )

    df1 = df1.drop(columns=["Current T-Rank Line", "Modified Line"])
    df1["current_spread"] = df1["current_spread"].astype(float)
    df1["modified_spread"] = df1["modified_spread"].astype(float)
    df1[["current_spread", "modified_spread"]] = df1[
        ["current_spread", "modified_spread"]
    ].apply(pd.to_numeric)

    df1["diff"] = np.where(
        df1["current_favorite"] == df1["modified_favorite"],
        df1["current_spread"] - df1["modified_spread"],
        df1["current_spread"] + df1["modified_spread"],
    )

    df1["diff"] = df1["diff"].abs()

    df1 = df1.dropna(subset=["diff"])

    df1 = df1.sort_values(by="diff", ascending=False)

    return df1

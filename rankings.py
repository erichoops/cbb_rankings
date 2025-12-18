import time
import pandas as pd
import requests as req
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

   
def get_espn_sor():
    
    espn_to_kenpom = {
     "Arizona Wildcats": "Arizona",
    "Purdue Boilermakers": "Purdue",
    "Duke Blue Devils": "Duke",
    "Michigan State Spartans": "Michigan St.",
    "Georgetown Hoyas": "Georgetown",
    "Nebraska Cornhuskers": "Nebraska",
    "Louisville Cardinals": "Louisville",
    "Alabama Crimson Tide": "Alabama",
    "Houston Cougars": "Houston",
    "Gonzaga Bulldogs": "Gonzaga",
    "Michigan Wolverines": "Michigan",
    "BYU Cougars": "BYU",
    "North Carolina Tar Heels": "North Carolina",
    "Santa Clara Broncos": "Santa Clara",
    "Virginia Cavaliers": "Virginia",
    "Oklahoma State Cowboys": "Oklahoma State",
    "Vanderbilt Commodores": "Vanderbilt",
    "SMU Mustangs": "SMU",
    "Utah State Aggies": "Utah St.",
    "UCF Knights": "UCF",
    "Iowa State Cyclones": "Iowa St.",
    "UConn Huskies": "Connecticut",
    "Indiana Hoosiers": "Indiana",
    "Florida Gators": "Florida",
    "Virginia Tech Hokies": "Virginia Tech",
    "Creighton Bluejays": "Creighton",
    "Arkansas Razorbacks": "Arkansas",
    "Kansas Jayhawks": "Kansas",
    "Maryland Terrapins": "Maryland",
    "Texas Longhorns": "Texas",
    "Florida State Seminoles": "Florida St.",
    "Marquette Golden Eagles": "Marquette",
    "Oregon Ducks": "Oregon",
    "TCU Horned Frogs": "TCU",
    "LSU Tigers": "LSU",
    "Missouri Tigers": "Missouri",
    "Saint Mary's Gaels": "Saint Mary's",
    "Washington State Cougars": "Washington St.",
    "Colorado Buffaloes": "Colorado",
    "Northwestern Wildcats": "Northwestern",
    "Illinois Fighting Illini": "Illinois",
    "Wake Forest Demon Deacons": "Wake Forest",
    "Miami Hurricanes": "Miami (FL)",
    "Iowa Hawkeyes": "Iowa",
    "Rutgers Scarlet Knights": "Rutgers",
    "Penn State Nittany Lions": "Penn St.",
    "Texas A&M Aggies": "Texas A&M",
    "Providence Friars": "Providence",
    "Clemson Tigers": "Clemson",
    "Purdue Boilermakers": "Purdue",
    "Duke Blue Devils": "Duke",
    "Gonzaga Bulldogs": "Gonzaga",
    "North Carolina Tar Heels": "North Carolina",
    "UCLA Bruins": "UCLA",
    "Tennessee Volunteers": "Tennessee",
    "Florida State Seminoles": "Florida St.",
    "Kentucky Wildcats": "Kentucky",
    "Houston Cougars": "Houston",
    "San Diego State Aztecs": "San Diego St.",
    "Florida Atlantic Owls": "Florida Atlantic",
    "Mississippi State Bulldogs": "Mississippi St.",
    "NC State Wolfpack": "N.C. State",
    "Gonzaga Bulldogs": "Gonzaga",
    "Baylor Bears": "Baylor",  # already mapped, skip
    "UCLA Bruins": "UCLA",
    "Florida State Seminoles": "Florida St",
    "Purdue Boilermakers": "Purdue",
    "Virginia Cavaliers": "Virginia",
    "Dayton Flyers": "Dayton",
    "Boise State Broncos": "Boise St",
    "Creighton Bluejays": "Creighton",  # already mapped, skip
    "Saint Louis Billikens": "Saint Louis",
    "Richmond Spiders": "Richmond",
    "Houston Cougars": "Houston",
    "Memphis Tigers": "Memphis",
    "Drake Bulldogs": "Drake",
    "St. John's Red Storm": "St. John's",
    "Wisconsin Badgers": "Wisconsin",
    "Auburn Tigers": "Auburn",
    "USC Trojans": "USC",
    "Texas Tech Red Raiders": "Texas Tech",
    "Ohio State Buckeyes": "Ohio St.",
    "Ole Miss Rebels": "Mississippi",
    "Akron Zips": "Akron",
    "Georgia Bulldogs": "Georgia",
    "Villanova Wildcats": "Villanova",
    "SMU Mustangs": "SMU",
    "Miami Hurricanes": "Miami FL",
    "VCU Rams": "VCU", 
    "Oklahoma State Cowboys": "Oklahoma St.",
    "": "San Diego St.",
    }

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    espn_url = "https://www.espn.com/mens-college-basketball/bpi/_/view/resume"
    # resp = req.get(espn_url)
    # options=options
    driver = webdriver.Chrome()
    driver.get(espn_url)
    time.sleep(3)
    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table")   # or find_all for multiple tables

    df = pd.read_html(str(table))[0]

    df["sor_rank"] = df.index + 1

    #         df["School"] = df["Team"].apply(remove_mascot)

    df["School"] = df["Team"].map(espn_to_kenpom)

    return df

def get_kenpom_df(): 

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    kp_url = "https://kenpom.com/index.php"
    # options=options
    driver = webdriver.Chrome()
    driver.get(kp_url)
    time.sleep(2)
    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table")   # or find_all for multiple tables
    
    df = pd.read_html(html)[0]

    # Use ONLY the last row of the MultiIndex header
    df.columns = df.columns.get_level_values(-1)

    # Remove columns that are duplicates
    df = df.loc[:, ~df.columns.duplicated()]

    # (Optional) clean up column names
    df.columns = df.columns.str.strip()

    df = df[["Rk", "Team"]]
    
    
    
    return df

def generate_rankings():

    espn_df = get_espn_sor()
    kenpom_df = get_kenpom_df()
    merged_df = kenpom_df.merge(espn_df, left_on="Team", right_on="School", how="outer")
    merged_df["Total"] = ((merged_df["Rk"]*.5) + (merged_df["sor_rank"]*.5))
    print(merged_df.columns)
    merged_df = merged_df.drop(columns=["CONF", "Team_y", "School"])
    merged_df = merged_df.rename(columns={
    'Team_x': 'Team',
    'Rk': 'Predictive Rank',
    'sor_rank': 'Resume Rank',
    'Total': 'Score'
})
    merged_df.insert(0, 'Rank', range(len(merged_df)))

    merged_df = merged_df[['Team', 'Predictive Rank', 'Resume Rank', 'Score']]

    merged_df.sort_values(by='Score').reset_index(drop=True)

    merged_df.insert(0, 'Rank', merged_df.index + 1)

# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    # display()
    return merged_df
import requests
import os
import pandas as pd

NYT_KEY = os.environ["NYTArchiveKey"]

class Times ():
    def __init__ (self, month, year = 2020) :
        self.month = month
        self.year = year
        self.NYT_res = self.connect()

    def connect(self) :
        NYT_URL = f"https://api.nytimes.com/svc/archive/v1/{self.year}/{self.month}.json?api-key={NYT_KEY}"

        try:
            NYT_r = requests.get(NYT_URL)
            NYT_res = NYT_r.json()
            return NYT_res
        except:
            print("NYT API failed to connect")
            return

    def make_csv(self) :
        NYT = self.NYT_res["response"]["docs"]
        NYT_snippets = [NYT[i]["snippet"] for i in range(len(self.NYT_res["response"]["docs"]))]
        NYT_sources = [NYT[i]["source"] for i in range(len(self.NYT_res["response"]["docs"]))]
        NYT_headlines = [NYT[i]["headline"]["main"] for i in range(len(self.NYT_res["response"]["docs"]))]
        NYT_lead_paragraphs = [NYT[i]["lead_paragraph"] for i in range(len(self.NYT_res["response"]["docs"]))]
        NYT_date = [pd.to_datetime(NYT[i]["pub_date"]) for i in range(len(self.NYT_res["response"]["docs"]))]

        data = pd.DataFrame({"Headline": NYT_headlines, "Snippet": NYT_snippets, "Lead paragraph":NYT_lead_paragraphs, "Source": NYT_sources, "Date": NYT_date})

        data.to_csv(f"data/NYT_{self.month}_{self.year}.csv")
        return data.head()

import pandas as pd
presidents=pd.read_csv("presidents.csv")
presidents["rank"]=presidents.groupby(["state","year"])["candidatevotes"].rank(method="max",ascending=False)
presidents=presidents.loc[:,"candidate":"rank"]
print(presidents.head())
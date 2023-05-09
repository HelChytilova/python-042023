import pandas as pd
import numpy as np

# 1.cast ukolu - konci sloupcovym grafem

presidents=pd.read_csv("presidents.csv")
presidents=presidents.sort_values(by=["state","year"],ascending=True)
presients=presidents.reset_index(drop=True)
presidents["rank"]=presidents.groupby(["state","year"])["candidatevotes"].rank(method="max",ascending=False)

winners=presidents[presidents["rank"]==1]
winners=winners.sort_values(by=["year","state",],ascending=True)
winners=winners.reset_index(drop=True)

winners["winners_2Y"]=winners.groupby("state")["party_simplified"].shift()
winners=winners.sort_values(by=["state","year"],ascending=True)
winners=winners.reset_index(drop=True)
winners["change"]=np.where((winners["winners_2Y"]==winners["party_simplified"]) | (winners["winners_2Y"].isnull()) ,0,1)


winners_grp=winners.groupby(["state"])["change"].sum()
winners_grp=pd.DataFrame(winners_grp)
winners_grp=winners_grp.sort_values(by=["change"],ascending=False)
winners_grp=winners_grp.reset_index()


import matplotlib.pyplot as plt
winners_grp=winners_grp.set_index("state")
winners_grp=winners_grp.iloc[:15]
winners_grp.plot(kind="bar")
plt.show()

# 2. cast ukolu-  konci pivot tabulkou ############################################################

winners2=presidents[presidents["rank"].isin([1,2])]
winners2=winners2.sort_values(by=["state","year"],ascending=True)
winners2=winners2.reset_index(drop=True)
winners2["candidatevotes2nd"]=winners2.groupby(["state","year"])["candidatevotes"].shift(-1)


winners2=winners2[winners2["rank"]==1]
winners2["margin"]=winners2["candidatevotes"]-winners2["candidatevotes2nd"]
winners2["relativeMargin"]=winners2["margin"]/winners2["totalvotes"]
winners2=winners2.sort_values(by=["relativeMargin"],ascending=True)
winners2=winners2.reset_index(drop=True)
# print(winners2.head())

# pivot tabulka

winners=winners[winners["year"]!=1976]
winners["swing"]=np.where((winners["change"]==1) & (winners["party_simplified"]=="DEMOCRAT"),"to Dem.", 
                 np.where((winners["change"]==1) & (winners["party_simplified"]=="REPUBLICAN"),"to Rep.","no swing"))

winners_pivot= pd.pivot_table(winners, values="state", index="year",  columns="swing", aggfunc="count", fill_value=0)
winners_pivot=pd.DataFrame(winners_pivot)
winners_pivot=winners_pivot.reset_index()
print(winners_pivot)

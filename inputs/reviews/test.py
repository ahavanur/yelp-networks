import pandas as pd 
data = pd.read_csv("reviews_rated_pittsburgh.csv")
print data["Eazor's Auto Salon"].value_counts()

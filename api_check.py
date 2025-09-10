import requests
import pandas as pd
url = f"https://wttr.in/Minsk?format=j1"
r = requests.get(url).json()
forecast = {"Date": [], "Temp": [], "Weather": []}
df = pd.DataFrame(forecast)
for day in r["weather"]:
    date = day["date"]
    avgtemp = day["avgtempC"]
    desc = day["hourly"][4]["weatherDesc"][0]["value"]
    df.loc[len(df)] = [date, f"{avgtemp}*C", desc]
print(df)
import pandas as pd

df = pd.read_csv('lastinput.csv')
new_df = df.dropna()
df.dropna().to_csv('lastinput_done.csv', index=False)
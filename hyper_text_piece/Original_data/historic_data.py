import pandas as pd
f=pd.read_csv("data_for_fe.csv", low_memory=False)
# keep_col = ['site_name','firstinput','lastinput']
# keep_col = ['site_name','site_add','firstinput','lastinput']
keep_col = ['lastinput']
new_f = f[keep_col]
new_f.to_csv("lastinput.csv", index=False)

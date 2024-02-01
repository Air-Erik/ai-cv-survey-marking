import pandas as pd


df = pd.DataFrame({'points': [25, 12, 15, 14, 19],
    'assists': [5, 7, 7, 9, 12],
    'rebounds': [11, 8, 10, 6, 6]})

for i in df.index:
    print(df['points'][i])

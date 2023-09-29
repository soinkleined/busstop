import pandas as pd
df = pd.read_csv('bus-stops.csv')
df = df[['Stop_Name', 'Naptan_Atco']]
df = df.sort_values(by=['Stop_Name'])
df.to_html('templates/table.html', classes=["stopinfo-table"], justify='left', index=False)

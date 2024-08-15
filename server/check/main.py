import pandas as pd
import json
# Load JSON data from a file
json_path = '2022.json'
with open(json_path) as f:
    data = json.load(f)

data_list=[list(data['Discription'][i].values()) for i in data['Discription']]

columns = ['Tax', 'Opening Stock', 'Purchase', 'Gross Profit', 'Sale', 'closing Stock']

df = pd.DataFrame(data_list, columns=columns, index=None)

df.to_excel('outtput.xlsx', index=False)

print(df)
# df = pd.read_json()

# # Display the DataFrame
# print(df)

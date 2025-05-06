import pandas as pandas
import pandas as pd

df = pandas.read_csv("data/employees.csv", header=0).convert_dtypes()
print(df)

edges = ''
for _, row in df.iterrows():
    if not pd.isna(row.iloc[1]):
        edges += f'\t"{row.iloc[0]} -> {row.iloc[1]}";\n'

d = f'diagraph {{\n{edges}}}'
print(d)
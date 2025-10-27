import pandas as pd 

df = pd.read_excel(r"Pertussis data consolidation\PN.xlsx") 
df.to_parquet(r"Pertussis data consolidation\PN.parquet")  

df = pd.read_excel(r"Pertussis data consolidation\PH.xlsx") 
df.to_parquet(r"Pertussis data consolidation\PH.parquet") 
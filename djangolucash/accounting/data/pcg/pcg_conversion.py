import pandas as pd
from django.conf import settings
from pathlib import Path

base_path = "/Users/lucassuner/Coding - Local/Project/LucashFlow/djangolucash/"
df = pd.read_csv(Path(base_path) / "accounting" / "data" / "pcg" / "source_pcg.csv", names=["number", "depth", "name"], sep ='\t')
# TO DO : DELETE ROW WHERE INT LENGHT =  1 ||| WHICH IS ALSO EQUAL TO IF VALUE < 10
df = df[df["number"]>10]
# Reset the insternal index 
df = df.reset_index(drop=True)
df.to_csv(Path(base_path) / "accounting" / "data" / "pcg" / "worked_pcg.csv", index=False)
"""

FINALLY THIS PART IS TREATED BY DJANGO ORM

# Add the class
df.insert(column="class", value=df["number"].astype(str).str[0].astype(int), loc=len(df.columns))

# Isolate the two digits
df.insert(column="code_class", value="G", loc=len(df.columns))
### Add the code_class :letter G, C, S (General/Customer/Supplier) - TO DO
two_digits = df["number"].astype(str).str[:2]
df.loc[two_digits == '40', "code_class"] = 'S'
df.loc[two_digits == '41', "code_class"] = 'C'
df.loc[(two_digits != '10') & (two_digits != '89') , "code_class"] = 'G'
print(df)



# ADD G TO EVERYTHING - TO DO
###df.insert(column="class", value)
# EXCEPT IF C = 40 (first two letters) --> convert to str & compare
#df.to_csv("pcg/worked_pcg.csv", index=False)



print(df.head())
"""
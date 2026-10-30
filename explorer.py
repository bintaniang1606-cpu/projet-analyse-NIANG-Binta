import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)

df = pd.read_csv("data/logs_reseau.csv")

print("Taille (lignes, colonnes) :", df.shape)
print()
print(df.head())
print()
print(df.dtypes)
print()
print("Valeurs manquantes par colonne :")
print(df.isna().sum())
print()
print("Lignes en double :", df.duplicated().sum())
print()
print(df["protocol"].value_counts())
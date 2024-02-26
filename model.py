import sqlite3
import pandas as pd

data = pd.read_csv("/Users/noahbrannon/Python/LifeExpApp/data/lifeExp.csv")

connection = sqlite3.connect('counties.db')

data.to_sql('Countries', connection, if_exists='replace', index=False)
connection.commit()
connection.close()

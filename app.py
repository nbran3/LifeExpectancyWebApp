from flask import Flask, g
import pandas as pd
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = '/Users/noahbrannon/Python/LifeExpApp/counties.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

def query_data():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT SpatialCode, Location, Value FROM Countries WHERE Period = 2019 and Sex = 'Both sexes'")
    rows = cursor.fetchall()
    cursor.close()
    return rows

def main():
    with app.app_context():
        data = query_data()
        df = pd.DataFrame(data, columns=['SpatialCode', 'Location', 'Value'])
    return df

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def get_data():
    return main()

if __name__ == '__main__':
    app.run(debug=True)
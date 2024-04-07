import mysql.connector
from flask import Flask, request, jsonify, render_template

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.cnx = None

    def connect(self):
        self.cnx = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def disconnect(self):
        if self.cnx:
            self.cnx.close()

    def insert_into_yndlings(self, frugt, dyr):
        try:
            if not self.cnx:
                self.connect()

            cursor = self.cnx.cursor()

            insert_query = "INSERT INTO yndlings (frugt, dyr) VALUES (%s, %s)"
            data = (frugt, dyr)

            cursor.execute(insert_query, data)
            self.cnx.commit()

            print("Data inserted successfully.")
            return True

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

        finally:
            if cursor:
                cursor.close()

class MyApp(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = Database(
            host='172.17.0.5',
            user='root',
            password='MaaGodt*7913',
            database='gorilladb'
        )

app = MyApp(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/insert', methods=['POST'])
def insert_data():
    try:
        frugt = request.form['frugt']
        dyr = request.form['dyr']
        if app.db.insert_into_yndlings(frugt, dyr):
            return jsonify({'success': True}), 200
        else:
            return jsonify({'success': False}), 500
    except Exception as e:
        print("Error:", e)
        return jsonify({'success': False}), 500

if __name__ == '__main__':
    app.run(debug=True)

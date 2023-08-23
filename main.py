import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'Nita87521@'
)

# prepare a cursor object
cursorObject = dataBase.cursor()

# Create a database
cursorObject.execute("SELECT * FROM inventory.sale")
returns = cursorObject.fetchall()
print(returns)